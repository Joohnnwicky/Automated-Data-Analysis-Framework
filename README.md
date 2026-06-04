# Automated Data Analysis Framework — 自动化数据分析框架

AI 驱动的数据分析技能，提供从业务意图澄清到专业报告生成的端到端工作流。服务于业务分析师、数据分析师、运营团队和管理层。

**核心价值：** 让数据分析从「理解业务问题」开始，产出管理层可直接汇报的专业报告。

## 这是什么？

这是一个 **Claude Code Skill** — 不是独立运行的软件，而是 Claude Code CLI 的扩展能力。

**使用方式：** 在 Claude Code 对话中直接用自然语言描述分析需求，Claude 会自动调用本项目的数据处理、分析、报告生成能力。

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code CLI                                             │
│                                                              │
│  用户: 分析 data/sales.xlsx，找出增长趋势                     │
│                                                              │
│  Claude: ┌─────────────────────────────────────────────────┐│
│          │ Automated Data Analysis Framework               ││
│          │ ─────────────────────────────────────────────── ││
│          │ [25%] 业务澄清 → 了解分析目标                     ││
│          │ [50%] 数据理解 → 加载画像数据                     ││
│          │ [75%] 多专家分析 → 6个专家并行分析                ││
│          │ [100%] 报告生成 → HTML/PPT 输出                   ││
│          │ ─────────────────────────────────────────────── ││
│          │ ✓ 报告已生成: output/report.html                 ││
│          └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 功能特性

- **业务意图澄清** — 可选的 Phase 0，确保分析方向正确
- **多专家并行分析** — 6 个专业专家角色提供多视角洞察
- **专业报告生成** — 11 种设计风格（FT、McKinsey、Economist 等），支持 HTML/PPT 输出
- **中文优先输出** — 中文报告，保留专业术语英文（ROI、CapEx、FCF 等）
- **自动类型识别** — 自动识别表格、投放、时序数据类型
- **内存安全处理** — 大数据集（>100K 行）自动分块加载和采样
- **进度指示器** — 工作流各阶段清晰可见

## 项目结构

```
dataanalyst/
├── src/
│   ├── data/               # Phase 2: 数据处理引擎
│   │   ├── loader.py       # 数据加载与编码检测
│   │   ├── profiler.py     # 数据画像（维度、统计、缺失值）
│   │   ├── classifier.py   # 类型分类（table/advertising/time_series）
│   │   ├── insights.py     # 初步洞察生成（异常、趋势）
│   │   └── memory.py       # 内存工具（分块、采样、估算）
│   │
│   ├── analysis/           # Phase 3: 分析引擎
│   │   ├── expert_roles.py     # 6 个预定义专家角色
│   │   ├── expert_selector.py  # 专家选择算法
│   │   ├── expert_runner.py    # 并行 subagent 执行
│   │   ├── clarification.py    # 业务意图澄清
│   │   ├── conflict_detector.py # 专家结论冲突检测
│   │   └── statistical_enforcement.py # 强制代码执行验证数值
│   │
│   ├── report/             # Phase 4: 报告生成
│   │   ├── styles.py       # 11 种专业设计风格
│   │   ├── synthesis.py    # 多专家综合引擎
│   │   ├── chart_selector.py   # 自动图表类型匹配
│   │   ├── chart_generator.py  # Plotly 图表生成
│   │   ├── html_report.py  # HTML 报告（Jinja2 模板）
│   │   ├── ppt_report.py   # PowerPoint 报告（python-pptx）
│   │   └── templates/      # Jinja2 HTML 模板
│   │
│   ├── workflow/           # Phase 5: 集成与 UX
│   │   ├── orchestrator.py     # 端到端工作流协调
│   │   ├── intent_detector.py  # 自然语言意图检测
│   │   ├── progress.py     # 进度指示器
│   │   └── phases.py       # 工作流阶段定义
│   │
│   ├── config/             # Phase 1: 基础设施
│   │   └── logging_config.py   # 结构化日志配置
│   │
│   └── scripts/            # 工具脚本
│       ├── read_excel.py   # Excel 读取辅助
│       └── read_pptx.py    # PowerPoint 读取辅助
│
├── tests/                  # 测试套件（157 个测试）
│   ├── test_data_*.py      # 数据模块测试
│   ├── test_expert_*.py    # 分析模块测试
│   ├── test_*.py           # 报告和工作流测试
│   └── test_infrastructure.py # 基础设施测试
│
├── .planning/              # GSD 工作流产物（gitignored）
├── requirements.txt        # 锁定依赖
├── pytest.ini              # 测试配置
└── .gitignore              # Git 忽略规则
```

## 安装部署

### 一键安装（推荐）

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.sh | sh

# 安装后添加到 PATH
export PATH="$PATH:$HOME/.automated-data-analysis/bin"

# 现在可以直接使用
analyze data/sales.xlsx
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/Joohnnwicky/Automated-Data-Analysis-Framework.git
cd Automated-Data-Analysis-Framework

# 安装依赖
pip install -r requirements.txt

# 直接使用 CLI
python src/workflow/cli.py data/sales.xlsx
```

### 环境要求

- Python 3.10+
- pip 包管理器

### 安装依赖

```bash
# 克隆仓库
git clone <repository-url>
cd dataanalyst

# 安装依赖
pip install -r requirements.txt
```

### 依赖说明

| 类别 | 包名 |
|------|------|
| 核心数据处理 | pandas, numpy, scipy, openpyxl, charset-normalizer |
| 可视化 | plotly, kaleido |
| 报告生成 | python-pptx, Pillow, xlsxwriter |
| 测试 | pytest, pytest-cov |
| UX | tqdm |

### 卸载

```bash
# 一键卸载
curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/uninstall.sh | sh

# 或手动卸载
rm -rf ~/.automated-data-analysis
```

## 使用方式

本项目支持两种使用方式：

### 方式一：CLI 命令行（推荐新手）

安装后可直接使用 `analyze` 命令：

```bash
# 基础分析
analyze data/sales.xlsx

# 生成 PPT 报告
analyze data/sales.xlsx --format ppt

# 使用 McKinsey 风格
analyze data/sales.xlsx --style mckinsey

# 指定分析任务
analyze data/sales.xlsx --query "找出ROI下降原因"

# 快速模式（仅显示数据画像）
analyze data/sales.xlsx --quick

# 查看帮助
analyze --help
```

**CLI 参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `data_file` | 数据文件路径 | `data/sales.xlsx` |
| `--format` | 输出格式 | `html` 或 `ppt` |
| `--style` | 设计风格 | `ft`, `mckinsey`, `economist` 等 |
| `--query` | 分析任务 | `"找出增长趋势"` |
| `--output` | 输出目录 | `output` |
| `--quick` | 快速模式 | 仅显示数据画像 |

### 方式二：Claude Code Skill（推荐高级用户）

## 使用指南

本项目是 **Claude Code Skill**，需要在 Claude Code CLI 环境中使用，不是独立运行的 GUI 应用。

### 环境准备

1. **安装 Claude Code CLI**
   ```bash
   # 参考 Claude Code 官方文档安装
   # https://claude.ai/code
   ```

2. **安装项目依赖**
   ```bash
   cd dataanalyst
   pip install -r requirements.txt
   ```

3. **注册 Skill**
   将项目目录放在 Claude Code 的 skills 目录下，或在 Claude Code 中直接指向此项目。

### 启动流程

在 Claude Code CLI 中，直接通过自然语言指令调用：

```bash
# 启动 Claude Code
claude

# 进入对话后，直接描述你的分析需求
> 分析这份销售数据 data/sales.xlsx，找出增长趋势
```

### 交互流程示例

#### 场景 1：完整数据分析

```
用户: 分析 data/advertising.xlsx 这份广告投放数据

Claude: 检测到广告投放数据类型，将启动多专家分析流程...

[25%] Phase 1: 业务澄清
  - 分析目标是什么？优化 ROI / 了解趋势 / 发现问题？
  - 报告受众是谁？管理层 / 运营团队 / 投放专员？
  - 关注哪些指标？ROI, CTR, 转化率, 成本？

用户: 目标是优化 ROI，报告给管理层看，关注 ROI 和转化率

[50%] Phase 2: 数据理解
  - 加载完成: 10,000 行, 12 列
  - 数据类型: advertising (广告投放)
  - 缺失率: 2.1%, 质量评分: 87
  - 初步洞察: Q4 ROI 下降 15%，渠道 A 转化率异常偏高

[75%] Phase 3: 多专家分析
  - 启动专家: 投放优化师, 量化分析师, 用户增长专家
  - 各专家独立分析中...
  - 检测到冲突: 投放优化师建议加大渠道A投入，量化分析师认为渠道A数据异常

[100%] Phase 4: 报告生成
  - 报告已生成: output/report_20260604.html
  - 设计风格: Financial Times
  - 建议导出 PDF: 按 Ctrl/Cmd + P

报告核心发现:
1. ROI 整体下降 8%，主要受渠道 B 成本上升影响
2. 渠道 A 转化率异常偏高，需核实数据准确性
3. 建议: 优化渠道 B 投放策略，核实渠道 A 数据
```

#### 场景 2：快速查询（Quick Mode）

```
用户: 这份数据有多少行？

Claude: [Quick Mode] 
  - 行数: 10,000
  - 列数: 12
  - 文件大小: 1.2 MB

用户: revenue 列的平均值是多少？

Claude: [Quick Mode]
  - revenue 均值: ¥45,632
  - revenue 中位数: ¥42,100
  - revenue 标准差: ¥12,450
```

#### 场景 3：生成 PPT 报告

```
用户: 用 McKinsey 风格生成一份 PPT 报告

Claude: [75%] Phase 4: PPT 报告生成
  - 使用 McKinsey 设计风格
  - 主色调: #18406F
  - 图表嵌入为 PNG

[100%] 报告已生成: output/report_20260604.pptx
  - 包含 8 页幻灯片
  - 结构: 执行摘要 → 关键指标 → 主题分析 → 结论建议
```

### 支持的自然语言指令

| 指令类型 | 示例 | 系统响应 |
|----------|------|----------|
| 数据加载 | "加载 data/sales.xlsx" | 自动识别格式，检测编码 |
| 快速统计 | "有多少行数据" / "revenue 的均值" | Quick Mode 直接返回 |
| 类型识别 | "这是什么类型的数据" | 返回 table/advertising/time_series |
| 完整分析 | "分析这份数据，找出问题" | 启动完整 4 阶段工作流 |
| 生成报告 | "生成 HTML 报告" / "生成 PPT" | 输出指定格式报告 |
| 指定风格 | "用 McKinsey 风格" / "FT 风格" | 应用对应设计风格 |

### 输出文件位置

```
output/
├── report_YYYYMMDD.html      # HTML 报告
├── report_YYYYMMDD.pptx      # PPT 报告
├── experts/                  # 专家分析结果
│   ├── business_context.md   # 业务上下文
│   ├── quant_analyst.md      # 量化分析师输出
│   ├── growth_optimizer.md   # 投放优化师输出
│   └── ...
└── charts/                   # 图表 PNG 文件（PPT 嵌入用）
```

### 常见问题处理

| 问题 | 系统响应 |
|------|----------|
| 文件不存在 | "文件未找到：请确认路径正确，文件存在于 data/ 目录" |
| 格式不支持 | "不支持该格式：仅支持 Excel (.xlsx)、CSV、JSON 文件" |
| 编码错误 | "编码检测失败：已尝试 GB2312/GBK/UTF-8，请确认文件编码" |
| 文件过大 | "文件超过 500MB 限制：建议分批处理或采样分析" |
| 专家结论冲突 | "检测到专家意见分歧：[详情]，建议人工复核" |

## 快速开始

### 1. 加载并画像数据

```python
from pathlib import Path
from src.data.loader import DataLoader
from src.data.profiler import DataProfiler

# 加载数据文件（Excel、CSV 或 JSON）
loader = DataLoader()
df = loader.load_file(Path('data/sales.xlsx'))

# 数据画像
profiler = DataProfiler(df)
profile = profiler.profile()

print(f"维度: {profile['dimensions']['rows']} 行, {profile['dimensions']['columns']} 列")
print(f"缺失率: {profile['quality']['missing_rate']:.2%}")
```

### 2. 分类数据类型

```python
from src.data.classifier import TypeClassifier

classifier = TypeClassifier(df)
data_type, suggested_methods = classifier.classify()

print(f"数据类型: {data_type}")  # 'table', 'advertising', 或 'time_series'
print(f"建议方法: {suggested_methods}")
```

### 3. 运行完整工作流

```python
from pathlib import Path
from src.workflow.orchestrator import WorkflowOrchestrator

# 初始化协调器
orchestrator = WorkflowOrchestrator(
    output_format='html',  # 或 'ppt'
    style='ft'             # 设计风格
)

# 执行端到端工作流
result = orchestrator.execute(
    query="分析这份销售数据，找出增长趋势",
    data_path=Path('data/sales.xlsx')
)

# 获取报告路径
print(f"报告已生成: {result['report_path']}")
```

### 4. Quick Mode（简单查询）

简单查询自动使用快速模式，无需完整多专家分析：

```python
from src.workflow.intent_detector import detect_intent, should_use_quick_mode
from src.workflow.intent_detector import quick_response

# 检测意图
intent = detect_intent("这份数据有多少行")
print(f"意图: {intent.intent_type}")  # 'quick_stats'

# 快速模式判断
if should_use_quick_mode(df, intent):
    # 直接返回统计结果，无需完整工作流
    response = quick_response(df, intent)
```

## 模块使用详解

### 数据加载 (`src/data/loader.py`)

```python
from pathlib import Path
from src.data.loader import DataLoader, DataLoadError, detect_encoding

# 自动编码检测（支持 GB2312、GBK、UTF-8）
encoding = detect_encoding(Path('data/chinese_data.csv'))

# 安全加载与错误处理
loader = DataLoader()
try:
    df = loader.load_file(Path('data/sales.xlsx'))
except DataLoadError as e:
    print(f"错误: {e.user_message}")        # 中文友好提示
    print(f"详情: {e.technical_detail}")    # 技术调试信息

# 大文件内存安全加载
df = loader.load_file(Path('data/big_file.csv'), chunk_size=50000)
```

### 数据画像 (`src/data/profiler.py`)

```python
from src.data.profiler import DataProfiler

profiler = DataProfiler(df)
profile = profiler.profile()

# 画像结构:
{
    'dimensions': {'rows': 1000, 'columns': 15},
    'fields': [
        {'name': 'revenue', 'type': 'numeric', 'missing_rate': 0.02, 'unique_count': 950},
        ...
    ],
    'statistics': {
        'revenue': {'mean': 45000, 'std': 12000, 'min': 5000, 'max': 100000}
    },
    'quality': {
        'missing_rate': 0.05,
        'duplicate_rate': 0.01,
        'quality_score': 85
    }
}

# 获取优化建议
suggestions = profiler.suggest_memory_optimization()
# 返回: {'category_columns': ['status', 'region'], 'estimated_reduction': '40%'}
```

### 类型分类 (`src/data/classifier.py`)

```python
from src.data.classifier import classify_data_type, detect_advertising_keywords

# 分类数据类型
data_type, methods = classify_data_type(df)
# 返回: ('advertising', ['ROI分析', 'CTR趋势', '渠道对比'])

# 检测投放关键词
keywords = detect_advertising_keywords(df.columns)
# 返回: ['ROI', 'CTR', 'click', 'impression', '转化']

# 检测时间列
datetime_cols = detect_datetime_columns(df)
# 返回: ['date', 'created_at', '更新时间']
```

### 专家角色 (`src/analysis/expert_roles.py`)

6 个预定义专家角色覆盖所有数据类型：

| 角色 ID | 名称 | 专业领域 | 数据类型 |
|---------|------|----------|----------|
| `quant_analyst` | 量化分析师 | 统计建模与分布分析 | table, time_series, advertising |
| `valuation_expert` | 估值专家 | 财务估值与现金流 | table, time_series |
| `growth_optimizer` | 投放优化师 | 广告 ROI 优化 | advertising |
| `user_growth` | 用户增长专家 | 用户行为与增长分析 | table, advertising |
| `industry_analyst` | 行业分析师 | 对标与战略分析 | table, time_series |
| `financial_analyst` | 财务分析师 | 财务健康与风险评估 | table, time_series |

```python
from src.analysis.expert_roles import EXPERT_ROLES, ExpertRole

# 查看专家定义
for role in EXPERT_ROLES:
    print(f"{role.name}: {role.domain}")

# 按数据类型筛选
advertising_experts = [r for r in EXPERT_ROLES if 'advertising' in r.data_types]
```

### 专家选择 (`src/analysis/expert_selector.py`)

```python
from src.analysis.expert_selector import ExpertSelector

selector = ExpertSelector()

# 按数据类型选择专家
experts = selector.select(
    data_type='advertising',
    business_context={'goal': '优化ROI', 'audience': '市场团队'}
)

# 每个专家获得隔离上下文（无跨专家引用）
# 返回: [ExpertRole(id='growth_optimizer'), ExpertRole(id='user_growth'), ...]

# 输出角色定义供审阅
selector.write_role_definitions(experts, Path('output/expert_roles.md'))
```

### 业务澄清 (`src/analysis/clarification.py`)

```python
from src.analysis.clarification import BusinessClarifier

clarifier = BusinessClarifier()

# 检查是否需要触发澄清
if clarifier.should_trigger(df):
    # 提问 3 个核心问题
    answers = clarifier.ask_questions()
    # 返回: {'goal': '...', 'audience': '...', 'metrics': '...'}

    # 写入业务上下文
    clarifier.write_context(answers, Path('output/experts/business_context.md'))

# 简单任务可跳过澄清
clarifier = BusinessClarifier(skip=True)
```

### 报告生成 (`src/report/`)

#### 设计风格

11 种专业设计风格：

| 风格 ID | 名称 | 适用场景 |
|---------|------|----------|
| `ft` | Financial Times | 财务报告 |
| `mckinsey` | McKinsey | 战略分析 |
| `economist` | Economist | 经济分析 |
| `goldman` | Goldman Sachs | 投资报告 |
| `swiss` | Swiss Style | 简洁极简 |
| `wsj` | Wall Street Journal | 商业新闻 |
| `bloomberg` | Bloomberg | 市场分析 |
| `reuters` | Reuters | 新闻报道 |
| `morningstar` | Morningstar | 投研报告 |
| `bcg` | BCG | 咨询报告 |
| `bain` | Bain & Company | 战略咨询 |

```python
from src.report.styles import get_design_style, DesignStyle

# 获取风格定义
style = get_design_style('mckinsey')
print(f"主色调: {style.primary_color}")  # #18406F

# 生成 CSS 变量用于模板
css_vars = style.to_css_vars()
# 返回: {'--primary-color': '#18406F', '--font-family': 'Noto Sans SC', ...}
```

#### HTML 报告

```python
from pathlib import Path
from src.report.html_report import HTMLReportGenerator

generator = HTMLReportGenerator(style='ft')

# 生成报告
report_path = generator.generate(
    report_data={
        'title': '销售分析报告',
        'executive_summary': '总体销售增长15%',
        'metrics_panel': {...},
        'thematic_analysis': {...},
        'conclusions': [...]
    },
    output_path=Path('output/report.html')
)

# 特性:
# - XSS 防护（Jinja2 autoescape）
# - PDF 导出提示（Ctrl/Cmd + P）
# - Plotly 图表嵌入为 SVG
# - 中文优先输出（lang='zh-CN'）
```

#### PPT 报告

```python
from src.report.ppt_report import PPTReportGenerator

generator = PPTReportGenerator(style='mckinsey')

# 生成 PowerPoint
report_path = generator.generate(
    report_data={...},
    output_path=Path('output/report.pptx')
)

# 特性:
# - 直接 python-pptx 构建（无需 HTML 转换）
# - 图表嵌入为 PNG 图片
# - 样式化标题和内容幻灯片
```

### 工作流协调器 (`src/workflow/orchestrator.py`)

```python
from pathlib import Path
from src.workflow.orchestrator import WorkflowOrchestrator

# 初始化
orchestrator = WorkflowOrchestrator(
    output_format='html',  # 'html' 或 'ppt'
    style='ft'             # 设计风格 ID
)

# 执行完整工作流
result = orchestrator.execute(
    query="分析这份广告投放数据，找出ROI下降的原因",
    data_path=Path('data/advertising.xlsx'),
    skip_clarification=False  # 设为 True 跳过 Phase 0
)

# 结果结构:
{
    'intent': IntentMatch(...),        # 检测到的意图
    'profile': {...},                  # 数据画像
    'workflow_mode': 'full',           # 'quick' 或 'full'
    'expert_outputs': {                # 专家分析路径
        'growth_optimizer': 'output/experts/growth_optimizer.md',
        'quant_analyst': 'output/experts/quant_analyst.md',
    },
    'report_path': 'output/report.html'
}
```

## 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定模块测试
python -m pytest tests/test_data_loader.py -v
python -m pytest tests/test_expert_selector.py -v

# 运行覆盖率测试
python -m pytest tests/ --cov=src --cov-report=html

# 当前状态: 157 通过, 4 跳过（集成测试）
```

## 输出示例

### 数据画像输出

```
数据概览
--------
行数: 10,000
列数: 15
缺失率: 2.5%
重复行: 0.1%

字段类型:
- revenue: 数值型 (唯一值: 9,850)
- date: 时间型 (范围: 2024-01 ~ 2024-12)
- region: 分类型 (唯一值: 5)

初步洞察:
- 异常值: revenue 列存在 5% 异常值 (>2σ)
- 趋势: Q4 相比 Q1 增长 20%
```

### 报告输出结构

```
报告标题: 销售增长20%，华东区域领跑

1. 执行摘要
   - 核心发现摘要
   - 关键指标变化

2. 关键指标面板
   - ROI: 15.2% (↑3%)
   - 转化率: 4.5% (↑0.8%)
   - 客单价: ¥850 (↑¥50)

3. 主题深度分析
   - 区域分析: 华东增长最快
   - 产品分析: A类产品贡献60%
   - 渠道分析: 线上渠道占比提升

4. 综合结论
   - 建议加大华东投入
   - 优化A类产品供应链
```

## 安全考虑

| 威胁 ID | 严重程度 | 缓解措施 |
|---------|----------|----------|
| T-2-03b | 高 | 500MB 文件大小限制防止内存耗尽 |
| T-3-03 | 高 | 统计强制要求所有数值结论通过代码执行 |
| T-4-01 | 高 | XSS 防护通过 Jinja2 autoescape |
| T-5-06 | 中 | DataLoadError 保留中文友好提示 |

## 版本限制 (v1.0)

- **仅静态文件** — Excel、CSV、JSON；不支持数据库或 API 流
- **中文优先** — 英文支持计划于 v2
- **固定设计风格** — 自定义风格参数计划于 v2
- **无数据清洗** — 假设数据已准备好

## 版本历史

- **v1.0** (2026-06-04) — 功能完整，5 个阶段，157 测试通过
  - Phase 1: 基础设施
  - Phase 2: 数据处理引擎
  - Phase 3: 分析引擎
  - Phase 4: 报告生成
  - Phase 5: 集成与 UX 优化

## 许可证

内部项目，用于 Claude Code skill 使用。