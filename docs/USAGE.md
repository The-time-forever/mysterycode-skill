# MysteryCode Skill 使用指南

## 快速开始

### 1. 安装 Skill

将此 skill 文件夹复制到 Claude Code 的 skills 目录:

```bash
# Linux/Mac
cp -r mysterycode-skill ~/.claude/skills/

# Windows
# 手动复制到 C:\Users\[用户名]\.claude\skills\
```

### 2. 验证安装

```bash
claude list-skills
```

应该能看到 `mystery-analysis` skill 出现在列表中。

## 基本使用

### 先处理 EPUB

如果源文件是 `.epub`，先运行：

```bash
python scripts/extract_epub.py <文件>.epub --output extracted.json
```

然后基于 `extracted.json` 中的章节文本做分析。不要在没有提取出正文时直接分析书名或文件本身。

中英场景推荐:

```bash
python scripts/extract_epub.py <文件>.epub --language auto --output extracted.json
```

如果提取失败或结构明显不对,按受控方式重试:

```bash
python scripts/extract_epub.py <文件>.epub --language en --disable-frontmatter-filter --output extracted.json
python scripts/extract_epub.py <文件>.epub --include-item chapter --exclude-item cover --output extracted.json
```

这些参数的作用是:
- `--language auto|zh|en`：选择语言规则
- `--disable-frontmatter-filter`：先别过滤前言/目录/短页,适合误杀正文时使用
- `--include-item`：强制保留某个 spine 项
- `--exclude-item`：强制排除明显噪音页

### 分析单个章节

```
用户: "分析这个推理小说第 5 章的线索和伏笔"

Claude 会:
1. 读取第 5 章内容
2. 提取细节、异常、伏笔和洞察
3. 返回结构化分析结果
```

### 分析多个章节

```
用户: "分析第 3-7 章,检查嫌疑人不在场证明的矛盾"

Claude 会:
1. 加载第 3-7 章
2. 比较陈述和时间线
3. 识别不一致之处
4. 报告矛盾点及章节引用
```

### 生成关系图谱

```
用户: "生成第 1-10 章的角色关系图"

Claude 会:
1. 提取所有角色名称
2. 识别角色间的关系
3. 创建关系图谱数据
4. 返回可视化结构
```

## 创建 Obsidian Vault

### 方式 1: 完整 Vault 创建

```
用户: "为这本推理小说创建一个 Obsidian vault"

Claude 会询问:
- Vault 创建位置 (例如: ./mystery-vault-书名)
- 书籍基本信息 (书名、作者等)

然后自动创建:
- 完整的文件夹结构
- Home.md 主页
- 书籍信息页
- 分析模板
```

### 方式 2: 导出现有分析

```
用户: "将第 1-5 章的分析导出到 Obsidian"

Claude 会:
- 询问 vault 位置
- 生成章节分析文件
- 创建角色卡片
- 使用双链连接所有实体
```

## Vault 结构说明

创建的 vault 包含以下结构:

```
mystery-vault-[书名]/
├──  Books/              # 书籍分析
│   └── [书名]/
│       ├── 00-书籍信息.md      # 书籍概览
│       ├── 01-第一章分析.md    # 章节分析
│       └── ...
├──  Analysis/           # 跨章节分析
│   ├── 线索追踪.md            # 线索汇总
│   ├── 一致性检查.md          # 矛盾检查
│   └── 伏笔汇总.md            # 伏笔追踪
├──  Characters/         # 角色卡片
│   ├── 角色A.md
│   └── 角色B.md
├──  Locations/          # 地点卡片
│   ├── 地点A.md
│   └── 地点B.md
├──  Objects/            # 物品与证物卡片
│   ├── 物品A.md
│   └── 物品B.md
├──  Timeline/           # 时间线与流转记录
│   └── 主时间线.md
├──  Templates/          # 模板
│   ├── 章节分析模板.md
│   ├── 角色卡片模板.md
│   ├── 地点卡片模板.md
│   ├── 物品卡片模板.md
│   └── 时间线模板.md
└──  Home.md            # 主索引页
```

## 文件内容示例

### 章节分析文件

每个章节分析包含:
-  章节概要
-  关键细节 (使用 [[双链]] 标记实体)
-  异常发现
-  伏笔识别
-  分析洞察
-  相关章节链接
-  实体提及列表
-  待解问题 (使用 `- [ ]` 待办)
-  时间线

### 角色卡片

每个角色卡片包含:
- 基本信息 (首次出现、角色类型)
- 出现章节列表
- 关键行为记录
- 可疑之处
- 关系网络
- 相关标签

### 地点 / 物品 / 时间页

建议不要把地点和物品散落在 vault 根目录,而是分别写进:
- `Locations/` - 案发地、住处、学校、商铺、街区
- `Objects/` - 证物、礼物、工具、可追踪物件
- `Timeline/` - 主时间线、人物时间线、物品流转

这样做的好处:
- 目录更干净
- 双链更容易查找
- 同名实体不容易混淆

### 线索追踪

跨章节线索追踪包含:
-  重要线索 (已确认)
-  待确认线索 (需验证)
-  已解决线索 (已解释)
- 章节引用和双链

## 在 Obsidian 中打开

### 步骤 1: 打开 Obsidian

启动 Obsidian 应用程序

### 步骤 2: 打开 Vault

1. 点击左侧的 "打开其他仓库" 或 "Open another vault"
2. 选择 "打开文件夹作为仓库" 或 "Open folder as vault"
3. 浏览到生成的 vault 路径
4. 点击 "打开" 或 "Open"

### 步骤 3: 开始使用

- 从 `Home.md` 开始浏览
- 点击 `[[双链]]` 在笔记间跳转
- 使用标签 `#mystery` `#chapter` 等过滤内容
- 使用图谱视图查看关系网络

## 高级功能

### 一致性检查

```
用户: "检查第 1-10 章中所有角色的不在场证明是否一致"

Claude 会:
- 提取所有时间线信息
- 比较不同章节的陈述
- 识别矛盾和不一致
- 生成一致性检查报告
```

### 伏笔追踪

```
用户: "追踪'红色围巾'在全书中的所有出现"

Claude 会:
- 搜索所有章节
- 记录每次出现的上下文
- 分析其重要性变化
- 评估伏笔效果
```

### 角色关系分析

```
用户: "分析角色 A 和角色 B 的关系演变"

Claude 会:
- 提取两人的所有互动
- 按时间线排序
- 分析关系变化
- 识别关键转折点
```

## 最佳实践

### 1. 逐章分析

建议按顺序分析章节,这样可以:
- 更好地追踪线索发展
- 识别跨章节的模式
- 避免剧透

### 2. 及时更新 Vault

每分析完一章,立即更新 vault:
- 添加新的章节分析
- 更新角色卡片
- 补充线索追踪
- 更新 `Home.md` 和 `00-书籍信息.md`
- 为新出现的双链实体补最小页面,避免 Obsidian 打开空白页
- 优先把实体落到 `Characters/`、`Locations/`、`Objects/`、`Timeline/`
- 如果人物从别称变成全名,更新主卡标题并保留别名入口页

### 2.1 章节写入后做一次校验

推荐在每次新增章节后运行:

```bash
python scripts/validate_vault.py <vault-path>
```

它会检查:
- 是否存在空白 markdown 页
- 是否有 wikilink 指向不存在的文件
- 新章节是否同步写进 `00-书籍信息.md`
- `Home.md` 是否指向最新章节
- 章节导航是否写反
- 人物卡标题变化后是否保留别名入口

### 3. 使用双链

充分利用 Obsidian 的双链功能:
- 所有角色名使用 `[[角色名]]`
- 重要物品使用 `[[物品名]]`
- 地点使用 `[[地点名]]`

### 4. 标签分类

使用一致的标签系统:
- `#mystery` - 推理小说
- `#chapter` - 章节分析
- `#character` - 角色
- `#clue` - 线索
- `#foreshadowing` - 伏笔

### 5. 待办追踪

使用待办列表追踪未解之谜:
- `- [ ] 未解问题`
- `- [x] 已解决问题`

## 故障排除

### Skill 未触发

确保你的请求包含触发词:
- "mystery analysis" / "推理分析"
- "analyze detective story" / "分析侦探故事"
- "track clues" / "追踪线索"
- "mystery novel" / "推理小说"

### EPUB 分析跑偏

如果 AI 看起来在根据常识作答而不是根据正文作答，检查:
- 是否先运行了 `scripts/extract_epub.py`
- 提取结果里是否真的有章节文本和预览
- 是否把 `extracted.json` 或提取出的正文提供给了分析步骤

### Vault 创建失败

检查:
- 目标路径是否有写入权限
- 路径是否已存在同名文件夹
- 磁盘空间是否充足

### 分析质量不佳

提供更多上下文:
- 明确指定章节范围
- 提供完整的章节文本
- 说明你关注的具体方面

### Obsidian 无法打开 Vault

确保:
- Vault 文件夹包含 `.md` 文件
- 文件编码为 UTF-8
- 文件名不包含特殊字符

### 章节写进去了但 Vault 不一致

如果出现“第三章有了,但线索页没更新”“点开双链是空白页”“人物还是旧名字”这类情况,说明只完成了章节写入,没有完成 vault 同步。

按这个顺序修复:
1. 更新 `00-书籍信息.md`
2. 更新 `Analysis/线索追踪.md`
3. 更新 `Home.md`
4. 为新链接补页面或删掉无意义链接
5. 对已揭示真名的人物,改主卡标题并保留别名页
6. 运行 `python scripts/validate_vault.py <vault-path>`

## 示例工作流

### 完整的推理小说分析流程

```
1. 创建 Vault
   "为《白夜行》创建一个 Obsidian vault"

2. 分析第一章
   "分析《白夜行》第一章的线索和伏笔"

3. 更新 Vault
   "将第一章分析添加到 vault"

4. 继续后续章节
   "分析第二章,并检查与第一章的一致性"

5. 生成关系图
   "生成前五章的角色关系图"

6. 追踪线索
   "追踪'废弃建筑'在前五章的所有出现"

7. 一致性检查
   "检查前五章中时间线是否一致"

8. 导出总结
   "生成前五章的分析总结"
```

## 技巧和窍门

### 1. 使用模板

Vault 中的模板文件可以帮助你:
- 保持分析格式一致
- 不遗漏重要维度
- 快速创建新笔记

### 2. 图谱视图

在 Obsidian 中使用图谱视图:
- 可视化角色关系
- 发现隐藏联系
- 识别孤立节点

### 3. 搜索功能

利用 Obsidian 的搜索:
- 搜索特定线索
- 查找角色出现
- 定位关键词

### 4. 标签面板

使用标签面板:
- 快速过滤内容
- 按类型浏览
- 发现模式

## 更多资源

- [Obsidian 官方文档](https://help.obsidian.md/)
- [推理小说分析方法](https://example.com)
- [Claude Code 技能开发](https://docs.anthropic.com)

## 反馈和改进

如果你有任何建议或发现问题:
1. 在项目 GitHub 提交 Issue
2. 分享你的使用案例
3. 贡献改进建议

---

祝你阅读愉快,享受推理的乐趣! 
