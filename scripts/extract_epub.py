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
FRONT_MATTER_KEYWORDS = {
    "about",
    "acknowledgment",
    "acknowledgements",
    "acknowledgment",
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
}
CHAPTER_TITLE_PATTERNS = (
    re.compile(r"^第[0-9一二三四五六七八九十百千零〇两]+章$"),
    re.compile(r"^chapter\s+\d+$", re.IGNORECASE),
    re.compile(r"^\d+$"),
)


@dataclass
class Chapter:
    order: int
    item_id: str
    href: str
    title: str
    text: str
    is_front_matter: bool

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
            "word_count": len(self.text.split()),
        }


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


def looks_like_front_matter(title: str, href: str, text: str) -> bool:
    normalized_title = normalize_whitespace(title)
    if is_probable_chapter_title(normalized_title, text):
        return False
    haystacks = {
        normalized_title.lower(),
        Path(href).stem.lower(),
    }
    if any(keyword in hay for hay in haystacks for keyword in FRONT_MATTER_KEYWORDS):
        return True
    words = text.split()
    if len(words) < 40:
        short_text = " ".join(words[:20]).lower()
        if any(keyword in short_text for keyword in FRONT_MATTER_KEYWORDS):
            return True
    return False


def is_probable_chapter_title(title: str, text: str) -> bool:
    if not title:
        return False
    if any(pattern.match(title) for pattern in CHAPTER_TITLE_PATTERNS):
        return len(text.strip()) > 80
    return False


def extract_chapter(epub_zip: zipfile.ZipFile, chapter_path: str, order: int, item_id: str) -> Chapter | None:
    raw = epub_zip.read(chapter_path)
    parser = XHTMLTextExtractor()
    parser.feed(raw.decode("utf-8", errors="ignore"))
    text = parser.extracted_text()
    if not text:
        return None
    title = parser.headings[0] if parser.headings else chapter_title_from_href(chapter_path)
    return Chapter(
        order=order,
        item_id=item_id,
        href=chapter_path,
        title=title,
        text=text,
        is_front_matter=looks_like_front_matter(title, chapter_path, text),
    )


def load_chapters(epub_path: Path, keep_front_matter: bool) -> tuple[str | None, list[Chapter], list[str]]:
    with zipfile.ZipFile(epub_path) as epub_zip:
        opf_path = get_opf_path(epub_zip)
        book_title, spine = parse_package(epub_zip, opf_path)
        chapters: list[Chapter] = []
        skipped: list[str] = []
        for order, (item_id, href) in enumerate(spine, start=1):
            chapter_path = resolve_href(opf_path, href)
            if not chapter_path.lower().endswith((".xhtml", ".html", ".htm")):
                skipped.append(chapter_path)
                continue
            chapter = extract_chapter(epub_zip, chapter_path, order, item_id)
            if chapter is None:
                skipped.append(chapter_path)
                continue
            if chapter.is_front_matter and not keep_front_matter:
                skipped.append(chapter_path)
                continue
            chapters.append(chapter)
        return book_title, chapters, skipped


def validate_chapters(chapters: Iterable[Chapter]) -> None:
    chapter_list = list(chapters)
    if not chapter_list:
        raise ValueError(
            "No readable chapter text was extracted from the EPUB. "
            "Do not analyze the book from prior knowledge."
        )


def build_result(epub_path: Path, book_title: str | None, chapters: list[Chapter], skipped: list[str], preview_chars: int) -> dict[str, object]:
    detected_title = book_title or epub_path.stem
    return {
        "source_file": str(epub_path),
        "book_title": detected_title,
        "chapter_count": len(chapters),
        "skipped_items": skipped,
        "chapters": [chapter.to_dict(preview_chars=preview_chars) for chapter in chapters],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract chapter text from an EPUB file.")
    parser.add_argument("epub_path", type=Path, help="Path to the .epub file")
    parser.add_argument("--output", type=Path, help="Write JSON output to a file instead of stdout")
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
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.epub_path.exists():
        print(f"EPUB file not found: {args.epub_path}", file=sys.stderr)
        return 1
    try:
        book_title, chapters, skipped = load_chapters(args.epub_path, args.keep_front_matter)
        validate_chapters(chapters)
    except Exception as exc:  # pragma: no cover - CLI surface
        print(str(exc), file=sys.stderr)
        return 1

    result = build_result(args.epub_path, book_title, chapters, skipped, args.preview_chars)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
