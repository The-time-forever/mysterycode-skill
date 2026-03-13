# MysteryCode Skill - 项目总览

##  项目结构

```
mysterycode-skill/
├── README.md                           # 英文完整说明
├── README_CN.md                        # 中文完整说明
├── USAGE.md                            # 详细使用指南
├── skill.md                            # 技能核心能力描述
├── skill.json                          # 技能元数据配置
├── prompt.md                           # 分析提示词和质量标准
├── examples.md                         # 详细使用示例
├── scripts/                            # 辅助脚本
│   └── extract_epub.py                 # EPUB 正文提取脚本
└── templates/                          # Obsidian 模板文件
    ├── chapter-analysis-template.md    # 章节分析模板
    ├── character-card-template.md      # 角色卡片模板
    └── clue-tracking-template.md       # 线索追踪模板
```

##  核心功能

### 1. 文本分析
- 支持多种格式 (Markdown, TXT, PDF, EPUB)
- EPUB 通过提取脚本先转换为可分析正文
- 自动章节识别和分段
- 结构化分析 (细节、异常、伏笔、洞察)

### 2. 一致性检查
- 跨章节矛盾检测
- 时间线验证
- 角色陈述对比

### 3. 关系图谱
- 角色关系可视化
- 实体连接分析
- 互动模式识别

### 4. Obsidian 集成 
- **自动创建完整 vault 仓库**
- 生成结构化笔记
- 双链系统连接所有实体
- 标签分类和待办追踪

##  快速开始

### 安装

```bash
# 复制到 Claude Code skills 目录
cp -r mysterycode-skill ~/.claude/skills/

# 验证安装
claude list-skills
```

### 基本使用

```
# 分析章节
"分析这个推理小说第 5 章的线索和伏笔"

# 创建 Obsidian vault
"为这本推理小说创建一个 Obsidian vault"

# 一致性检查
"检查第 3-7 章中嫌疑人不在场证明的矛盾"

# 生成关系图
"生成第 1-10 章的角色关系图"
```

##  文档说明

### README.md / README_CN.md
- 项目概述和功能介绍
- 安装和使用说明
- 技术细节和架构
- Obsidian vault 结构说明

### USAGE.md
- 详细的使用指南
- 完整的工作流程示例
- 最佳实践和技巧
- 故障排除

### skill.md
- 核心能力描述
- 分析维度说明
- 设计原则和哲学
- 质量标准

### prompt.md
- 分析提示词模板
- 质量标准和规范
- Obsidian vault 创建指令
- 边缘情况处理

### examples.md
- 详细的使用示例
- 完整的 vault 创建示例
- 各种分析场景演示
- 输出格式示例

### skill.json
- 技能元数据
- 触发条件
- 能力列表
- 工作流程定义

## 🗂️ 模板文件

### chapter-analysis-template.md
章节分析的标准模板,包含:
-  章节概要
-  关键细节
-  异常发现
-  伏笔识别
-  分析洞察
-  相关章节
-  实体提及
-  待解问题
-  时间线

### character-card-template.md
角色卡片的标准模板,包含:
- 基本信息
- 外貌特征
- 性格特点
- 出现章节
- 关键行为
- 可疑之处
- 关系网络
- 背景故事

### clue-tracking-template.md
线索追踪的标准模板,包含:
-  重要线索 (已确认)
-  待确认线索 (需验证)
-  已解决线索 (已解释)
-  线索关联
-  线索统计

## 🎨 Obsidian Vault 结构

创建的 vault 包含以下结构:

```
mystery-vault-[书名]/
├──  Books/              # 书籍分析
│   └── [书名]/
│       ├── 00-书籍信息.md
│       ├── 01-第一章分析.md
│       └── ...
├──  Analysis/           # 跨章节分析
│   ├── 线索追踪.md
│   ├── 一致性检查.md
│   └── 伏笔汇总.md
├──  Characters/         # 角色卡片
│   ├── 角色A.md
│   └── 角色B.md
├──  Templates/          # 模板文件
│   ├── 章节分析模板.md
│   └── 角色卡片模板.md
└──  Home.md            # 主索引页
```

##  特色功能

### 1. 证据优先
所有分析必须基于文本中的明确证据,避免推测。

### 2. 语言保持
自动匹配源文本语言,中文源文本生成中文分析。

### 3. 细读增强
帮助读者注意容易忽略的细节,不替代阅读体验。

### 4. 双链系统
使用 `[[]]` 连接所有实体,构建知识网络。

### 5. 待办追踪
使用 `- [ ]` 追踪未解之谜和待确认信息。

##  使用场景

### 推理小说读者
- 追踪长篇小说中的线索
- 识别模式和联系
- 首次阅读时注意伏笔
- 准备读书会讨论

### 作家
- 分析推理小说的结构和节奏
- 学习如何埋设线索
- 研究伏笔技巧
- 理解一致性要求

### 研究者
- 进行叙事分析
- 研究侦探小说惯例
- 分析情节构建
- 比较推理写作风格

##  技术特点

- 支持多种 LLM 模型 (Claude, DeepSeek, OpenAI GPT)
- 结构化 JSON 输出
- 长文本处理能力
- Markdown 和 Obsidian 格式导出
- 图谱可视化数据生成

##  推荐阅读顺序

1. **README_CN.md** - 了解项目概述
2. **USAGE.md** - 学习如何使用
3. **examples.md** - 查看实际示例
4. **prompt.md** - 理解分析原理
5. **templates/** - 查看模板文件

##  贡献指南

欢迎贡献:
- 测试不同类型的推理小说
- 报告分析质量问题
- 建议新的分析功能
- 贡献示例分析
- 改进文档

##  版本信息

- **版本**: 1.0.0
- **状态**: 稳定版
- **最后更新**: 2026-03-11

##  许可证

MIT License

##  相关资源

- [Claude Code 文档](https://docs.anthropic.com)
- [Obsidian 官方文档](https://help.obsidian.md/)
- [推理小说分析方法](https://example.com)

---

**开始使用**: 阅读 `USAGE.md` 获取详细的使用指南

**快速示例**: 查看 `examples.md` 了解实际使用场景

**技能配置**: 查看 `skill.json` 了解触发条件

祝你阅读愉快,享受推理的乐趣! 
