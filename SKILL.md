---
name: mystery-analysis
description: Analyze mystery novels and detective stories with evidence-based close reading workflows. Use when Claude needs to extract EPUB text, analyze chapters for clues, anomalies, foreshadowing, and insights, check consistency across chapters, or generate Obsidian vault notes for mystery and detective fiction.
---

# MysteryCode Analysis Skill

A specialized skill for analyzing mystery novels and detective stories using structured investigation workflows. This skill helps readers perform close reading, track clues, identify foreshadowing, and detect inconsistencies in narrative text.

## Core Capabilities

### Text Import and Processing
- Import mystery text from multiple formats (markdown, plain text, PDF, EPUB)
- Extract readable chapter text from EPUB files with `scripts/extract_epub.py` before analysis
- Parse and segment text into chapters
- Handle multi-language content (English, Chinese, etc.)
- Preserve full chapter text for detailed analysis

### Structured Analysis
The skill performs evidence-based analysis focusing on:

1. **Details**: Concrete observations from the text
   - Recurring names, objects, places, actions
   - Specific dialogue and character reactions
   - Temporal and spatial markers

2. **Anomalies**: Suspicious or unusual elements
   - Unusual reactions or behaviors
   - Suspicious omissions or evasions
   - Contradictions or inconsistencies
   - Out-of-place details

3. **Foreshadowing**: Potential setup for future reveals
   - Emphasized details that seem significant
   - Callbacks to earlier events
   - Symbolic or metaphorical elements
   - Unresolved questions

4. **Insights**: Grounded interpretations
   - Patterns across multiple observations
   - Possible connections between clues
   - Restrained speculation tied to evidence

### Investigation Workflow
- **Chapter Selection**: Choose specific chapter ranges for focused analysis
- **Consistency Checking**: Detect contradictions and weak links across chapters
- **Relation Graphs**: Visualize character relationships and entity connections
- **Export**: Generate Obsidian-compatible notes for external knowledge management

## Analysis Philosophy

### Evidence-First Approach
- All analysis must be grounded in explicit text from selected chapters
- Avoid speculation based on prior knowledge of the story
- Prioritize observations over interpretations
- Include source evidence for important claims
- When EPUB extraction provides `notes`, use them only as labeled reference context, not as primary plot evidence

### Language Preservation
- Maintain the source language in analysis output
- If source is Chinese, output should be Chinese
- Avoid language drift during analysis

### Close Reading Focus
The tool amplifies close reading rather than replacing it. It should:
- Surface details that make the mystery work
- Help readers notice patterns they might miss
- Track open questions worth following
- Avoid "solving" the mystery for the reader

## Typical Investigation Session

```
1. Import source text
2. If the source is EPUB, run `python scripts/extract_epub.py <book>.epub --output extracted.json`
3. Review extracted chapter structure and previews
4. Select investigation scope (single chapter or range)
5. Run structured analysis on extracted text only
6. Check for consistency issues
7. Inspect relation graphs
8. Export findings to notes
```

## EPUB Workflow Guardrail

- Never claim to have read an EPUB directly unless chapter text has been extracted first.
- For `.epub` inputs, use `scripts/extract_epub.py` and inspect the extracted chapter previews before analysis.
- If extraction fails or produces no readable chapters, stop and report that the source text is unavailable.
- Do not infer plot content from the file name, title, metadata, or prior knowledge.

## Supporting Resources

- `docs/prompt.md`: prompt rules, EPUB note handling, and Obsidian output expectations
- `docs/USAGE.md`: user-facing examples and workflow walkthroughs
- `docs/examples.md`: longer scenario examples
- `templates/`: chapter, character, and clue-tracking templates
- `scripts/extract_epub.py`: EPUB extraction script used before narrative analysis
