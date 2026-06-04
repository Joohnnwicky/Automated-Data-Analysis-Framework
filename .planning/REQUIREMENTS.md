# Requirements — Data Analyst Pro

**Project:** AI-powered data analysis skill (huashu-data-pro + data-analyst TUI 融合)
**Version:** v1
**Last Updated:** 2026-06-03

---

## v1 Requirements

### Infrastructure (Phase 1)

- [ ] **INF-01**: 创建 requirements.txt 并锁定所有 Python 依赖版本
- [ ] **INF-02**: 使用 pathlib 替换所有硬编码 Windows 路径，实现跨平台兼容
- [ ] **INF-03**: 引入 logging 模块替换 200+ print 语句，支持日志级别配置
- [ ] **INF-04**: Git 版本控制初始化，规划文档纳入 .gitignore 或版本控制
- [ ] **INF-05**: 清理 __MACOSX 元数据目录，规范化 skill 文件结构

### Phase 0: Business Intent Clarification

- [ ] **CLAR-01**: 用户可选择是否进入业务意图澄清流程（可选交互，简单任务可跳过）
- [ ] **CLAR-02**: 实现 3 个核心问题询问：分析目标、报告受众、核心关注指标
- [ ] **CLAR-03**: 澄清结果写入 `.planning/context.md` 供后续阶段参考
- [ ] **CLAR-04**: 提供快速跳过选项，直接进入 Phase 1 数据理解
- [ ] **CLAR-05**: 支持智能触发判断（数据复杂度 > 阈值时自动进入澄清）

### Phase 1: Data Understanding

- [x] **DATA-01**: 自动读取 Excel (.xlsx)、CSV、JSON 数据文件，支持中文编码
- [x] **DATA-02**: 输出数据概览（维度、字段、数据类型、缺失率、统计摘要）
- [x] **DATA-03**: 实现数据类型自动识别（表格数据/投放数据/时序数据）
- [x] **DATA-04**: 基础统计分析（均值/中位数/极值/分布）
- [x] **DATA-05**: 输出初步洞察（1-2 个可见趋势或异常）
- [x] **DATA-06**: 大数据集 chunking 支持（>10万行时采样策略）
- [x] **DATA-07**: 缺失值报告 + 处理策略建议

### Phase 2: Multi-Expert Analysis

- [ ] **EXPT-01**: Expert Selector 根据数据类型和业务意图选取 3-5 个专家角色
- [ ] **EXPT-02**: 专家角色库：量化分析师、估值专家、投放优化师、用户增长专家、行业分析师、财务分析师
- [ ] **EXPT-03**: 每个专家角色用 subagent 并行执行分析（run_in_background=true）
- [ ] **EXPT-04**: 专家角色陈述写入 md 文件供用户确认或调整
- [ ] **EXPT-05**: Subagent 上下文隔离（每个专家只看到自己的角色定义）
- [ ] **EXPT-06**: 每个专家写入独立输出文件，不共享状态
- [ ] **EXPT-07**: 强制代码计算，禁用 LLM mental math（防止 PITFALL-01）
- [ ] **EXPT-08**: 支持专家分析矛盾检测和标记

### Phase 3: Report Generation

- [ ] **REP-01**: HTML 报告生成（默认输出，内嵌 SVG/Canvas 图表）
- [ ] **REP-02**: PPT 生成（用户明确要求时，HTML→PPTX 转换）
- [ ] **REP-03**: 11 种设计风格选择（FT/McKinsey/Economist/Goldman/Swiss + 6 种设计风格）
- [ ] **REP-04**: 中文优先输出（保留专业术语英文：ROI、CapEx、FCF、MA200 等）
- [ ] **REP-05**: 结论式标题（「CapEx翻倍，净现金首次转负」而非「资本支出分析」）
- [ ] **REP-06**: Manager-POV Synthesis（从管理型分析师视角整合，不出现专家名字）
- [ ] **REP-07**: 报告结构：核心摘要 → 关键指标面板 → 分主题分析 → 综合结论与建议
- [ ] **REP-08**: 单一设计风格源（防止样式漂移）
- [ ] **REP-09**: 图表类型自动匹配数据特征
- [ ] **REP-10**: PDF 导出提示（Ctrl/Cmd + P）

### User Experience

- [ ] **UX-01**: Skill 触发关键词识别（"分析数据"、"做报告"、"做PPT"、"Excel"、"投放分析"等）
- [ ] **UX-02**: 快速响应模式（简单查询直接输出，不启动多专家流程）
- [ ] **UX-03**: 进度提示（Phase 阶段切换时显示进度）
- [x] **UX-04**: 错误友好提示（文件读取失败、格式不支持等场景）

---

## v2 Requirements (Deferred)

### Advanced Analysis

- [ ] **ADV-01**: 时间序列预测（趋势预测、季节性分析）
- [ ] **ADV-02**: 相关性深入分析（因果推断辅助）
- [ ] **ADV-03**: 异常检测自动化（IQR、Z-score、ML 方法）
- [ ] **ADV-04**: 统计假设检验（t-test、chi-square、ANOVA）

### Report Enhancements

- [ ] **REP-V2-01**: 英文报告生成支持
- [ ] **REP-V2-02**: 自定义设计风格参数
- [ ] **REP-V2-03**: 交互式 HTML 报告（筛选、钻取）
- [ ] **REP-V2-04**: 报告模板保存和复用

### Integration

- [ ] **INT-V2-01**: 数据库连接（PostgreSQL、MySQL）
- [ ] **INT-V2-02**: API 数据接入（REST API）
- [ ] **INT-V2-03**: 实时数据流（Kafka、WebSocket）

---

## Out of Scope

- **实时数据接入** — 仅处理静态文件（Excel/CSV/JSON），不接入数据库或 API 实时流。理由：保持 skill 定位清晰，避免运维复杂度。

- **英文报告生成** — v1 保持中文优先。理由：目标用户中文环境，v1 聚焦核心价值。

- **自定义设计风格** — v1 使用现有 11 种风格。理由：已验证的设计系统，无需重新设计。

- **数据清洗工具** — 假设用户已准备好数据。理由：数据清洗是独立领域，会增加复杂度。

- **自动化 ML 训练** — 不做模型训练或预测服务。理由：定位为分析报告，不是 ML 平台。

- **Dashboard Builder** — 不做可定制 Dashboard。理由：输出是静态报告，不是实时 Dashboard。

---

## Definition of Done

**Phase Done Criteria:**

1. ✅ 所有 REQ-ID 标记的需求已实现
2. ✅ 代码无硬编码路径
3. ✅ 使用 logging 模块而非 print
4. ✅ 所有数值计算有代码支撑（非 LLM mental math）
5. ✅ 报告输出符合设计风格规范
6. ✅ 中文输出质量验证（人工审核）

---

## Traceability

| REQ-ID | Phase | Description | Status |
|--------|-------|-------------|--------|
| INF-01 | Phase 1: Infrastructure | requirements.txt 创建 | Pending |
| INF-02 | Phase 1: Infrastructure | pathlib 跨平台路径 | Pending |
| INF-03 | Phase 1: Infrastructure | logging 替换 print | Pending |
| INF-04 | Phase 1: Infrastructure | Git 初始化 | Pending |
| INF-05 | Phase 1: Infrastructure | 文件结构规范化 | Pending |
| DATA-01 | Phase 2: Data Processing | 数据文件加载 | Complete (02-02a, 02-02b) |
| DATA-02 | Phase 2: Data Processing | 数据概览输出 | Complete (02-03a) |
| DATA-03 | Phase 2: Data Processing | 数据类型识别 | Complete (02-04) |
| DATA-04 | Phase 2: Data Processing | 基础统计分析 | Complete (02-03a) |
| DATA-05 | Phase 2: Data Processing | 初步洞察输出 | Complete (02-05) |
| DATA-06 | Phase 2: Data Processing | 大数据集 chunking | Complete (02-06) |
| DATA-07 | Phase 2: Data Processing | 缺失值报告 | Complete (02-03b) |
| UX-04 | Phase 2: Data Processing | 错误友好提示 | Complete (02-02b) |
| CLAR-01 | Phase 3: Analysis Engine | 澄清流程可选 | Pending |
| CLAR-02 | Phase 3: Analysis Engine | 3 个核心问题 | Pending |
| CLAR-03 | Phase 3: Analysis Engine | context.md 写入 | Pending |
| CLAR-04 | Phase 3: Analysis Engine | 快速跳过选项 | Pending |
| CLAR-05 | Phase 3: Analysis Engine | 智能触发判断 | Pending |
| EXPT-01 | Phase 3: Analysis Engine | Expert Selector | Pending |
| EXPT-02 | Phase 3: Analysis Engine | 专家角色库 | Pending |
| EXPT-03 | Phase 3: Analysis Engine | subagent 并行 | Pending |
| EXPT-04 | Phase 3: Analysis Engine | 专家陈述写入 | Pending |
| EXPT-05 | Phase 3: Analysis Engine | 上下文隔离 | Pending |
| EXPT-06 | Phase 3: Analysis Engine | 独立输出文件 | Pending |
| EXPT-07 | Phase 3: Analysis Engine | 强制代码计算 | Pending |
| EXPT-08 | Phase 3: Analysis Engine | 矛盾检测标记 | Pending |
| REP-01 | Phase 4: Report Generation | HTML 报告生成 | Pending |
| REP-02 | Phase 4: Report Generation | PPT 生成 | Pending |
| REP-03 | Phase 4: Report Generation | 设计风格选择 | Pending |
| REP-04 | Phase 4: Report Generation | 中文优先输出 | Pending |
| REP-05 | Phase 4: Report Generation | 结论式标题 | Pending |
| REP-06 | Phase 4: Report Generation | Manager-POV Synthesis | Pending |
| REP-07 | Phase 4: Report Generation | 报告结构规范 | Pending |
| REP-08 | Phase 4: Report Generation | 单一风格源 | Pending |
| REP-09 | Phase 4: Report Generation | 图表类型匹配 | Pending |
| REP-10 | Phase 4: Report Generation | PDF 导出提示 | Pending |
| UX-01 | Phase 5: Integration | 触发关键词识别 | Pending |
| UX-02 | Phase 5: Integration | 快速响应模式 | Pending |
| UX-03 | Phase 5: Integration | 进度提示 | Pending |

---

*Last updated: 2026-06-04 after 02-05 completion*