# Mystery Analysis Skill for Claude Code

Evidence-based mystery and detective fiction analysis for Claude Code. This repository packages a reusable skill, EPUB extraction helpers, and Obsidian-oriented templates so a user can ask the agent to read a book, analyze chapters, and build an Obsidian vault.

## Install

Clone this repository and add it as a local plugin:

```bash
git clone https://github.com/The-time-forever/mysterycode-skill.git
/plugin add /path/to/mysterycode-skill
```

If you prefer, you can also copy the folder into the Claude skills directory:

```bash
cp -r mysterycode-skill ~/.claude/skills/
```

On Windows, copy the folder to `C:\Users\<you>\.claude\skills\`.

### Verify

```bash
claude list-skills
```

Look for `mystery-analysis`.

## Repository Layout

```text
mysterycode-skill/
├── SKILL.md
├── skill.json
├── scripts/
│   └── extract_epub.py
├── templates/
│   ├── chapter-analysis-template.md
│   ├── character-card-template.md
│   ├── location-card-template.md
│   ├── object-card-template.md
│   ├── timeline-note-template.md
│   └── clue-tracking-template.md
└── docs/
    ├── README_CN.md
    ├── USAGE.md
    ├── prompt.md
    ├── examples.md
    ├── PROJECT_OVERVIEW.md
    └── CHANGELOG.md
```

## What It Does

- Read mystery novels from extracted EPUB text and other text formats
- Analyze chapters for details, anomalies, foreshadowing, and insights
- Check consistency across chapters and timelines
- Generate character and entity relationship notes
- Create Obsidian-compatible vault content with double-links, tags, and structured folders
- Organize vault entities into dedicated folders for characters, locations, objects, and timeline notes

## Quick Start

You do not need to run the Python scripts manually in normal use. The agent should call them when needed.

Typical prompts:

```text
Read this EPUB, analyze chapter 1, and create an Obsidian vault in ./mystery-vault-book

Continue analyzing chapter 2 and update the existing Obsidian vault

Check this mystery vault for missing links, empty pages, and stale indexes
```

## Skill Behavior

- EPUB analysis is intentionally two-step: the agent extracts first, then analyzes.
- EPUB extraction now supports `zh` and `en` profiles plus `--language auto`.
- Extracted `notes` are reference context, not primary plot evidence.
- Vault output location is user-controlled; ask Claude to place it wherever you want.
- If EPUB extraction fails, the skill should stop and report the failure instead of guessing from prior knowledge.
- On extraction failure, use the returned diagnostics with controlled retries such as `--language`, `--include-item`, `--exclude-item`, or `--disable-frontmatter-filter`.
- Chapter writes should be followed by vault synchronization: update book info, clue tracking, recent-analysis links, and minimal entity pages.
- Use `scripts/validate_vault.py` to catch empty pages, missing link targets, stale indexes, and broken chapter navigation.

## Obsidian Output

This skill is designed to produce and maintain an Obsidian vault, not just one-off chapter summaries.

Typical vault output includes:
- `Books/[书名]/` chapter analysis notes
- `Analysis/` cross-chapter clue tracking
- `Characters/`, `Locations/`, and `Objects/` entity pages
- `Timeline/` time-order notes
- `Home.md` as the vault entry page

## More Docs

- Chinese overview: `docs/README_CN.md`
- Usage guide: `docs/USAGE.md`
- Prompt rules: `docs/prompt.md`
- Project overview: `docs/PROJECT_OVERVIEW.md`
- Examples: `docs/examples.md`
- Changelog: `docs/CHANGELOG.md`

## License

MIT
