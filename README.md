# 标准编写工作流技能

本仓库集中管理中文标准编写相关技能，用于组织资料检索、标准 Markdown 编写、机械审校、清单审查和 Word 生成。

## 技能目录

| 目录 | 职责 |
| --- | --- |
| `standard-drafting-workflow` | 标准编写流程：收集需求、检索资料、阅读来源、整理证据、组织草稿、安排审校和交付。 |
| `standard-audit-workflow` | 标准审校流程：调用机械审校器，整理问题，执行机械规则难以覆盖的清单审查。 |
| `md2std-standard` | 生成器使用说明：维护 md2std Markdown 输入契约和 DOCX 生成调用脚本。 |

## 配套项目

本仓库只维护工作流技能，不复制工具源码。配套项目如下：

| 项目 | 用途 |
| --- | --- |
| [MdToStandardWord](https://github.com/LoyDgIk/MdToStandardWord) | 将标准 Markdown 转换为 Word `.docx`。 |
| [md2std-standard-auditor](https://github.com/LoyDgIk/md2std-standard-auditor) | 对标准 Markdown 做机械审校。 |
| [GBMCP](https://github.com/LoyDgIk/GBMCP) | 检索标准信息、详情和可下载文本。 |
| [CKCEST-MCP](https://github.com/LoyDgIk/CKCEST-MCP) | 检索政策、科研项目和统计数据。 |

## 本地安装

将本仓库中的三个技能目录链接到本地技能目录。下面命令中的占位路径按实际环境替换：

```powershell
New-Item -ItemType SymbolicLink -Path <skills-dir>\standard-drafting-workflow -Target <repo-root>\standard-drafting-workflow
New-Item -ItemType SymbolicLink -Path <skills-dir>\standard-audit-workflow -Target <repo-root>\standard-audit-workflow
New-Item -ItemType SymbolicLink -Path <skills-dir>\md2std-standard -Target <repo-root>\md2std-standard
```

`md2std-standard-auditor` 可安装到当前 Python 环境，也可通过环境变量指定源码位置：

```powershell
set MD2STD_AUDITOR_ROOT=<path-to-md2std-standard-auditor>
```

`md2std` 生成器依赖由 `md2std-standard/scripts/requirements.txt` 固定到 release tag。

## 推荐流程

1. 使用 `standard-drafting-workflow` 收集需求、检索并阅读来源。
2. 编写或修订符合 `md2std-standard` 输入契约的 Markdown。
3. 使用 `standard-audit-workflow` 执行机械审校和清单审查。
4. 修复阻塞问题和必须修改项。
5. 使用 `md2std-standard` 调用生成器输出 Word。

机械审校通过只表示 Markdown 未触发已知规则错误，不代表技术内容已经通过专家审查。
