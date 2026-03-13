# MysteryCode Skill Usage Examples

## Example 1: Basic Mystery Analysis

### User Request
"I'm reading a detective novel and want to analyze chapter 5 for clues and foreshadowing."

### Skill Response
The skill would:
1. Ask for the text source (file path or direct text)
2. Parse the chapter structure
3. Perform structured analysis focusing on:
   - Concrete details from the chapter
   - Suspicious or unusual elements
   - Potential foreshadowing
   - Grounded insights

### Sample Output
```json
{
  "details": [
    "Inspector Chen arrived at the crime scene at 9:15 AM, noting the front door was unlocked",
    "The victim's coffee cup was still warm, suggesting recent activity",
    "A torn photograph was found under the desk, showing only half a face"
  ],
  "anomalies": [
    "The victim's phone was missing, but the charger was still plugged in",
    "Neighbor claimed to hear arguing at 8 AM, but victim lived alone",
    "The torn photograph appears to be deliberately hidden, not accidentally dropped"
  ],
  "foreshadowing": [
    "The inspector paused at the bookshelf, noting a gap where a book should be",
    "The torn photograph's visible half shows a distinctive ring on the person's hand",
    "The coffee cup brand matches the one mentioned in Chapter 2's cafe scene"
  ],
  "insights": [
    "The missing phone and warm coffee suggest the victim was interrupted suddenly",
    "The torn photograph may connect to the mysterious visitor mentioned earlier",
    "The timeline discrepancy between the neighbor's account and physical evidence needs investigation"
  ],
  "summary": "Inspector Chen investigates a crime scene with several suspicious elements, including a missing phone, a torn photograph, and conflicting witness testimony.",
  "entities": ["Inspector Chen", "victim", "neighbor", "torn photograph", "coffee cup", "phone"],
  "chapters": ["Chapter 5"]
}
```

## Example 2: Multi-Chapter Consistency Check

### User Request
"Check chapters 3-7 for any contradictions or inconsistencies in the suspect's alibi."

### Skill Response
The skill would:
1. Load chapters 3-7
2. Extract all statements related to the suspect's whereabouts
3. Compare timelines and claims
4. Identify contradictions

### Sample Output
```
Consistency Check Results:

CONTRADICTION FOUND:
- Chapter 3: Suspect claims to be at home alone from 7-10 PM
- Chapter 5: Security footage shows suspect's car leaving apartment at 8:30 PM
- Chapter 7: Suspect revises statement, now claims to have gone for a drive at 8:30 PM

TIMELINE INCONSISTENCY:
- Chapter 4: Witness sees suspect at restaurant at 9 PM
- Chapter 6: Restaurant receipt shows payment at 8:45 PM
- Issue: 15-minute discrepancy between witness account and physical evidence

UNRESOLVED TENSION:
- Chapter 3: Suspect mentions meeting "an old friend"
- Chapters 4-7: This friend is never identified or mentioned again
- Question: Who is this friend, and why hasn't the detective followed up?
```

## Example 3: Character Relation Graph

### User Request
"Generate a relation graph for all characters in chapters 1-10."

### Skill Response
The skill would:
1. Extract all character names
2. Identify relationships and interactions
3. Generate graph data structure

### Sample Output
```
Character Relation Graph:

NODES:
- Detective Sarah Miller (protagonist)
- Dr. James Chen (victim)
- Lisa Chen (victim's wife)
- Mark Thompson (business partner)
- Rachel Kim (assistant)

EDGES:
- Sarah Miller → Dr. James Chen [investigating]
- Lisa Chen → Dr. James Chen [married to]
- Mark Thompson → Dr. James Chen [business partner]
- Rachel Kim → Dr. James Chen [worked for]
- Mark Thompson → Lisa Chen [frequent contact, suspicious]
- Rachel Kim → Mark Thompson [former relationship, mentioned in Ch. 4]

INTERACTION PATTERNS:
- High frequency: Sarah Miller ↔ Lisa Chen (5 scenes)
- Suspicious: Mark Thompson ↔ Lisa Chen (3 private meetings)
- Avoided: Rachel Kim avoids Mark Thompson (noted in Ch. 7)
```

## Example 4: Chinese Mystery Novel Analysis

### User Request (Chinese)
"分析《白夜行》第一章的线索和伏笔"

### Skill Response (Chinese)
```json
{
  "details": [
    "1973年大阪的废弃建筑中发现一具男尸",
    "死者是当铺老板桐原洋介,死于钝器打击",
    "现场没有打斗痕迹,死者似乎认识凶手",
    "死者的儿子桐原亮司11岁,性格内向"
  ],
  "anomalies": [
    "死者身上没有钱包,但现场没有被翻动的痕迹",
    "案发时间推测为晚上8点,但没有人听到声响",
    "死者的妻子对丈夫的行踪表现得异常冷淡",
    "儿子亮司对父亲的死亡反应过于平静"
  ],
  "foreshadowing": [
    "亮司在学校图书馆借阅了大量推理小说",
    "废弃建筑附近有一家小卖部,老板娘的女儿雪穗经常出现",
    "警察注意到亮司手上有不寻常的伤痕",
    "死者生前经常深夜外出,去向不明"
  ],
  "insights": [
    "案件可能是熟人作案,现场的平静暗示死者对凶手没有防备",
    "亮司的冷静反应和手上的伤痕值得关注",
    "废弃建筑的选择可能不是随机的,可能与死者的秘密活动有关",
    "妻子的冷淡态度暗示家庭关系存在问题"
  ],
  "summary": "第一章描述了1973年大阪当铺老板桐原洋介在废弃建筑中被杀的案件,重点刻画了死者儿子亮司的异常反应和案件的诸多疑点。",
  "entities": ["桐原洋介", "桐原亮司", "废弃建筑", "当铺", "雪穗", "小卖部"],
  "chapters": ["第一章"]
}
```

## Example 5: Create Complete Obsidian Vault

### User Request
"Create an Obsidian vault for my mystery novel analysis."

### Skill Response
The skill would:
1. Ask for vault location (e.g., `./mystery-vault-detective-story`)
2. Create complete folder structure
3. Generate all necessary files

### Generated Vault Structure

```
mystery-vault-detective-story/
├──  Books/
│   └── Detective Story/
│       ├── 00-Book-Info.md
│       └── 01-Chapter-1-Analysis.md
├──  Analysis/
│   └── Clue-Tracking.md
├──  Characters/
│   ├── Inspector-Chen.md
│   └── Victim.md
├──  Templates/
│   └── Chapter-Analysis-Template.md
└──  Home.md
```

### Sample File: Home.md

```markdown
# Mystery Investigation Vault

##  Current Books
- [[Books/Detective Story/00-Book-Info|Detective Story]]

##  Recent Analysis
- [[Books/Detective Story/01-Chapter-1-Analysis|Chapter 1 Analysis]]

##  Quick Links
- [[Templates/Chapter-Analysis-Template|Chapter Analysis Template]]
- [[Analysis/Clue-Tracking|Clue Tracking]]

##  Statistics
- Books: 1
- Chapters Analyzed: 1
- Characters: 2
- Open Questions: 3

---
Created: 2026-03-11
Last Updated: 2026-03-11
```

### Sample File: Books/Detective Story/00-Book-Info.md

```markdown
# Detective Story

## 基本信息
- 作者: Unknown Author
- 类型: 推理小说
- 分析开始日期: 2026-03-11
- 当前进度: Chapter 1

## 章节列表
- [[01-Chapter-1-Analysis|Chapter 1: The Crime Scene]]
- [ ] Chapter 2
- [ ] Chapter 3

## 主要角色
- [[Characters/Inspector-Chen|Inspector Chen]] - 侦探
- [[Characters/Victim|Victim]] - 受害者

## 关键线索
- [ ] Missing phone
- [ ] Torn photograph
- [ ] Warm coffee cup
- [ ] Unlocked front door

## 未解之谜
- [ ] Who was the victim arguing with at 8 AM?
- [ ] Where is the missing phone?
- [ ] What book is missing from the shelf?

---
Tags: #mystery #book #detective-story
Created: 2026-03-11
```

### Sample File: Books/Detective Story/01-Chapter-1-Analysis.md

```markdown
# Chapter 1: The Crime Scene

##  章节概要
Inspector Chen arrives at a crime scene where a victim was found in their apartment. The front door was unlocked, and several suspicious elements suggest foul play. The investigation begins with conflicting witness testimony and missing evidence.

##  关键细节
- [[Inspector Chen]] arrived at crime scene at 9:15 AM
- Front door was unlocked when police arrived
- [[Victim]]'s phone was missing from the scene
- [[Coffee Cup]] on desk was still warm to touch
- [[Torn Photograph]] found under the desk, showing only half a face
- Distinctive ring visible on the hand in the photograph
- Gap on bookshelf where a book should be

##  异常发现
- Phone missing but charger still plugged in → suggests sudden interruption
- [[Neighbor]] claimed to hear arguing at 8 AM → but victim lived alone
- Torn photograph appears deliberately hidden, not accidentally dropped
- Coffee cup brand matches the cafe mentioned in earlier context
- No signs of forced entry despite unlocked door

##  伏笔识别
- Inspector paused at the bookshelf, noting the gap → missing book may be significant
- Ring visible in torn photograph → may help identify the other person
- Warm coffee suggests victim was active shortly before death
- Unlocked door implies victim knew the visitor

##  分析洞察
- Missing phone and warm coffee suggest victim was interrupted suddenly
- Torn photograph may connect to a relationship the victim was hiding
- Timeline discrepancy between neighbor's account (8 AM arguing) and physical evidence needs investigation
- Unlocked door + no forced entry = victim likely let the killer in

##  相关章节
- Next: [[02-Chapter-2-Analysis|Chapter 2]]

##  实体提及
**Characters:**
- [[Characters/Inspector-Chen|Inspector Chen]] - Lead investigator
- [[Characters/Victim|Victim]] - Deceased
- [[Characters/Neighbor|Neighbor]] - Witness (unreliable?)

**Objects:**
- [[Coffee Cup]]
- [[Torn Photograph]]
- [[Missing Phone]]
- [[Missing Book]]

**Locations:**
- [[Victim's Apartment]]
- [[Crime Scene]]

##  待解问题
- [ ] Who was the victim arguing with at 8 AM?
- [ ] Where is the missing phone?
- [ ] What book is missing from the shelf?
- [ ] Who is in the torn photograph?
- [ ] Why was the door unlocked?

##  时间线
- 8:00 AM - Neighbor claims to hear arguing
- 8:30 AM - Estimated time of death (coroner)
- 9:15 AM - Inspector Chen arrives at scene
- 9:45 AM - Torn photograph discovered under desk

---
Tags: #chapter #analysis #detective-story #crime-scene
Created: 2026-03-11
Previous: [[00-Book-Info|Book Info]]
Next: [[02-Chapter-2-Analysis|Chapter 2]]
```

### Sample File: Characters/Inspector-Chen.md

```markdown
# Inspector Chen

## 基本信息
- 首次出现: [[Books/Detective Story/01-Chapter-1-Analysis|Chapter 1]]
- 角色类型: 主角 / 侦探
- 职业: Police Inspector

## 出现章节
- [[Books/Detective Story/01-Chapter-1-Analysis|Chapter 1]] - Arrived at crime scene, began investigation

## 关键行为
- Arrived at crime scene at 9:15 AM
- Noted the unlocked front door
- Observed the warm coffee cup
- Paused at the bookshelf, noticing a gap
- Discovered the torn photograph

## 观察能力
- Detail-oriented (noticed missing book)
- Methodical approach to crime scene
- Questions physical evidence vs witness testimony

## 关系网络
- Investigating [[Characters/Victim|Victim]]'s death
- Interviewing [[Characters/Neighbor|Neighbor]]

## 调查进展
- [ ] Identify person in torn photograph
- [ ] Locate missing phone
- [ ] Verify neighbor's alibi
- [ ] Find missing book

---
Tags: #character #detective #protagonist #detective-story
```

### Vault Completion Message

```
 Obsidian Vault Created Successfully!

Location: ./mystery-vault-detective-story/

Structure:
-  Books/Detective Story/ (2 files)
-  Characters/ (2 files)
-  Analysis/ (1 file)
-  Templates/ (1 file)
-  Home.md

Total Files: 7

To open in Obsidian:
1. Launch Obsidian
2. Click "Open folder as vault"
3. Select: ./mystery-vault-detective-story/
4. Start exploring your mystery analysis!
```

## Example 6: Handling Insufficient Text

### User Request
"Analyze chapter 10."

### Skill Response (if chapter 10 is just a title)
```
Analysis Status: INSUFFICIENT TEXT

The selected chapter (Chapter 10) contains only structural content:
- Chapter title: "第十章"
- No narrative text found

This appears to be a chapter header or title page without actual story content.

Recommendation:
- Check if the chapter segmentation is correct
- Try selecting the next chapter (Chapter 11)
- Review the chapter list with /chapters command to verify structure

Cannot perform analysis without narrative text. Analysis requires actual story content with dialogue, descriptions, and character interactions.
```

## Example 7: Foreshadowing Tracking Across Chapters

### User Request
"Track all mentions of the 'red scarf' across chapters 1-15 and analyze its significance."

### Skill Response
```
Foreshadowing Analysis: Red Scarf

CHAPTER 1:
- First mention: "A red scarf hung on the coat rack, out of place in the summer heat"
- Context: Detective's initial visit to victim's apartment
- Significance: Emphasized as unusual for the season

CHAPTER 4:
- Second mention: "The witness recalled seeing someone in a red scarf near the scene"
- Context: Witness testimony
- Significance: Potential connection to suspect

CHAPTER 7:
- Third mention: "Among the victim's belongings, no red scarf was found"
- Context: Evidence inventory
- Significance: Scarf from Chapter 1 has disappeared

CHAPTER 12:
- Fourth mention: "The suspect's alibi witness wore a red scarf during the interview"
- Context: Alibi verification
- Significance: Possible callback to earlier mentions

CHAPTER 15:
- Fifth mention: "The red scarf was found in the suspect's car trunk, with traces of the victim's DNA"
- Context: Search warrant execution
- Significance: Key evidence linking suspect to crime

PATTERN ANALYSIS:
- The red scarf appears 5 times across 15 chapters
- Each mention escalates its significance
- Initial "out of place" detail becomes crucial physical evidence
- The scarf's disappearance in Chapter 7 creates tension
- Final discovery in Chapter 15 resolves the mystery

FORESHADOWING EFFECTIVENESS:
- Strong: The initial emphasis on the scarf being "out of place" signals importance
- The disappearance creates a mystery within the mystery
- The callback in Chapter 12 maintains reader attention
- The payoff in Chapter 15 feels earned, not contrived
```

## Integration with Claude Code

These examples can be triggered in Claude Code by:

1. Direct skill invocation:
   ```
   /mysterycode analyze chapter 5
   ```

2. Natural language request:
   ```
   "I need to analyze this mystery novel chapter for clues"
   ```

3. File-based analysis:
   ```
   "Analyze the mystery novel in mystery.epub, chapters 3-7"
   ```

The skill maintains structured output and evidence-based reasoning across all use cases.
