#!/usr/bin/env python3
"""Extract chapter text from an EPUB file for evidence-based analysis."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


CONTAINER_PATH = "META-INF/container.xml"
XML_NAMESPACES = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
}
HEADING_TAGS = {"h1", "h2", "h3"}
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "div",
    "li",
    "p",
    "section",
    "tr",
}
SKIP_TAGS = {"head", "nav", "script", "style", "title"}
CJK_RANGE_RE = re.compile(r"[\u4e00-\u9fff]")
DEFAULT_MIN_TEXT_CHARS = 80
DEFAULT_LANGUAGE = "auto"
SUPPORTED_LANGUAGES = {"auto", "zh", "en"}

LANGUAGE_RULES = {
    "zh": {
        "front_matter_keywords": {
            "about",
            "acknowledgment",
            "acknowledgements",
            "appendix",
            "author",
            "colophon",
            "contents",
            "copyright",
            "cover",
            "dedication",
            "foreword",
            "frontmatter",
            "imprint",
            "index",
            "license",
            "notes",
            "preface",
            "title",
            "toc",
            "版权",
            "目录",
            "前言",
            "序言",
            "后记",
            "附录",
            "封面",
        },
        "front_matter_text_snippets": {
            "all rights reserved",
            "copyright ©",
            "first published",
            "isbn:",
            "出版社",
            "版权信息",
            "作 者：",
            "版权所有",
        },
        "chapter_title_patterns": (
            re.compile(r"^第[0-9一二三四五六七八九十百千零〇两]+章$"),
            re.compile(r"^chapter\s+\d+$", re.IGNORECASE),
            re.compile(r"^\d+$"),
        ),
        "chapter_marker_pattern": re.compile(
            r"^(第[0-9一二三四五六七八九十百千零〇两]+章|chapter\s+\d+|\d+)$",
            re.IGNORECASE,
        ),
        "note_start_patterns": (
            re.compile(r"^\d{3,4}年"),
            re.compile(r"^\d{1,2}世纪"),
            re.compile(r"^在日本"),
        ),
        "note_phrases": (
            "原指",
            "之称",
            "电话",
            "公害疾病",
            "受害者",
            "导致",
            "是报警电话",
            "是火警",
            "被判败诉",
        ),
    },
    "en": {
        "front_matter_keywords": {
            "about",
            "acknowledgment",
            "acknowledgements",
            "appendix",
            "author",
            "colophon",
            "contents",
            "copyright",
            "cover",
            "dedication",
            "epigraph",
            "foreword",
            "frontmatter",
            "glossary",
            "imprint",
            "index",
            "license",
            "notes",
            "preface",
            "prologue",
            "table of contents",
            "title",
            "toc",
        },
        "front_matter_text_snippets": {
            "all rights reserved",
            "copyright ©",
            "copyright",
            "first published",
            "isbn:",
            "published by",
            "no part of this publication",
            "library of congress",
        },
        "chapter_title_patterns": (
            re.compile(r"^chapter\s+\d+$", re.IGNORECASE),
            re.compile(r"^chapter\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)$", re.IGNORECASE),
            re.compile(r"^(prologue|epilogue)$", re.IGNORECASE),
            re.compile(r"^[ivxlcdm]+$", re.IGNORECASE),
            re.compile(r"^\d+$"),
        ),
        "chapter_marker_pattern": re.compile(
            r"^(chapter\s+\d+|chapter\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)|prologue|epilogue|[ivxlcdm]+|\d+)$",
            re.IGNORECASE,
        ),
        "note_start_patterns": (
            re.compile(r"^\d{4}\b"),
            re.compile(r"^(in|during)\s", re.IGNORECASE),
            re.compile(r"^(literally|historically|in japan|in china)\b", re.IGNORECASE),
        ),
        "note_phrases": (
            "literally",
            "refers to",
            "in japan",
            "emergency number",
            "police emergency",
            "fire emergency",
            "historically",
            "the term",
        ),
    },
}


@dataclass
class ExtractionContext:
    requested_language: str
    language: str
    language_source: str
    disable_front_matter_filter: bool
    include_items: tuple[str, ...]
    exclude_items: tuple[str, ...]
    diagnostics: dict[str, object]


class ExtractionFailure(ValueError):
    def __init__(self, message: str, diagnostics: dict[str, object]) -> None:
        super().__init__(message)
        self.diagnostics = diagnostics


@dataclass
class Chapter:
    order: int
    item_id: str
    href: str
    title: str
    text: str
    is_front_matter: bool
    front_matter_reason: str | None
    chapter_label: str | None
    chapter_number: str | None
    notes: list[str]

    def to_dict(self, preview_chars: int) -> dict[str, object]:
        preview = self.text[:preview_chars].replace("\n", " ")
        return {
            "order": self.order,
            "item_id": self.item_id,
            "href": self.href,
            "title": self.title,
            "text": self.text,
            "preview": preview,
            "is_front_matter": self.is_front_matter,
            "front_matter_reason": self.front_matter_reason,
            "chapter_label": self.chapter_label,
            "chapter_number": self.chapter_number,
            "notes": self.notes,
            "note_count": len(self.notes),
            "word_count": len(self.text.split()),
            "char_count": len(self.text),
        }


def detect_language(sample: str) -> str:
    if not sample.strip():
        return "en"
    cjk_count = len(CJK_RANGE_RE.findall(sample))
    alpha_count = sum(ch.isascii() and ch.isalpha() for ch in sample)
    if cjk_count >= max(20, alpha_count // 3):
        return "zh"
    return "en"


def build_context(
    requested_language: str,
    disable_front_matter_filter: bool,
    include_items: list[str] | None,
    exclude_items: list[str] | None,
) -> ExtractionContext:
    if requested_language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {requested_language}")
    language = "en" if requested_language == "auto" else requested_language
    language_source = "default"
    diagnostics: dict[str, object] = {
        "requested_language": requested_language,
        "language": language,
        "language_source": language_source,
        "disable_front_matter_filter": disable_front_matter_filter,
        "include_items": include_items or [],
        "exclude_items": exclude_items or [],
        "spine_item_count": 0,
        "html_spine_item_count": 0,
        "forced_included_items": [],
        "forced_excluded_items": [],
    }
    return ExtractionContext(
        requested_language=requested_language,
        language=language,
        language_source=language_source,
        disable_front_matter_filter=disable_front_matter_filter,
        include_items=tuple(include_items or []),
        exclude_items=tuple(exclude_items or []),
        diagnostics=diagnostics,
    )


class XHTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._current_heading_tag: str | None = None
        self._current_heading_parts: list[str] = []
        self.headings: list[str] = []
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in HEADING_TAGS:
            self._current_heading_tag = tag
            self._current_heading_parts = []
        if tag in BLOCK_TAGS:
            self._text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag == self._current_heading_tag:
            heading = normalize_whitespace("".join(self._current_heading_parts))
            if heading:
                self.headings.append(heading)
                self._text_parts.append("\n")
                self._text_parts.append(heading)
                self._text_parts.append("\n")
            self._current_heading_tag = None
            self._current_heading_parts = []
        if tag in BLOCK_TAGS:
            self._text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = html.unescape(data)
        if self._current_heading_tag is not None:
            self._current_heading_parts.append(text)
            return
        self._text_parts.append(text)

    def extracted_text(self) -> str:
        return normalize_whitespace("".join(self._text_parts))


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_opf_path(epub_zip: zipfile.ZipFile) -> str:
    container_xml = epub_zip.read(CONTAINER_PATH)
    tree = ET.fromstring(container_xml)
    rootfile = tree.find(".//container:rootfile", XML_NAMESPACES)
    if rootfile is None:
        raise ValueError("EPUB container.xml is missing a rootfile entry.")
    full_path = rootfile.attrib.get("full-path")
    if not full_path:
        raise ValueError("EPUB rootfile entry does not include full-path.")
    return full_path


def parse_package(epub_zip: zipfile.ZipFile, opf_path: str) -> tuple[str | None, list[tuple[str, str]]]:
    package_xml = epub_zip.read(opf_path)
    tree = ET.fromstring(package_xml)
    manifest: dict[str, str] = {}
    for item in tree.findall(".//opf:manifest/opf:item", XML_NAMESPACES):
        item_id = item.attrib.get("id")
        href = item.attrib.get("href")
        if item_id and href:
            manifest[item_id] = href
    spine: list[tuple[str, str]] = []
    for itemref in tree.findall(".//opf:spine/opf:itemref", XML_NAMESPACES):
        item_id = itemref.attrib.get("idref")
        href = manifest.get(item_id or "")
        if item_id and href:
            spine.append((item_id, href))
    dc_title = tree.findtext(".//dc:title", default=None, namespaces=XML_NAMESPACES)
    return dc_title.strip() if dc_title else None, spine


def resolve_href(base_path: str, href: str) -> str:
    base_dir = posixpath.dirname(base_path)
    normalized = posixpath.normpath(posixpath.join(base_dir, href))
    return normalized


def chapter_title_from_href(href: str) -> str:
    stem = Path(href).stem
    stem = stem.replace("_", " ").replace("-", " ")
    return normalize_whitespace(stem.title()) or "Untitled Chapter"


def classify_front_matter(
    title: str,
    href: str,
    text: str,
    min_text_chars: int,
    rules: dict[str, object],
) -> tuple[bool, str | None]:
    normalized_title = normalize_whitespace(title)
    if is_probable_chapter_title(normalized_title, text, min_text_chars, rules):
        return False, None
    front_matter_keywords = rules["front_matter_keywords"]
    front_matter_text_snippets = rules["front_matter_text_snippets"]
    haystacks = {
        normalized_title.lower(),
        Path(href).stem.lower(),
    }
    for hay in haystacks:
        for keyword in front_matter_keywords:
            if keyword in hay:
                return True, f"matched_keyword:{keyword}"
    words = text.split()
    lowered_text = text.lower()
    for snippet in front_matter_text_snippets:
        if snippet in lowered_text or snippet in text:
            return True, f"matched_text_snippet:{snippet}"
    if len(words) < 40:
        short_text = " ".join(words[:20]).lower()
        for keyword in front_matter_keywords:
            if keyword in short_text:
                return True, f"matched_short_text_keyword:{keyword}"
    if len(text.strip()) < min_text_chars:
        return True, "too_short_for_body_text"
    return False, None


def is_probable_chapter_title(title: str, text: str, min_text_chars: int, rules: dict[str, object]) -> bool:
    if not title:
        return False
    patterns: tuple[re.Pattern[str], ...] = rules["chapter_title_patterns"]
    if any(pattern.match(title) for pattern in patterns):
        return len(text.strip()) >= min_text_chars
    return False


def english_word_to_number(value: str) -> str | None:
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
        "eleven": "11",
        "twelve": "12",
        "thirteen": "13",
        "fourteen": "14",
        "fifteen": "15",
        "sixteen": "16",
        "seventeen": "17",
        "eighteen": "18",
        "nineteen": "19",
        "twenty": "20",
    }
    return mapping.get(value.lower())


def parse_chapter_marker(value: str, language: str) -> tuple[str | None, str | None]:
    normalized = normalize_whitespace(value)
    if not normalized:
        return None, None
    if language == "zh" and re.fullmatch(r"第([0-9一二三四五六七八九十百千零〇两]+)章", normalized):
        match = re.fullmatch(r"第([0-9一二三四五六七八九十百千零〇两]+)章", normalized)
        assert match is not None
        number = match.group(1)
        return normalized, number
    if re.fullmatch(r"chapter\s+(\d+)", normalized, flags=re.IGNORECASE):
        match = re.fullmatch(r"chapter\s+(\d+)", normalized, flags=re.IGNORECASE)
        assert match is not None
        number = match.group(1)
        return f"Chapter {number}", number
    if re.fullmatch(
        r"chapter\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)",
        normalized,
        flags=re.IGNORECASE,
    ):
        match = re.fullmatch(
            r"chapter\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)",
            normalized,
            flags=re.IGNORECASE,
        )
        assert match is not None
        word = match.group(1)
        number = english_word_to_number(word)
        return f"Chapter {word.title()}", number
    if re.fullmatch(r"(prologue|epilogue)", normalized, flags=re.IGNORECASE):
        return normalized.title(), None
    if re.fullmatch(r"\d+", normalized):
        return normalized, normalized
    return None, None


def infer_chapter_metadata(title: str, text: str, language: str) -> tuple[str | None, str | None]:
    title_label, title_number = parse_chapter_marker(title, language)
    if title_label:
        return title_label, title_number
    first_line = normalize_whitespace(text.splitlines()[0] if text.splitlines() else "")
    text_label, text_number = parse_chapter_marker(first_line, language)
    if text_label:
        return text_label, text_number
    return None, None


def is_generic_numeric_label(value: str | None) -> bool:
    if not value:
        return False
    return bool(re.fullmatch(r"\d+", normalize_whitespace(value)))


def split_paragraphs(text: str) -> list[str]:
    return [normalize_whitespace(part) for part in re.split(r"\n\s*\n", text) if normalize_whitespace(part)]


def looks_like_note_paragraph(paragraph: str, rules: dict[str, object]) -> bool:
    if len(paragraph) < 20:
        return False
    if paragraph.startswith("“"):
        return False
    note_start_patterns: tuple[re.Pattern[str], ...] = rules["note_start_patterns"]
    note_phrases: tuple[str, ...] = rules["note_phrases"]
    if any(pattern.match(paragraph) for pattern in note_start_patterns):
        return True
    if any(phrase in paragraph for phrase in note_phrases):
        digit_count = sum(ch.isdigit() for ch in paragraph)
        if digit_count >= 2 or len(paragraph) <= 180:
            return True
    return False


def split_trailing_notes(text: str, rules: dict[str, object]) -> tuple[str, list[str]]:
    paragraphs = split_paragraphs(text)
    if len(paragraphs) < 3:
        return text, []
    trailing_notes: list[str] = []
    index = len(paragraphs) - 1
    while index >= 0 and looks_like_note_paragraph(paragraphs[index], rules):
        trailing_notes.insert(0, paragraphs[index])
        index -= 1
    if len(trailing_notes) < 2:
        return text, []
    narrative = "\n\n".join(paragraphs[: index + 1]).strip()
    return narrative or text, trailing_notes


def extract_chapter(
    epub_zip: zipfile.ZipFile,
    chapter_path: str,
    order: int,
    item_id: str,
    min_text_chars: int,
    context: ExtractionContext,
) -> Chapter | None:
    raw = epub_zip.read(chapter_path)
    parser = XHTMLTextExtractor()
    parser.feed(raw.decode("utf-8", errors="ignore"))
    text = parser.extracted_text()
    if not text:
        return None
    if context.requested_language == "auto":
        detected_language = detect_language(text[:2000])
        if context.language_source == "default":
            context.language = detected_language
            context.language_source = "auto-detected-from-text"
            context.diagnostics["language"] = detected_language
            context.diagnostics["language_source"] = context.language_source
    rules = LANGUAGE_RULES[context.language]
    text, notes = split_trailing_notes(text, rules)
    title = parser.headings[0] if parser.headings else chapter_title_from_href(chapter_path)
    chapter_label, chapter_number = infer_chapter_metadata(title, text, context.language)
    is_front_matter, front_matter_reason = classify_front_matter(title, chapter_path, text, min_text_chars, rules)
    return Chapter(
        order=order,
        item_id=item_id,
        href=chapter_path,
        title=title,
        text=text,
        is_front_matter=is_front_matter,
        front_matter_reason=front_matter_reason,
        chapter_label=chapter_label,
        chapter_number=chapter_number,
        notes=notes,
    )


def load_chapters(
    epub_path: Path,
    keep_front_matter: bool,
    min_text_chars: int,
    context: ExtractionContext,
) -> tuple[str | None, list[Chapter], list[dict[str, str]]]:
    with zipfile.ZipFile(epub_path) as epub_zip:
        opf_path = get_opf_path(epub_zip)
        book_title, spine = parse_package(epub_zip, opf_path)
        context.diagnostics["opf_path"] = opf_path
        context.diagnostics["spine_item_count"] = len(spine)
        chapters: list[Chapter] = []
        skipped: list[dict[str, str]] = []
        pending_chapter_label: str | None = None
        pending_chapter_number: str | None = None
        for order, (item_id, href) in enumerate(spine, start=1):
            chapter_path = resolve_href(opf_path, href)
            item_ref = f"{item_id}:{chapter_path}"
            if context.exclude_items and any(token in item_ref for token in context.exclude_items):
                context.diagnostics["forced_excluded_items"].append(item_ref)
                skipped.append({"href": chapter_path, "reason": "excluded_by_user"})
                continue
            if not chapter_path.lower().endswith((".xhtml", ".html", ".htm")):
                skipped.append({"href": chapter_path, "reason": "non_html_spine_item"})
                continue
            context.diagnostics["html_spine_item_count"] = int(context.diagnostics["html_spine_item_count"]) + 1
            chapter = extract_chapter(epub_zip, chapter_path, order, item_id, min_text_chars, context)
            if chapter is None:
                skipped.append({"href": chapter_path, "reason": "empty_text_after_parsing"})
                continue
            forced_include = bool(context.include_items) and any(token in item_ref for token in context.include_items)
            if forced_include:
                context.diagnostics["forced_included_items"].append(item_ref)
            if chapter.is_front_matter and chapter.chapter_label and len(chapter.text.strip()) <= 20:
                pending_chapter_label = chapter.chapter_label
                pending_chapter_number = chapter.chapter_number
            if chapter.is_front_matter and not keep_front_matter and not context.disable_front_matter_filter and not forced_include:
                skipped.append(
                    {
                        "href": chapter_path,
                        "reason": chapter.front_matter_reason or "classified_as_front_matter",
                    }
                )
                continue
            if pending_chapter_label and (not chapter.chapter_label or is_generic_numeric_label(chapter.chapter_label)):
                chapter.chapter_label = pending_chapter_label
                chapter.chapter_number = pending_chapter_number
                chapter_marker_pattern: re.Pattern[str] = LANGUAGE_RULES[context.language]["chapter_marker_pattern"]
                if chapter_marker_pattern.match(chapter.title):
                    chapter.title = pending_chapter_label
            pending_chapter_label = None
            pending_chapter_number = None
            chapters.append(chapter)
        return book_title, chapters, skipped


def validate_chapters(chapters: Iterable[Chapter], diagnostics: dict[str, object]) -> None:
    chapter_list = list(chapters)
    if not chapter_list:
        raise ExtractionFailure(
            "No readable chapter text was extracted from the EPUB. "
            "Do not analyze the book from prior knowledge.",
            diagnostics,
        )


def build_result(
    epub_path: Path,
    book_title: str | None,
    chapters: list[Chapter],
    skipped: list[dict[str, str]],
    preview_chars: int,
    min_text_chars: int,
    context: ExtractionContext,
) -> dict[str, object]:
    detected_title = book_title or epub_path.stem
    chapter_titles = [chapter.chapter_label or chapter.title for chapter in chapters]
    return {
        "source_file": str(epub_path),
        "book_title": detected_title,
        "chapter_count": len(chapters),
        "chapter_titles": chapter_titles,
        "min_text_chars": min_text_chars,
        "language": context.language,
        "language_source": context.language_source,
        "diagnostics": context.diagnostics,
        "skipped_items": skipped,
        "chapters": [chapter.to_dict(preview_chars=preview_chars) for chapter in chapters],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract chapter text from an EPUB file.")
    parser.add_argument("epub_path", type=Path, help="Path to the .epub file")
    parser.add_argument("--output", type=Path, help="Write JSON output to a file instead of stdout")
    parser.add_argument(
        "--language",
        choices=sorted(SUPPORTED_LANGUAGES),
        default=DEFAULT_LANGUAGE,
        help="Extraction language profile. Use auto to detect zh/en from chapter text.",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=160,
        help="Number of text characters to include in each chapter preview",
    )
    parser.add_argument(
        "--keep-front-matter",
        action="store_true",
        help="Keep cover/toc/preface-like sections instead of filtering them out",
    )
    parser.add_argument(
        "--min-text-chars",
        type=int,
        default=DEFAULT_MIN_TEXT_CHARS,
        help="Minimum text length to treat short pages as likely body text",
    )
    parser.add_argument(
        "--disable-frontmatter-filter",
        action="store_true",
        help="Keep items that would normally be filtered as cover/toc/preface-like sections",
    )
    parser.add_argument(
        "--include-item",
        action="append",
        default=[],
        help="Force-keep a spine item if this token appears in its item id or href; repeatable",
    )
    parser.add_argument(
        "--exclude-item",
        action="append",
        default=[],
        help="Force-skip a spine item if this token appears in its item id or href; repeatable",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.epub_path.exists():
        print(f"EPUB file not found: {args.epub_path}", file=sys.stderr)
        return 1
    context = build_context(
        requested_language=args.language,
        disable_front_matter_filter=args.disable_frontmatter_filter,
        include_items=args.include_item,
        exclude_items=args.exclude_item,
    )
    try:
        book_title, chapters, skipped = load_chapters(
            args.epub_path,
            args.keep_front_matter or args.disable_frontmatter_filter,
            args.min_text_chars,
            context,
        )
        validate_chapters(chapters, context.diagnostics)
    except ExtractionFailure as exc:  # pragma: no cover - CLI surface
        payload = json.dumps({"error": str(exc), "diagnostics": exc.diagnostics}, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        print(payload, file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - CLI surface
        print(str(exc), file=sys.stderr)
        return 1

    result = build_result(
        args.epub_path,
        book_title,
        chapters,
        skipped,
        args.preview_chars,
        args.min_text_chars,
        context,
    )
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
