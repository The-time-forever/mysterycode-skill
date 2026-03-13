# Mystery Analysis Skill for Claude Code

A specialized skill for analyzing mystery novels and detective stories through structured investigation workflows. This skill enables evidence-based close reading, clue tracking, and narrative analysis.

## Overview

This skill brings systematic mystery analysis capabilities to Claude Code, allowing users to:
- Import and parse mystery text from multiple formats
- Perform structured analysis of clues, anomalies, and foreshadowing
- Check consistency across chapters
- Generate character relation graphs
- Create complete Obsidian vaults for knowledge management
- Export findings with double-links and tags

## Installation

### For Claude Code

1. Copy this skill folder to your Claude Code skills directory:
   ```bash
   cp -r mystery-analysis-skill ~/.claude/skills/
   ```

2. Restart Claude Code or reload skills:
   ```bash
   claude reload-skills
   ```

3. Verify installation:
   ```bash
   claude list-skills
   ```

## Usage

### Basic Analysis

```
User: "Analyze chapter 5 of my mystery novel for clues and foreshadowing"

Claude: [Invokes mystery analysis skill]
- Parses the chapter
- Extracts details, anomalies, foreshadowing, and insights
- Returns structured analysis with evidence
```

### Multi-Chapter Consistency Check

```
User: "Check chapters 3-7 for contradictions in the suspect's alibi"

Claude: [Invokes mystery analysis skill]
- Loads specified chapter range
- Compares statements and timelines
- Identifies inconsistencies
- Reports contradictions with chapter references
```

### Relation Graph Generation

```
User: "Generate a character relation graph for chapters 1-10"

Claude: [Invokes mystery analysis skill]
- Extracts character names and relationships
- Identifies interaction patterns
- Creates graph structure
- Returns visualization data
```

### Export to Obsidian

```
User: "Export my mystery analysis to Obsidian vault"

Claude: [Invokes mystery analysis skill]
- Asks for vault location
- Creates complete folder structure
- Generates book info, chapter analysis, character pages
- Uses [[double-links]] for all entities
- Adds tags and metadata
- Returns vault path for opening in Obsidian
```

### Create Obsidian Vault

```
User: "Create an Obsidian vault for analyzing this mystery novel"

Claude: [Invokes mystery analysis skill]
- Creates vault structure with Books/, Characters/, Analysis/ folders
- Generates Home.md index page
- Creates book information page
- Sets up templates for future analysis
- Ready to open in Obsidian
```

## Skill Triggers

The skill activates when users mention:
- "mystery analysis"
- "analyze detective story"
- "track clues"
- "check consistency"
- "foreshadowing analysis"
- "character relations"
- "mystery novel"

Or when working with mystery-related files:
- `.epub` files with mystery content that should be extracted first
- Text files containing detective stories
- PDF mystery novels

## Features

### Evidence-Based Analysis

All analysis is grounded in explicit text from selected chapters:
- Concrete details with context
- Suspicious elements with explanations
- Potential foreshadowing with reasoning
- Grounded insights tied to evidence

### Language Preservation

The skill maintains source language in output:
- Chinese source → Chinese analysis
- English source → English analysis
- No language drift during analysis

### Structured Output

Analysis follows a consistent format:
```json
{
  "details": ["Observable facts from text"],
  "anomalies": ["Suspicious or unusual elements"],
  "foreshadowing": ["Potential setup for later"],
  "insights": ["Grounded interpretations"],
  "summary": "Brief chapter overview",
  "entities": ["Characters, objects, locations"],
  "chapters": ["Chapter references"]
}
```

### Quality Standards

✓ Specific quotes or paraphrases
✓ Concrete details (names, times, places)
✓ Observable character behaviors
✓ Textual evidence for claims
✓ Source language preservation

✗ Generic plot summaries
✗ Speculation without support
✗ Prior knowledge of endings
✗ Language switching
✗ Solving the mystery for the reader

## Workflow

### Typical Investigation Session

1. **Import**: Load mystery text from file
   ```
   "Extract chapter text from mystery.epub, then show me the chapter structure"
   ```

2. **Review Structure**: Check chapter segmentation
   ```
   "Show me the chapter structure"
   ```

3. **Select Scope**: Choose chapters to analyze
   ```
   "Select chapters 5-8 for analysis"
   ```

4. **Analyze**: Run structured analysis
   ```
   "Analyze the selected chapters for clues"
   ```

5. **Check Consistency**: Detect contradictions
   ```
   "Check for inconsistencies in the timeline"
   ```

6. **Generate Graph**: Visualize relationships
   ```
   "Create a character relation graph"
   ```

7. **Export**: Save findings
   ```
   "Export analysis to Obsidian format"
   ```

## Configuration

### Supported Formats

- **Markdown** (`.md`): Plain text with markdown formatting
- **Text** (`.txt`): Plain text files
- **PDF** (`.pdf`): PDF documents
- **EPUB** (`.epub`): Use `python scripts/extract_epub.py <book>.epub --output extracted.json` before analysis

### EPUB Guardrail

- Do not treat a raw `.epub` file as already-read chapter text.
- Extract readable chapters first, then analyze only the extracted text.
- If extraction returns no readable chapters, stop and report the failure instead of answering from memory.

### Model Support

The skill works with multiple LLM providers:
- Claude (Anthropic)
- DeepSeek
- OpenAI GPT models
- Other compatible models

### Output Formats

- **JSON**: Structured analysis data
- **Markdown**: Human-readable notes
- **Obsidian**: Knowledge base integration
- **Graph Data**: Visualization formats

## Examples

See `examples.md` for detailed usage examples including:
- Basic mystery analysis
- Multi-chapter consistency checks
- Character relation graphs
- Chinese mystery novel analysis
- Obsidian export
- Foreshadowing tracking

## Philosophy

### Evidence-First Approach

The skill prioritizes observations over interpretations:
1. Details (what is explicitly present)
2. Anomalies (what seems unusual)
3. Foreshadowing (what might be setup)
4. Insights (grounded interpretations)

### Close Reading Focus

The tool amplifies close reading rather than replacing it:
- Surface details that make the mystery work
- Help readers notice patterns
- Track open questions
- Avoid solving the mystery

### Analysis Priority

The skill follows this analysis order:
1. Observations
2. Anomalies
3. Foreshadowing
4. Restrained insights

This ensures model output exposes evidence before offering interpretations.

## Limitations

### Current Constraints

- Very long chapters may be truncated
- EPUB front matter filtering is heuristic
- Graph generation can produce duplicate names
- Analysis requires strong grounding prompts

### Future Improvements

- Chunking strategy for long chapters
- Better EPUB front matter filtering
- Stronger evidence-gating
- Improved graph stability
- Multi-chapter summary synthesis

## Use Cases

### For Mystery Readers
- Track clues across long novels
- Identify patterns and connections
- Notice foreshadowing on first read
- Prepare for book club discussions

### For Writers
- Analyze mystery structure and pacing
- Study how authors plant clues
- Learn foreshadowing techniques
- Understand consistency requirements

### For Researchers
- Perform narrative analysis
- Study detective fiction conventions
- Analyze plot construction
- Compare mystery writing styles

## Technical Details

### Architecture

The skill provides structured analysis capabilities:
- **Core Engine**: Text parsing and analysis
- **Analysis Pipeline**: Multi-stage processing
- **Export System**: Multiple output formats including Obsidian vault
- **Integration Layer**: Claude Code compatibility

### Obsidian Vault Structure

When creating an Obsidian vault, the following structure is generated:

```
mystery-vault-[BookName]/
├── Books/              # Book analysis
│   └── [BookName]/
│       ├── 00-Book-Info.md
│       ├── 01-Chapter-1-Analysis.md
│       ├── 02-Chapter-2-Analysis.md
│       └── ...
├── Analysis/           # Cross-chapter analysis
│   ├── Clue-Tracking.md
│   ├── Consistency-Check.md
│   └── Foreshadowing-Summary.md
├── Characters/         # Character pages
│   ├── Character-A.md
│   ├── Character-B.md
│   └── ...
├── Templates/          # Template files
│   ├── Chapter-Analysis-Template.md
│   └── Character-Card-Template.md
└── Home.md            # Main index page
```

### Vault Features

- Double-Link System: Uses `[[Character]]` `[[Object]]` to connect all entities
- Tag Classification: `#mystery` `#chapter` `#character` tags
- Task Tracking: `- [ ]` for tracking unsolved mysteries
- Timeline: Records event chronology
- Relation Network: Character and entity connections

### Opening in Obsidian

1. Open Obsidian application
2. Select "Open folder as vault"
3. Choose the generated vault path
4. Start browsing and editing analysis notes

### Dependencies

- TypeScript
- Modern LLM APIs
- Text processing libraries
- Graph generation tools

## Contributing

To improve this skill:

1. Test with various mystery novels
2. Report issues with analysis quality
3. Suggest new analysis features
4. Contribute example analyses
5. Improve documentation

## License

MIT License

## Support

For issues or questions:
- Documentation: See `skill.md` for detailed capabilities
- Examples: See `examples.md` for usage patterns
