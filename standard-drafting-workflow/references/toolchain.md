# 工具链参考

本 skill 需要串联多个已有工具。使用时优先读取和遵守对应工具自己的 skill 说明，本文件只规定全流程中的职责边界。

## 职责总览

| 工具 | 本流程中的职责 | 不承担的职责 |
| --- | --- | --- |
| standard-drafting-workflow | 证据检索、资料阅读、草稿组织、审校任务委托、修订计划、交付确认 | 不复制审校规则，不生成 DOCX |
| standard-audit-workflow | 机械校验、AI 清单审查、审校报告 | 不检索标准源，不生成 DOCX |
| GBMCP | 标准检索、标准详情、可下载标准文本 | 不负责起草、审校、排版 |
| CKCEST | 政策、项目、统计数据检索 | 不负责起草、审校、排版 |
| md2std-standard-auditor | Markdown 确定性审校规则和报告 | 不生成 DOCX，不决定资料证据是否充分 |
| md2std-standard | md2std 生成器输入约定和 DOCX 生成包装 | 不编排审校流程，不维护审校规则 |
| MdToStandardWord / md2std | Markdown 转 DOCX 排版生成 | 不负责证据检索或标准内容审校 |

## GBMCP 标准检索和下载

优先用途：

- 查找真实标准编号、名称、状态、发布/实施日期、ICS/CCS、归口/起草信息。
- 下载可公开获取的标准正文、行业标准、食品安全标准、生态环境/卫生健康/应急管理/计量/ITU 文档。
- 为规范性引用文件和参考文献提供真实来源。
- 支撑草案条款前，必须阅读下载的标准正文或详情页内容；不要只依据检索结果标题编写要求。

使用原则：

- 普通国家标准元数据：用 SAMR / openstd 相关工具。
- 可下载 GB/GB/T/GB/Z：先查可下载源，再下载。
- 行业或领域标准按来源选择 NHC、MEE、MEM、CFSA、RESMEA、ITU 等。
- Doc88 只作为补充下载路径，不作为首选权威元数据来源。
- 搜索、详情、下载分步执行；不要把元数据工具当下载工具。
- 规范性引用文件只选对本标准条款不可缺少的文件。优先少而准，最好少于 8 篇。

参考 companion skill：`gbmcp-standards`。

## CKCEST 数据、政策和项目检索

优先用途：

- 查政策依据、监管要求、行业发展背景、政策趋势。
- 查科研项目、技术方向、承担机构、资助机构等研发背景。
- 查统计数据，用真实指标支撑范围、现状、指标设定或编制说明。
- 标准正文中的数据、年份、项目数量、国家/地区对比、政策事实必须来自 CKCEST 返回结果或用户提供资料，不得伪造。

使用原则：

- 政策库用于政策文件、法规、规划文本、政策解读。
- 全球科研项目库用于技术路线、研究热点、项目分布。
- 全球统计数据库用于数据中心、指标概览、国家/地区对比。
- 需要登录时先按 `ckcest` skill 执行 `check_login` / `set_cookie` / `stats_check_login`。
- 多项对比必须先用 `get_compare_options` 获取真实指标和国家 ID，不能猜 ID。
- 如果数据库无结果，应写明未取得数据或换源检索，不要补写看似合理的数字。

参考 companion skill：`ckcest`。

## 文档提取和摘要

适用输入：

- 用户提供的 PDF、CAJ、DOCX、网页、标准正文、政策全文、项目详情、统计导出表。

处理原则：

- 对下载的标准或政策文档，先提取结构化文本，再摘要。
- 编写标准前必须阅读/抽取所有会影响条款的下载标准、政策、文献和用户资料。
- 摘要时保留可追溯来源：文件名、标准号/政策号、发布日期、页码或章节位置。
- 只把能回溯到来源的事实写入标准正文或编制依据；无法确认的数据标记为待核实。
- 从来源中提取术语、定义、指标、试验方法、限值、分类、流程和引用文件候选。

如果本地有 MinerU 或其他文档提取 skill，优先按该 skill 的流程处理 PDF/MinerU Markdown。

## md2std 写作和转换

优先用途：

- 按 `md2std-standard` 的生成器输入约定组织 Markdown。
- 使用 YAML front matter 管理封面、前言、引言元数据。
- 生成 DOCX。

关键命令：

```powershell
# 在 md2std-standard skill 根目录执行
python -X utf8 scripts/run_md2std.py input.md -o output.docx
```

最终交付前如需 Word 域更新、分页和续表：

```powershell
# 在 md2std-standard skill 根目录执行
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

参考 companion skill：`md2std-standard`。

## 审校技能

用法：

```powershell
# 在 standard-audit-workflow skill 根目录执行
python -X utf8 scripts/run_mechanical_audit.py input.md
python -X utf8 scripts/run_mechanical_audit.py input.md --json
```

边界：

- `standard-drafting-workflow` 负责把草稿和证据交给 `standard-audit-workflow`，再根据审校报告组织修订。
- `standard-audit-workflow` 负责运行机械校验，并按 AI 清单审查机械规则无法覆盖的内容。
- 机械审校规则清单以 `md2std-standard-auditor` 的 README 和测试为准，本文件不复制规则。
- AI 审查清单以 `standard-audit-workflow/references/ai-review-checklist.md` 为准。
- 脚本只做机械审校。条款类型、术语定义质量、数据真实性和技术合理性仍需按 `SKILL.md` 工作流人工/模型复核。
