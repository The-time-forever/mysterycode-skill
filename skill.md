# MysteryCode Analysis Skill

A specialized skill for analyzing mystery novels and detective stories using structured investigation workflows. This skill helps readers perform close reading, track clues, identify foreshadowing, and detect inconsistencies in narrative text.

## Core Capabilities

### Text Import and Processing
- Import mystery text from multiple formats (markdown, plain text, PDF, EPUB)
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
2. Review chapter structure
3. Select investigation scope (single chapter or range)
4. Run structured analysis
5. Check for consistency issues
6. Inspect relation graphs
7. Export findings to notes
```

## Output Structure

### Analysis Output
```
{
  "details": [
    "Concrete observation with context"
  ],
  "anomalies": [
    "Suspicious element with explanation"
  ],
  "foreshadowing": [
    "Potential setup with reasoning"
  ],
  "insights": [
    "Grounded interpretation tied to evidence"
  ],
  "summary": "Brief overview of chapter content",
  "entities": ["Character names", "Key objects", "Locations"],
  "chapters": ["Chapter references"]
}
```

### Consistency Check Output
- Contradictions between chapters
- Unresolved tensions
- Potential callbacks
- Timeline inconsistencies

### Relation Graph Output
- Character relationships
- Entity connections
- Interaction patterns
- Network visualization data

## Quality Standards

### What to Include
- Specific quotes or paraphrases from the text
- Concrete details (names, times, places, actions)
- Observable character behaviors
- Explicit dialogue and reactions
- Textual evidence for each claim

### What to Avoid
- Generic plot summaries
- Speculation without textual support
- Prior knowledge of the story's ending
- Broad interpretations without evidence
- Language switching (maintain source language)

## Use Cases

### For Mystery Readers
- Track clues across long novels
- Identify patterns and connections
- Notice foreshadowing on first read
- Prepare for book club discussions

### For Writers
- Analyze mystery structure and pacing
- Study how published authors plant clues
- Learn foreshadowing techniques
- Understand consistency requirements

### For Researchers
- Perform narrative analysis
- Study detective fiction conventions
- Analyze plot construction
- Compare mystery writing styles

## Technical Notes

### Supported Formats
- Markdown (.md)
- Plain text (.txt)
- PDF (.pdf)
- EPUB (.epub)

### Chapter Segmentation
- Automatic chapter detection
- Manual chapter boundary adjustment
- Preview before analysis
- Handle front matter and structural content

### Model Requirements
- Supports multiple LLM providers
- Works with DeepSeek, Claude, and other models
- Structured output generation
- Long-context handling for full chapters

## Limitations and Known Issues

### Current Constraints
- Chapter truncation may occur for very long chapters
- EPUB segmentation may include front matter as chapters
- Graph generation can produce duplicate node names
- Analysis may drift without strong grounding prompts

### Future Improvements
- Chunking strategy for long chapters
- Better EPUB front matter filtering
- Stronger evidence-gating in prompts
- Improved graph stability
- Multi-chapter summary synthesis

## Integration with Claude Code

This skill can be invoked through Claude Code to:
- Analyze mystery novels during reading
- Generate investigation notes
- Export findings to knowledge bases
- Support creative writing projects
- Assist with literary analysis tasks

The skill maintains the command-first interaction model and structured output format that makes MysteryCode effective for systematic investigation workflows.
