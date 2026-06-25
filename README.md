# Automated Data Analysis Framework

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blue)](https://claude.ai/code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)

> 面向中文场景的数据分析与专业报告生成 Skill：从原始数据、半结构化材料到可交付的 Markdown / HTML / PPT 报告。

---

## 这是什么

`automated-data-analysis` 是一个 Claude Code Skill，用于把数据分析流程产品化：

1. **理解数据**：读取数据、识别字段、检测编码、生成数据画像。
2. **分析问题**：围绕用户目标进行多视角分析、排序、对比和解释。
3. **生成报告**：输出结构清晰、可交付的专业报告。
4. **可视化表达**：HTML 报告默认加入图表，而不是只给表格。

适用场景包括：

- 经营分析、销售分析、投放分析、用户增长分析；
- 财务、行业、运营、管理层汇报；
- 多周期数据对比；
- 半结构化材料先整理成 CSV/JSON，再生成报告；
- 需要中文报告、中文图表、离线 HTML 交付的场景。

---

## 启动方式

在 Claude Code 中直接输入：

```text
/automated-data-analysis
```

也可以把需求一起写上：

```text
/automated-data-analysis 分析这个 CSV，生成一份带图表的 HTML 数据分析报告
```

```text
/automated-data-analysis 读取这几个文件，先整理成结构化 CSV/JSON，再生成专业分析报告
```

也可以用自然语言触发：

```text
用 automated-data-analysis 这个 skill 分析这份数据，生成报告
```

---

## 核心能力

### 1. 数据理解

- 自动识别字段类型、缺失值、异常值和基础统计分布。
- 支持中文编码场景，优先保证中文内容不乱码。
- 对半结构化来源，先抽取成 UTF-8 中间文件，再整理为结构化 CSV/JSON。
- 保留来源、周期、分类、实体、日期、指标、原始值、标准化值、单位、阈值、状态等可追溯字段。

### 2. 多视角分析

内置多类专家视角，可按任务选择：

| 角色 | 关注点 |
|---|---|
| 量化分析师 | 统计分布、相关性、异常检测 |
| 估值专家 | FCF、估值指标、财务健康 |
| 投放优化师 | ROI、CTR、渠道效率 |
| 用户增长专家 | 用户行为、漏斗、留存 |
| 行业分析师 | 对标、竞争格局、趋势 |
| 财务分析师 | 财务比率、风险评估 |

### 3. 专业报告生成

默认报告结构面向专业交付，而不是简单问答：

1. 背景与报告目标
2. 执行摘要
3. 数据理解与处理方法
4. 总体画像
5. 分组 / 分层 / 趋势分析
6. 风险、机会或优先级排序
7. 建议与后续动作
8. 方法局限
9. 附录：数据字典与产出文件

支持风格：

```text
ft | mckinsey | economist | goldman | swiss | wsj | bloomberg | reuters | morningstar | bcg | bain
```

---

## 用户确认的默认规则

这些规则来自实际使用反馈，后续使用 Skill 时默认遵守。

### 1. 默认使用中性的专业交付口径

- 数据分析报告
- 管理层摘要
- 业务分析建议
- 项目组 / 数据服务团队
- 后续动作与方法局限

### 2. 半结构化数据先结构化

如果输入不是标准 Excel/CSV/JSON，而是 PDF、Markdown、TXT 或其他半结构化材料：

1. 先抽取原始文本或表格内容。
2. 写入 UTF-8 中间文件，避免控制台编码影响判断。
3. 再解析成结构化 CSV/JSON。
4. 最后基于结构化数据生成报告。

不要直接从原始文本跳到结论。

### 3. 派生指标必须解释

如果报告中使用派生指标，必须说明：

- 指标公式；
- 适用范围；
- 分层阈值；
- 缺失值、截尾值、异常值或标准化处理方式；
- 哪些结论不能由该指标直接推出。

不要因为样本量变化、覆盖范围变化、统计口径变化而过度推断因果。

### 4. HTML 报告必须有图

当数据支持可视化时，HTML 不能只包含 KPI 卡片和表格。默认至少加入多种图形表达。

推荐图表：

| 图表 | 用途 |
|---|---|
| 构成图 | 展示类别、章节、业务板块占比 |
| 条形图 / 柱状图 | 展示 Top N 维度排序 |
| 饼图 / 环图 | 展示分布、分桶、结构占比 |
| 趋势图 | 展示时间变化 |
| 散点图 | 展示关系、异常点、阈值附近样本 |
| 热力图 | 展示二维交叉，如区域 × 指标、品类 × 周期 |

### 5. 默认使用离线内联 SVG

HTML 可视化默认使用 Python 生成内联 SVG，而不是依赖 Chart.js 或 CDN。

原因：

- 单文件 HTML 可离线打开；
- 不依赖网络；
- 更适合企业归档和打印；
- 避免浏览器脚本或 CDN 兼容问题。

如果当前脚本缺图表能力，应补充简单 SVG 生成函数，例如：

```python
bar_svg(...)
donut_svg(...)
scatter_svg(...)
heatmap_svg(...)
trend_svg(...)
```

### 6. Word 是可选导出

默认先把 Markdown / HTML 分析报告做好。

只有当用户明确要求 Word 时，再额外生成 `.docx`。Word 排版不作为默认优先事项。

---

## 输出文件

常见输出包括：

| 文件 | 说明 |
|---|---|
| `*.csv` | 清洗后的结构化数据 |
| `*.json` | 统计摘要、分组指标、元数据 |
| `*.md` | Markdown 分析报告 |
| `*.html` | 带图表的离线 HTML 报告 |
| `*.pptx` | 可选 PPT 报告 |
| `*.docx` | 用户要求时的可选 Word 报告 |

---

## 验证清单

生成报告后应检查：

- Markdown / HTML 文件已生成；
- HTML 中包含多个 `<svg` 图表，完整分析报告通常不少于 5 个；
- HTML 不默认依赖 `<script>`、CDN 或 Chart.js；
- 除非用户明确要求，不出现求职类表述：`应聘`、`招聘`、`面试`、`简历`、`JD`、`目标公司`、`岗位`；
- 报告中的核心数字与 CSV/JSON 统计结果一致；
- 派生指标、阈值、数据处理限制已披露；
- 没有从覆盖变化或样本量变化中做无依据因果推断。

---

## 安装

### Claude Code Skill 安装

```bash
npx skills add Joohnnwicky/Automated-Data-Analysis-Framework
```

或手动放入：

| Runtime | Skills 目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Continue | `~/.continue/skills/` |

### 本地 CLI 安装

macOS / Linux：

```bash
curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.sh | sh
```

Windows：

```powershell
iwr -useb https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.ps1 | iex
```

安装后可使用 `analyze` 命令，或在 Claude Code 中直接调用 Skill。

---

## 项目结构

```text
automated-data-analysis/
├── SKILL.md                 # Skill 定义与行为规则
├── README.md                # 项目说明
├── requirements.txt         # Python 依赖
├── install.ps1              # Windows 安装脚本
├── install.sh               # macOS / Linux 安装脚本
├── src/
│   ├── data/                # 数据加载、分类、画像
│   ├── analysis/            # 多专家分析与统计逻辑
│   ├── report/              # HTML/PPT/图表生成
│   └── workflow/            # CLI 与工作流协调
└── tests/                   # 测试用例
```

---

## 要求

- Python 3.10+
- Claude Code 或兼容 Skill 的运行环境
- 基础支持：Excel `.xlsx`、CSV、JSON
- 半结构化文件需要按任务先抽取、解析、结构化

---

## License

MIT
