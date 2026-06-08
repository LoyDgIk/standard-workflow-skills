# md2std Standard Skill

这是 `md2std` 的 Codex Skill，用于说明生成器输入约定并调用排版生成器转换中文标准 Markdown。排版生成器本体在独立仓库维护：[LoyDgIk/MdToStandardWord](https://github.com/LoyDgIk/MdToStandardWord)。

本 skill 不承载审校流程。标准审校由 `standard-audit-workflow` 承担：机械校验通过独立项目 `md2std-standard-auditor` 执行，AI 清单审查在审校 skill 中完成。

本目录就是 skill 内容，可以直接作为 Codex skill 安装或链接到 Codex skills 目录。

## 内容

```text
SKILL.md             Skill 主说明
agents/openai.yaml   Codex UI 元数据
examples/            Skill 内部示例 Markdown
scripts/             Skill 调用脚本
```

`scripts/` 只放轻量包装和依赖声明，不复制 CLI 源码：

```text
scripts/run_md2std.py        调用已安装的 md2std.cli.main
scripts/requirements.txt     固定引用 CLI 仓库 tag
```

当前 CLI 依赖：

```text
md2std @ git+https://github.com/LoyDgIk/MdToStandardWord.git@v0.1.2
```

## 安装依赖

首次使用或当前 Python 环境中没有 `md2std` 时，在本仓库根目录执行：

```powershell
python -m pip install -r scripts/requirements.txt
```

该命令会从 CLI 仓库的固定 tag 安装 `md2std`。固定 tag 的目的是保证生成器行为可复现，不跟随 `main` 的临时变更。

## 转换示例

使用 skill wrapper 转换示例文件：

```powershell
python -X utf8 scripts/run_md2std.py examples/智能井盖运行维护规范.md -o examples/智能井盖运行维护规范.docx
```

指定国家标准：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --kind national
```

最终交付前启用 Word COM 后处理：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --word-com-postprocess
```

Word COM 后处理仅适用于安装 Microsoft Word 的 Windows 环境，用于更新域、重新分页并按 Word 实际分页处理续表。

如需让封面旧式下拉框打开 Word 后即可选择并刷新显示，可启用封面表单保护：

```powershell
python -X utf8 scripts/run_md2std.py input.md -o output.docx --cover-form-protection
```

该参数只保护封面节，正文节保持可编辑。也可在 YAML front matter 中写 `cover_form_protection: true` 固定启用；命令行 `--cover-form-protection` / `--no-cover-form-protection` 优先于 YAML。草案版次用 `draft_version` 设置，例如 `draft_version: （征求意见稿）`。

## Skill 使用范围

适合使用本 skill 的任务：

- 起草 GB/T 风格标准、团体标准、国家标准 Markdown。
- 将 PDF/MinerU 转出的 Markdown 规范化为 `md2std` 语法。
- 修复表、图、公式题注和交叉引用。
- 生成标准文本 `.docx`。

核心规则：

- 不手写章条编号、表号、图号、公式号。
- 不使用旧交叉引用语法 `{@id}`。
- 不使用 LaTeX `\tag{...}`。
- 表、图、公式锚点分别使用 `#tbl:id`、`#fig:id`、`#eq:id`。
- 交叉引用使用 `{{tbl:id}}`、`{{fig:id:label}}`、`{{eq:id:label}}`。
- 封面草案版次使用 YAML `draft_version`，常用值包括 `草案版次选择`、`（工作组讨论稿）`、`（征求意见稿）`、`（送审讨论稿）`、`（送审稿）`、`（报批稿）`。
- 行内角标支持 Typora/Obsidian 风格扩展 Markdown：上标用 `^...^`，如下 `2^10^`；下标用 `~...~`，如下 `H~2~O`。兼容 `<sup>...</sup>`、`<sub>...</sub>`，但推荐使用 `^...^`、`~...~`。
- 需要与公式字体一致的行内变量可写 `$$T_r$$`、`$$Q_e$$`，生成 Word 原生行内公式；表格单元格、表内注、图内段、来源和脚注也统一使用 `$$...$$`。
- 表、图的单位、来源、脚注使用紧跟目标后的通用块标记：`{单位} ...`、`{来源} ...`、`{脚注} ...`。
- 表格单元格内普通注使用 `〔注：...〕`，单元格可以只有注；表格脚注引用点使用 `〔脚注〕`，脚注内容用块级 `{脚注} ...`，编号由 Word 样式自动生成。
- HTML 表格支持 `rowspan`、`colspan`、空单元格和边框属性 `data-border-outer/inner/top/right/bottom/left`，边框值为 `none`、`thin`、`thick`；表头单元格底线默认使用粗线。
- 组合分图使用 `{图：#fig:id} 图题`、`{分图组:2}` 和后续连续图片块；`{图标引}` 自动编号，`{图段}` 表示图内段落。
- 多块示例用 `{示例结束}` 结束；无结束标记时保留单段示例写法。

完整写作规则见 `SKILL.md`。

## 维护流程

CLI 仓库发布新版本时：

1. 在 `LoyDgIk/MdToStandardWord` 提交 CLI 改动。
2. 运行 CLI 测试和转换验证。
3. 创建并推送新 tag。
4. 在本仓库更新 `scripts/requirements.txt` 中的 tag。
5. 用 `scripts/run_md2std.py` 转换 `examples/智能井盖运行维护规范.md` 验证。
6. 在统一 workflow skills 仓库中提交更新。

不要把 CLI 源码复制进本 skill；保持 `scripts/` 只引用固定版本的 CLI 包。

## 验证

在已安装依赖后执行：

```powershell
python -X utf8 scripts/run_md2std.py examples/智能井盖运行维护规范.md -o "$env:TEMP/md2std-skill-test.docx"
```

如果转换看到 `OK -> ...docx` 并输出文件非空，说明 skill wrapper 和生成器依赖可用。
