# md2std 标准生成技能

本目录维护 `md2std` 的输入约定和生成调用脚本，用于把中文标准 Markdown 转换为 Word `.docx`。生成器本体在 [MdToStandardWord](https://github.com/LoyDgIk/MdToStandardWord) 维护。

本技能不负责标准内容审校。审校流程由 `standard-audit-workflow` 组织，机械规则由 [md2std-standard-auditor](https://github.com/LoyDgIk/md2std-standard-auditor) 维护。

## 目录内容

```text
SKILL.md             技能主说明
agents/openai.yaml   本地界面元数据
examples/            示例 Markdown
scripts/             调用脚本和依赖声明
```

`scripts/` 只放轻量调用脚本，不复制生成器源码：

```text
scripts/run_md2std.py        调用已安装的 md2std.cli.main
scripts/requirements.txt     固定引用 MdToStandardWord 的 release tag
```

当前生成器依赖：

```text
md2std @ git+https://github.com/LoyDgIk/MdToStandardWord.git@v0.1.2
```

## 安装依赖

首次使用或当前 Python 环境中没有 `md2std` 时，在本目录执行：

```powershell
python -m pip install -r scripts/requirements.txt
```

固定 tag 用于保证生成结果可复现。

## 转换命令

转换示例文件：

```powershell
python -X utf8 scripts/run_md2std.py examples/智能井盖运行维护规范.md -o examples/智能井盖运行维护规范.docx
```

指定国家标准：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --kind national
```

启用 Word COM 后处理：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

启用封面旧式下拉框表单保护：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --cover-form-protection
```

`--word-com-postprocess` 仅适用于安装 Microsoft Word 的 Windows 环境。`--cover-form-protection` 只保护封面节，正文节仍可编辑。

## 输入规则摘要

- 不手写章条编号、表号、图号、公式号。
- 不使用旧交叉引用语法 `{@id}`。
- 不使用 LaTeX `\tag{...}`。
- 表、图、公式锚点分别使用 `#tbl:id`、`#fig:id`、`#eq:id`。
- 交叉引用使用 `{{tbl:id}}`、`{{fig:id:label}}`、`{{eq:id:label}}`。
- 标准编号中的年份连接号使用 `—`，例如 `GB/T 1.1—2020`。
- 参考文献条目不手写 `[1]`、`[2]`；编号由 Word 样式生成。
- 封面草案版次使用 YAML `draft_version`。
- 行内上标使用 `^...^`，行内下标使用 `~...~`。
- 数学变量如需保持公式字体，可写行内公式 `$$T_r$$`、`$$Q_e$$`。
- `# 范围`、`# 规范性引用文件`、`# 术语和定义`、`# 符号和缩略语` 内不使用 `{无标题条:n}`；这些基础章直接写普通段落、引用文件条目、符号条目或术语块。
- `{无标题条:n}` 只用于“术语和定义”之后的技术章或附录。
- `# 规范性引用文件` 的固定导语可省略，生成器会补齐；有清单时每条用行首 `{{std:id}}` 注册，例如 `{{std:GB/T 11615}} GB/T 11615  地热资源地质勘查规范`；无引用时可写 `本文件没有规范性引用文件。`，空章也会自动补齐。
- `# 术语和定义` 的默认导语和无术语说明可省略，生成器会补齐；仅引用外部术语或同时引用外部术语并列本文件术语时，应显式写对应导语。
- 普通英文术语对应词不加斜体；拉丁学名、生物分类学名称等需要斜体时，在英文对应词中使用 Markdown 斜体，例如 `{术语：大肠埃希氏菌 | *Escherichia coli*}`。
- `# 符号和缩略语` 如需区分“符号”“缩略语”或二者兼有，可显式写 `下列符号适用于本文件。`、`下列缩略语适用于本文件。` 或 `下列符号和缩略语适用于本文件。`；省略时生成器补默认导语。
- 表、图的单位、来源、脚注使用紧跟目标后的 `{单位}`、`{来源}`、`{脚注}`。
- 表格单元格内普通注使用 `〔注：...〕`，脚注引用点使用 `〔脚注〕`。
- HTML 表格支持 `rowspan`、`colspan`、空单元格、边框属性和 `data-align="left|center|right|decimal"`。
- 组合分图使用 `{图：#fig:id} 图题`、`{分图组:n}` 和后续连续图片块。
- 多块示例用 `{示例结束}` 结束。

完整输入规则见 `SKILL.md`。

## 维护流程

`MdToStandardWord` 发布新版本后：

1. 在生成器仓库完成提交、测试和 tag。
2. 更新本目录 `scripts/requirements.txt` 中引用的 tag。
3. 转换示例文件确认调用脚本可用。
4. 在 `standard-workflow-skills` 仓库提交更新。

## 验证

在已安装依赖后执行：

```powershell
python -X utf8 scripts/run_md2std.py examples/智能井盖运行维护规范.md -o "$env:TEMP/md2std-skill-test.docx"
```

看到 `OK -> ...docx` 且输出文件非空，即表示调用脚本和生成器依赖可用。
