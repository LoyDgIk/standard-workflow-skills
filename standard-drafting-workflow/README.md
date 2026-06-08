# 标准编写工作流

本目录维护中文标准编写流程说明，用于从主题需求推进到标准 Markdown、审校结果和 Word 交付物。

## 职责边界

- 本技能负责需求梳理、资料检索、来源阅读、证据整理、草稿组织、审校委托、修订计划和交付检查。
- `standard-audit-workflow` 负责审校流程；机械审校规则只在 `md2std-standard-auditor` 中维护。
- `md2std-standard` 负责生成器输入约定和 DOCX 生成调用脚本。
- `MdToStandardWord` / `md2std` 负责 Markdown 到 Word 的排版生成。
- GBMCP 只作为标准查询和文本下载工具使用。

## 配套工具

| 工具 | 用途 |
| --- | --- |
| GBMCP | 检索标准、查看详情、下载可获取的标准文本。 |
| CKCEST | 检索政策、科研项目和统计数据。 |
| `md2std-standard-auditor` | 执行标准 Markdown 机械审校。 |
| `md2std-standard` | 说明 md2std 输入契约并调用生成器。 |
| `MdToStandardWord` | 生成 Word `.docx`。 |

## 基本流程

1. 明确标准主题、标准化对象、适用范围、标准类型、目标用户和交付格式。
2. 通过 GBMCP 检索真实标准，必要时下载标准文本。
3. 通过 CKCEST 检索真实政策、科研项目、统计指标或行业数据。
4. 编写标准前阅读已下载的标准、文献和用户材料。
5. 提取证据，记录来源标题、编号、发布机构、日期、链接、工具结果和下载文件名。
6. 只把确实构成条款依据的文件列入规范性引用文件。
7. 技术数据、日期、标准编号、政策名称、指标、限值和试验方法必须能追溯到来源或用户材料。
8. 编写符合 `md2std-standard` 输入契约的 Markdown。
9. 委托 `standard-audit-workflow` 审校，修复机械 `error` 和清单审查中的 `必须修改`。
10. 使用 `md2std-standard` 转换为 Word。

## 常用命令

机械审校：

```powershell
# 在 standard-audit-workflow 目录执行
python -X utf8 scripts/run_mechanical_audit.py input.md
```

输出 JSON 审校结果：

```powershell
# 在 standard-audit-workflow 目录执行
python -X utf8 scripts/run_mechanical_audit.py input.md --json
```

转换为 Word：

```powershell
# 在 md2std-standard 目录执行
python -X utf8 scripts/run_md2std.py input.md -o output.docx
```

启用 Word COM 后处理：

```powershell
# 在 md2std-standard 目录执行
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

## 交付检查

最终交付应说明：

- 标准 Markdown 文件。
- Word 文件。
- 已使用的标准、政策、统计数据、文献和用户材料。
- 已阅读的下载文件清单。
- 机械审校结果和清单审查结论。
- md2std 转换状态。
- 未核实内容和需要专家确认的问题。

机械审校通过不等于技术内容已经通过专家审查。涉及安全、健康、计量、检测方法和合规边界的条款，应由专业人员复核。
