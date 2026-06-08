# Standard Drafting Workflow

这是用于编写中文标准的 Codex skill，覆盖从用户主题意图收集、真实资料检索、标准和文献阅读、证据归纳、标准 Markdown 编写、审校修订编排到 Word 转换的全流程。

本技能不单独承担全部能力，需要按照仓库的其他配套项目一起使用：

- GBMCP：标准检索、标准详情查看和标准文本下载。
  - 远程仓库：`https://github.com/LoyDgIk/GBMCP`
- CKCEST-MCP：政策、科研项目、统计数据等真实数据库检索。
  - 远程仓库：按实际使用的 CKCEST-MCP 项目配置。
- md2std CLI：把标准 Markdown 转换为 Word 文档。
  - 远程仓库：`https://github.com/LoyDgIk/MdToStandardWord`
- md2std Standard Skill：提供 md2std 生成器输入约定、示例和 DOCX 生成包装脚本。
  - 本仓库子目录：`md2std-standard`
- md2std Standard Auditor：提供确定性 Markdown 审校规则和审校报告。
  - 远程仓库：`https://github.com/LoyDgIk/md2std-standard-auditor`
- standard-audit-workflow：编排标准审校任务，包含机械校验和 AI 清单审查。
  - 本仓库子目录：`standard-audit-workflow`

## 职责边界

- 本 skill 负责标准编写流程、证据纪律、审校任务委托、修订计划和最终交付清单。
- 审校流程由 `standard-audit-workflow` 承担；机械审校规则只在 `md2std-standard-auditor` 中维护。
- DOCX 生成只由 `md2std` / `MdToStandardWord` 承担；本仓库不维护排版生成源码。
- `md2std-standard` 只作为生成器 skill 使用，不承载审校流程。
- GBMCP 只作为标准查询/下载工具使用，本 skill 不修改 GBMCP。

## 使用方式

建议在标准编写项目中启用本技能，并同时启用 `gbmcp-standards`、`ckcest` 和 `md2std-standard` 等配套技能。自述只描述仓库职责和通用命令。

## 必须遵守的流程

1. 收集用户的标准主题、标准化对象、适用范围、标准类型、目标用户和交付格式。
2. 通过 GBMCP 检索真实标准，必要时下载标准文本。
3. 通过 CKCEST-MCP 检索真实政策、科研项目、统计指标或行业数据。
4. 编写标准前，必须阅读已下载的标准、文献和用户提供材料，不能只依赖搜索结果摘要。
5. 提取并总结证据，记录来源标题、编号、发布机构、日期、URL、工具结果和下载文件名。
6. 规范性引用文件只保留真正构成标准条款依据的文件，数量应尽量少，最好少于 8 篇；达到 8 篇及以上时，应说明每一篇不可替代的必要性。
7. 所有技术数据、日期、标准编号、政策名称、指标、限值、试验方法必须来自数据库检索结果、下载文档或用户材料，不能伪造。
8. 编写 md2std Markdown，分清 `# 规范性引用文件` 和 `# 参考文献`。
9. 委托 `standard-audit-workflow` 审校，修复机械 `error` 和 AI `必须修改`，人工复核 `warning` / `建议复核`。
10. 使用 md2std 包装脚本转换为 Word。

## 常用命令

机械审校标准 Markdown：

```powershell
# 在 standard-audit-workflow skill 根目录执行
python -X utf8 scripts/run_mechanical_audit.py input.md
```

输出 JSON 审校结果：

```powershell
# 在 standard-audit-workflow skill 根目录执行
python -X utf8 scripts/run_mechanical_audit.py input.md --json
```

转换为 Word：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx
```

需要 Word COM 后处理时：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

## 交付要求

最终交付时应包含：

- 标准 Markdown 文件。
- Word 文件。
- 使用过的标准、政策、统计数据、文献和用户材料摘要。
- 已阅读的下载文件清单；未阅读的材料必须明确列为剩余工作。
- 审校脚本结果和 md2std 转换状态。
- 未核实或需要专家确认的内容。

机械审校通过不等于技术内容已经专家审查通过。涉及安全、健康、计量、检测方法、合规边界的条款仍需要专业人员复核。
