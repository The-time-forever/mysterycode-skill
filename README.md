# Mystery Analysis Skill for Claude Code

Evidence-based mystery and detective fiction analysis for Claude Code. This repository packages a reusable skill, an EPUB extraction script, and Obsidian-oriented templates so users can go from raw book files to structured reading notes.

## Install

### Option 1: Clone and install locally

```bash
git clone https://github.com/<your-account>/mysterycode-skill.git
/plugin add /path/to/mysterycode-skill
```

### Option 2: Copy into the skills directory

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

- Extract readable chapter text from EPUB files before analysis
- Analyze chapters for details, anomalies, foreshadowing, and insights
- Check consistency across chapters and timelines
- Generate character and entity relationship notes
- Create Obsidian-compatible vault content with double-links and tags

## Quick Start

### Extract an EPUB

```bash
python scripts/extract_epub.py my-book.epub --output extracted.json
```

### Ask Claude to analyze and create a vault

```text
Analyze chapter 1 of this mystery novel using extracted.json and create an Obsidian vault in ./mystery-vault-book
```

## Skill Behavior

- EPUB analysis is intentionally two-step: extract first, analyze second.
- Extracted `notes` are reference context, not primary plot evidence.
- Vault output location is user-controlled; ask Claude to place it wherever you want.
- If EPUB extraction fails, the skill should stop and report the failure instead of guessing from prior knowledge.

## More Docs

- Chinese overview: `docs/README_CN.md`
- Usage guide: `docs/USAGE.md`
- Prompt rules: `docs/prompt.md`
- Project overview: `docs/PROJECT_OVERVIEW.md`
- Examples: `docs/examples.md`
- Changelog: `docs/CHANGELOG.md`

## License

MIT
