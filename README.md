# Kang Agent Workforce

[![status](https://img.shields.io/badge/status-public%20release-2ea44f)](https://github.com/KanG-ciyuan/kang-agent-workforce/releases)
[![version](https://img.shields.io/github/v/release/KanG-ciyuan/kang-agent-workforce?label=version)](https://github.com/KanG-ciyuan/kang-agent-workforce/releases)
[![core skills](https://img.shields.io/badge/core%20skills-4-0969da)](#岗位技能)
[![tests](https://img.shields.io/badge/local%20tests-3%20passed-2ea44f)](tests/)
[![license](https://img.shields.io/badge/license-Kang%20terms-6f42c1)](LICENSE)

Kang 的可复用产品研发数字员工团队。它把产品架构、企业流程、B2B UX 和产品验收拆成可以显式调用、独立交接和独立验收的 Skills。

## 它解决什么问题

它不是企业流程诊断产品本身，也不是员工摸排 Agent。它解决的是“如何让多个专业岗位协作完成产品研发审查和交付”的问题：谁先做、依据什么、交给谁、失败如何退回、什么时候必须由 Kang 决策。

## 岗位技能

总控不会把岗位正文嵌套进自己的安装目录，而是通过明确名称关联四个独立仓库：

| 数字员工 | 独立 Skill | 负责什么 |
|---|---|---|
| 产品架构 | [`kang-product-architect`](https://github.com/KanG-ciyuan/kang-product-architect) | 入口、角色、权限、页面边界 |
| 企业流程 | [`kang-enterprise-process-reviewer`](https://github.com/KanG-ciyuan/kang-enterprise-process-reviewer) | 流程责任、证据门、失败升级 |
| B2B UX | [`kang-b2b-ux-auditor`](https://github.com/KanG-ciyuan/kang-b2b-ux-auditor) | 任务可理解性、导航、状态反馈 |
| 产品验收 | [`kang-product-acceptance-auditor`](https://github.com/KanG-ciyuan/kang-product-acceptance-auditor) | 场景验收、证据、发布阻塞 |

安装总控后，按需安装岗位 Skill；总控 README 和 `SKILL.md` 是关联入口，不会把四个岗位的全文塞进当前上下文。

## 目录

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 总控编排 Skill，可用 `$kang-agent-workforce` 显式调用 |
| `contracts/` | 跨岗位交接合同和证据状态 |
| `evals/` | 触发与输出评估用例 |
| `reports/` | 发布和验证证据 |

## 显式调用

```text
$kang-agent-workforce
```

总控再按任务需要点名岗位：

```text
$kang-product-architect
$kang-enterprise-process-reviewer
$kang-b2b-ux-auditor
$kang-product-acceptance-auditor
```

Skill 正文不会预加载到所有项目上下文。调用时只加载当前岗位所需的说明和交接材料。

## 边界

数字员工是“岗位规则 + 临时子代理 + 项目上下文 + 交接文件”的工作单元，不是拥有永久记忆、独立商业决策权或生产权限的真人替代品。产品方向、业务取舍、发布和高风险操作必须由 Kang 批准。

## 安装

本仓库只安装总控 Skill。四个岗位是独立 Skill 包，分别安装到 Codex 的个人 Skills 目录；不要把多个可发现的 `SKILL.md` 嵌套进总控安装目录，否则会产生重复发现或调用歧义。当前仓库不包含密钥，也不要求任何外部服务凭据。

从 GitHub 安装前，请确认本机已有 Git、Node.js/npm 和 Codex：

```bash
git --version
node --version
npx --version
```

## 前置条件

- [ ] 已安装 Git：`git --version`
- [ ] 已安装 Node.js 与 npx：`node --version && npx --version`
- [ ] 已安装 Codex，并能访问个人 Skills 目录
- [ ] 已阅读各岗位权限边界，知道实现、部署和发布需要人工批准

通过 Agent Skills 安装器查看并安装：

```bash
npx skills add KanG-ciyuan/kang-agent-workforce --list
npx skills add KanG-ciyuan/kang-agent-workforce
npx skills add KanG-ciyuan/kang-product-architect
npx skills add KanG-ciyuan/kang-enterprise-process-reviewer
npx skills add KanG-ciyuan/kang-b2b-ux-auditor
npx skills add KanG-ciyuan/kang-product-acceptance-auditor
```

安装后可以这样验证：

```bash
find "${CODEX_HOME:-$HOME/.codex}/skills" -maxdepth 2 -name SKILL.md -print | grep 'kang-'
python3 "${CODEX_HOME:-$HOME/.codex}/skills/kang-meta-skill/scripts/validate_skill.py" "${CODEX_HOME:-$HOME/.codex}/skills/kang-agent-workforce"
```

## 你可以直接这样说

在 Codex 中可以直接说：

- “使用 `$kang-agent-workforce` 审查当前项目，先只读，不修改代码。”
- “使用 `$kang-product-architect` 检查这个 SaaS 的入口、角色权限和完成标准。”
- “使用 `$kang-enterprise-process-reviewer` 检查员工提交到负责人决策的交接依据。”
- “使用 `$kang-b2b-ux-auditor` 判断一线员工进入后是否知道第一步做什么。”
- “使用 `$kang-product-acceptance-auditor` 从干净入口做独立验收，不要在验收中修代码。”

## Troubleshooting

**Codex 显示两个同名 Skill**

检查是否把岗位仓库重复嵌套进总控目录。总控和四个岗位必须是五个独立入口。

**总控没有调用预期岗位**

在任务中显式写出 `$kang-...` 名称，并指定输入文件、输出文件和权限。自动发现只是便利机制，正式流程不依赖自动猜测。

**子代理读到了过多上下文**

只向该岗位传递当前交接文件和必要项目证据。不要把所有岗位 Skill 正文或之前所有对话一次性传给子代理。

**验收 Agent 一边验收一边修复**

停止该轮验收并重新调用 `$kang-product-acceptance-auditor`。验收岗位必须独立，只报告证据、严重度和退回岗位。

<!-- kang-author:start -->
## About Kang

Maintained by Kang. GitHub: https://github.com/KanG-ciyuan/

<!-- kang-author:end -->

## License

Copyright (c) Kang. See [LICENSE](LICENSE).

## Author

Created and maintained by [Kang](https://github.com/KanG-ciyuan).
