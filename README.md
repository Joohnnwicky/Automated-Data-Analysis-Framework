# Automated Data Analysis Framework

> AI 驱动的数据分析工具，从业务理解到专业报告生成，一站式完成。

## 功能

- 📊 **智能数据画像** — 自动识别 Excel/CSV/JSON，检测编码，输出数据概览
- 🎯 **多专家分析** — 6 种专家角色并行分析，提供多视角洞察
- 📄 **专业报告** — 11 种设计风格（FT、McKinsey、Economist 等），HTML/PPT 输出
- 🇨🇳 **中文优先** — 中文报告，保留专业术语（ROI、CapEx、FCF）

## 安装

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.sh | sh
```

### Windows

```powershell
iwr -useb https://raw.githubusercontent.com/Joohnnwicky/Automated-Data-Analysis-Framework/main/install.ps1 | iex
```

### 手动安装

```bash
git clone https://github.com/Joohnnwicky/Automated-Data-Analysis-Framework.git
cd Automated-Data-Analysis-Framework
pip install -r requirements.txt
```

## 使用

### 命令行

```bash
# 基础分析
analyze data/sales.xlsx

# PPT 报告
analyze data/sales.xlsx --format ppt

# 指定风格
analyze data/sales.xlsx --style mckinsey

# 查看帮助
analyze --help
```

### Claude Code Skill

在 Claude Code CLI 中直接描述分析需求：

```
> 分析这份销售数据，找出增长趋势
> 用 McKinsey 风格生成 PPT 报告
```

## 设计风格

| 风格 | 适用场景 |
|------|----------|
| `ft` | 财务报告 |
| `mckinsey` | 战略分析 |
| `economist` | 经济分析 |
| `goldman` | 投资报告 |
| `wsj` | 商业新闻 |
| `bloomberg` | 市场分析 |
| `bcg` / `bain` | 咨询报告 |

## 要求

- Python 3.10+
- 支持：Excel (.xlsx)、CSV、JSON

## 许可证

MIT