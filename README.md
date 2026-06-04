# Data Analyst Pro — 融合增强版数据分析 Skill

AI-powered data analysis skill that provides end-to-end workflow from business intent clarification to professional report generation. Designed for business analysts, data analysts, operations teams, and management.

**Core Value:** 让数据分析从「理解业务问题」开始，产出管理层可直接汇报的专业报告。

## Features

- **Business Intent Clarification** — Optional Phase 0 to ensure analysis direction is correct
- **Multi-Expert Parallel Analysis** — 6 specialized expert roles providing multi-perspective insights
- **Professional Report Generation** — 11 design styles (FT, McKinsey, Economist, etc.) with HTML/PPT output
- **Chinese-First Output** — Reports in Chinese with professional terminology retained (ROI, CapEx, FCF, etc.)
- **Automatic Type Detection** — Recognizes table, advertising, and time-series data types
- **Memory-Safe Processing** — Chunked loading and sampling for large datasets (>100K rows)
- **Progress Indicators** — Clear phase transitions during workflow execution

## Project Structure

```
dataanalyst/
├── src/
│   ├── data/               # Phase 2: Data Processing Engine
│   │   ├── loader.py       # Data loading with encoding detection
│   │   ├── profiler.py     # Data profiling (dimensions, statistics, missing values)
│   │   ├── classifier.py   # Type classification (table/advertising/time_series)
│   │   ├── insights.py     # Initial insight generation (anomalies, trends)
│   │   └── memory.py       # Memory utilities (chunking, sampling, estimation)
│   │
│   ├── analysis/           # Phase 3: Analysis Engine
│   │   ├── expert_roles.py     # 6 predefined expert role definitions
│   │   ├── expert_selector.py  # Expert selection algorithm
│   │   ├── expert_runner.py    # Parallel subagent execution
│   │   ├── clarification.py    # Business intent clarification
│   │   ├── conflict_detector.py # Detect conflicting expert conclusions
│   │   └── statistical_enforcement.py # Enforce code execution for numerical claims
│   │
│   ├── report/             # Phase 4: Report Generation
│   │   ├── styles.py       # 11 professional design styles
│   │   ├── synthesis.py    # Multi-expert synthesis engine
│   │   ├── chart_selector.py   # Automatic chart type matching
│   │   ├── chart_generator.py  # Plotly chart generation
│   │   ├── html_report.py  # HTML report with Jinja2 templates
│   │   ├── ppt_report.py   # PowerPoint report via python-pptx
│   │   └── templates/      # Jinja2 HTML templates
│   │
│   ├── workflow/           # Phase 5: Integration & UX
│   │   ├── orchestrator.py     # End-to-end workflow coordination
│   │   ├── intent_detector.py  # Natural language intent detection
│   │   ├── progress.py     # Progress indicators
│   │   └── phases.py       # Workflow phase definitions
│   │
│   ├── config/             # Phase 1: Infrastructure
│   │   └── logging_config.py   # Structured logging setup
│   │
│   └── scripts/            # Utility scripts
│       ├── read_excel.py   # Excel reading helper
│       └── read_pptx.py    # PowerPoint reading helper
│
├── tests/                  # Test suite (157 tests)
│   ├── test_data_*.py      # Data module tests
│   ├── test_expert_*.py    # Analysis module tests
│   ├── test_*.py           # Report and workflow tests
│   └── test_infrastructure.py # Infrastructure tests
│
├── .planning/              # GSD workflow artifacts (gitignored)
├── requirements.txt        # Locked dependencies
├── pytest.ini              # Test configuration
└── .gitignore              # Git ignore patterns
```

## Installation

### Prerequisites

- Python 3.10+
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd dataanalyst

# Install dependencies
pip install -r requirements.txt
```

### Dependencies Overview

| Category | Packages |
|----------|----------|
| Core Data | pandas, numpy, scipy, openpyxl, charset-normalizer |
| Visualization | plotly, kaleido |
| Reports | python-pptx, Pillow, xlsxwriter |
| Testing | pytest, pytest-cov |
| UX | tqdm |

## Quick Start

### 1. Load and Profile Data

```python
from pathlib import Path
from src.data.loader import DataLoader
from src.data.profiler import DataProfiler

# Load data file (Excel, CSV, or JSON)
loader = DataLoader()
df = loader.load_file(Path('data/sales.xlsx'))

# Profile the data
profiler = DataProfiler(df)
profile = profiler.profile()

print(f"Dimensions: {profile['dimensions']['rows']} rows, {profile['dimensions']['columns']} columns")
print(f"Missing rate: {profile['quality']['missing_rate']:.2%}")
```

### 2. Classify Data Type

```python
from src.data.classifier import TypeClassifier

classifier = TypeClassifier(df)
data_type, suggested_methods = classifier.classify()

print(f"Data type: {data_type}")  # 'table', 'advertising', or 'time_series'
print(f"Suggested methods: {suggested_methods}")
```

### 3. Run Full Workflow

```python
from pathlib import Path
from src.workflow.orchestrator import WorkflowOrchestrator

# Initialize orchestrator
orchestrator = WorkflowOrchestrator(
    output_format='html',  # or 'ppt'
    style='ft'             # Design style
)

# Execute end-to-end workflow
result = orchestrator.execute(
    query="分析这份销售数据，找出增长趋势",
    data_path=Path('data/sales.xlsx')
)

# Get report path
print(f"Report generated: {result['report_path']}")
```

### 4. Quick Mode (Simple Queries)

For simple queries, the system automatically uses quick mode without full multi-expert analysis:

```python
from src.workflow.intent_detector import detect_intent, should_use_quick_mode

# Detect intent
intent = detect_intent("这份数据有多少行")
print(f"Intent: {intent.intent_type}")  # 'quick_stats'

# Quick mode check
if should_use_quick_mode(df, intent):
    # Returns immediate statistics without full workflow
    response = quick_response(df, intent)
```

## Module Usage

### Data Loading (`src/data/loader.py`)

```python
from pathlib import Path
from src.data.loader import DataLoader, DataLoadError, detect_encoding

# Automatic encoding detection (supports GB2312, GBK, UTF-8)
encoding = detect_encoding(Path('data/chinese_data.csv'))

# Safe loading with error handling
loader = DataLoader()
try:
    df = loader.load_file(Path('data/sales.xlsx'))
except DataLoadError as e:
    print(f"Error: {e.user_message}")  # Chinese user-friendly message
    print(f"Detail: {e.technical_detail}")  # Technical debug info

# Memory-safe loading for large files
df = loader.load_file(Path('data/big_file.csv'), chunk_size=50000)
```

### Data Profiling (`src/data/profiler.py`)

```python
from src.data.profiler import DataProfiler

profiler = DataProfiler(df)
profile = profiler.profile()

# Profile structure:
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

# Get optimization suggestions
suggestions = profiler.suggest_memory_optimization()
# Returns: {'category_columns': ['status', 'region'], 'estimated_reduction': '40%'}
```

### Type Classification (`src/data/classifier.py`)

```python
from src.data.classifier import classify_data_type, detect_advertising_keywords

# Classify data type
data_type, methods = classify_data_type(df)
# Returns: ('advertising', ['ROI分析', 'CTR趋势', '渠道对比'])

# Check for advertising keywords
keywords = detect_advertising_keywords(df.columns)
# Returns: ['ROI', 'CTR', 'click', 'impression', '转化']

# Detect datetime columns
datetime_cols = detect_datetime_columns(df)
# Returns: ['date', 'created_at', '更新时间']
```

### Expert Roles (`src/analysis/expert_roles.py`)

6 predefined expert roles covering all data types:

| Role ID | Name | Domain | Data Types |
|---------|------|--------|------------|
| `quant_analyst` | 量化分析师 | Statistical analysis | table, time_series, advertising |
| `valuation_expert` | 估值专家 | Financial valuation | table, time_series |
| `growth_optimizer` | 投放优化师 | Advertising ROI | advertising |
| `user_growth` | 用户增长专家 | User behavior analysis | table, advertising |
| `industry_analyst` | 行业分析师 | Competitive analysis | table, time_series |
| `financial_analyst` | 财务分析师 | Financial health | table, time_series |

```python
from src.analysis.expert_roles import EXPERT_ROLES, ExpertRole

# Access expert definitions
for role in EXPERT_ROLES:
    print(f"{role.name}: {role.domain}")

# Filter by data type
advertising_experts = [r for r in EXPERT_ROLES if 'advertising' in r.data_types]
```

### Expert Selection (`src/analysis/expert_selector.py`)

```python
from src.analysis.expert_selector import ExpertSelector

selector = ExpertSelector()

# Select experts by data type
experts = selector.select(
    data_type='advertising',
    business_context={'goal': 'optimize ROI', 'audience': 'marketing team'}
)

# Each expert gets isolated context (no cross-expert references)
# Returns: [ExpertRole(id='growth_optimizer'), ExpertRole(id='user_growth'), ...]

# Write role definitions for review
selector.write_role_definitions(experts, Path('output/expert_roles.md'))
```

### Business Clarification (`src/analysis/clarification.py`)

```python
from src.analysis.clarification import BusinessClarifier

clarifier = BusinessClarifier()

# Check if clarification should trigger
if clarifier.should_trigger(df):
    # Ask 3 core questions
    answers = clarifier.ask_questions()
    # Returns: {'goal': '...', 'audience': '...', 'metrics': '...'}

    # Write business context
    clarifier.write_context(answers, Path('output/experts/business_context.md'))

# Skip clarification for simple tasks
clarifier = BusinessClarifier(skip=True)
```

### Report Generation (`src/report/`)

#### Design Styles

11 professional design styles available:

| Style ID | Name | Use Case |
|----------|------|----------|
| `ft` | Financial Times | Financial reporting |
| `mckinsey` | McKinsey | Strategic analysis |
| `economist` | Economist | Economic analysis |
| `goldman` | Goldman Sachs | Investment reports |
| `swiss` | Swiss Style | Clean, minimalist |
| `wsj` | Wall Street Journal | Business news |
| `bloomberg` | Bloomberg | Market analysis |
| `reuters` | Reuters | News reporting |
| `morningstar` | Morningstar | Investment research |
| `bcg` | BCG | Consulting reports |
| `bain` | Bain & Company | Strategy consulting |

```python
from src.report.styles import get_design_style, DesignStyle

# Get style definition
style = get_design_style('mckinsey')
print(f"Primary color: {style.primary_color}")  # #18406F

# Generate CSS variables for templates
css_vars = style.to_css_vars()
# Returns: {'--primary-color': '#18406F', '--font-family': 'Noto Sans SC', ...}
```

#### HTML Report

```python
from pathlib import Path
from src.report.html_report import HTMLReportGenerator

generator = HTMLReportGenerator(style='ft')

# Generate report
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

# Features:
# - XSS prevention via Jinja2 autoescape
# - PDF export hint (Ctrl/Cmd + P)
# - Embedded Plotly charts as SVG
# - Chinese-first output with lang='zh-CN'
```

#### PPT Report

```python
from src.report.ppt_report import PPTReportGenerator

generator = PPTReportGenerator(style='mckinsey')

# Generate PowerPoint
report_path = generator.generate(
    report_data={...},
    output_path=Path('output/report.pptx')
)

# Features:
# - Direct python-pptx construction (no HTML conversion)
# - Chart embedding as PNG images
# - Styled title and content slides
```

### Workflow Orchestrator (`src/workflow/orchestrator.py`)

```python
from pathlib import Path
from src.workflow.orchestrator import WorkflowOrchestrator

# Initialize with options
orchestrator = WorkflowOrchestrator(
    output_format='html',  # 'html' or 'ppt'
    style='ft'             # Design style ID
)

# Execute full workflow
result = orchestrator.execute(
    query="分析这份广告投放数据，找出ROI下降的原因",
    data_path=Path('data/advertising.xlsx'),
    skip_clarification=False  # Set True to skip Phase 0
)

# Result structure:
{
    'intent': IntentMatch(...),        # Detected intent
    'profile': {...},                  # Data profile
    'workflow_mode': 'full',           # 'quick' or 'full'
    'expert_outputs': {                # Expert analysis paths
        'growth_optimizer': 'output/experts/growth_optimizer.md',
        'quant_analyst': 'output/experts/quant_analyst.md',
    },
    'report_path': 'output/report.html'
}
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific module tests
python -m pytest tests/test_data_loader.py -v
python -m pytest tests/test_expert_selector.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Current test status: 157 passed, 4 skipped (integration tests)
```

## Output Examples

### Data Profile Output

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

### Report Output Structure

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

## Security Considerations

| Threat ID | Severity | Mitigation |
|-----------|----------|------------|
| T-2-03b | HIGH | 500MB file size limit prevents memory exhaustion |
| T-3-03 | HIGH | Statistical enforcement requires code execution for all numerical claims |
| T-4-01 | HIGH | XSS prevention via Jinja2 autoescape |
| T-5-06 | MEDIUM | DataLoadError preserved with user-friendly Chinese messages |

## Limitations (v1.0)

- **Static files only** — Excel, CSV, JSON; no database or API streaming
- **Chinese-first** — English support planned for v2
- **Fixed design styles** — Custom style parameters planned for v2
- **No data cleaning** — Assumes data is already prepared

## License

Internal project for Claude Code skill usage.

## Version History

- **v1.0** (2026-06-04) — Feature-complete with 5 phases, 157 tests passing
  - Phase 1: Infrastructure Foundation
  - Phase 2: Data Processing Engine
  - Phase 3: Analysis Engine
  - Phase 4: Report Generation
  - Phase 5: Integration & UX Polish