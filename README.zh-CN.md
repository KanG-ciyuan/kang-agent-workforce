# Kang Agent Workforce

[English](README.md) | 简体中文

[![Release](https://img.shields.io/github/v/release/KanG-ciyuan/kang-agent-workforce?display_name=tag&sort=semver&style=flat-square)](https://github.com/KanG-ciyuan/kang-agent-workforce/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/KanG-ciyuan/kang-agent-workforce?style=flat-square)](https://github.com/KanG-ciyuan/kang-agent-workforce/commits/main)

**一个角色化的 AI 产品团队：责任显式、交接有合同、复核有独立关卡、人工决策有边界。**

一个总控 Skill 点名四个岗位 Skill，固定调用顺序，并要求每一步之间都有落盘的交接记录。不要让一个 Agent 同时定义需求、检查流程、审核体验，最后再验收自己的工作。

`kang-agent-workforce` 是一份**协同规范，不是运行时**。`SKILL.md`（44 行）就是本仓库的全部行为内容，仓库里没有任何编排代码。它面向的是这样一类使用者：已经在用支持 Skill 的 Agent 运行时，希望真实产品工作有岗位分工，而不是由一个通用 Agent 从头做到尾。本公开仓库只包含可复用的编排逻辑；企业 AI 流程诊断产品及其私有运行时 Skills 是独立项目，不在这里。

## 为什么不能只靠一个通用 Agent？

总控自己的指令已经把前提说清楚了（`SKILL.md:11`）：

> You are the coordinator for a small, explicit product-development team. You do not pretend to be all specialists at once. You select the smallest set of named Kang Skills, pass only the required project artifacts, and preserve a reviewable handoff.

一个 Agent 写完需求、检查完流程、审核完体验，再给自己的产出签字验收，它的结论无法被反驳——因为它产出的所有东西都互相印证。`SKILL.md` 里有四条规则专门针对这种"自我印证"。

| 规则 | 原文 |
| --- | --- |
| 一次只加载一个岗位 | `Load a specialist's full instructions only for that specialist's turn.`（`SKILL.md:22`） |
| 交接的是文件，不是摘要 | `Pass artifacts through files, not summaries alone.`（`SKILL.md:24`） |
| 证据状态不可混同 | `Keep confirmed, inferred, and to_verify distinct. An inferred design is not approval.`（`SKILL.md:25`） |
| 复核者不是作者 | `Run the acceptance Skill independently after implementation. It must not silently fix the product or treat a passing API response as usability proof.`（`SKILL.md:27`） |

这套设计的来源是本地工作流失败和安装行为验证，而不是与其他多 Agent 框架的对比——`reports/prior-art-research.md` 明确这么写，也明确放弃了这类比较。

## 通用 Agent 与专业岗位团队

| 关注点 | 一个通用 Agent | 这个 Skill 规定的做法 |
| --- | --- | --- |
| 岗位身份 | 角色只在同一个 prompt 里松散描述 | `Invoke specialist Skills by their exact names, never by vague role labels`（`SKILL.md:17`） |
| 上下文 | 所有岗位说明一次性加载 | 只加载当前岗位的说明（`SKILL.md:22`） |
| 步骤之间的传递 | 靠对话里的摘要 | 靠文件传递产物（`SKILL.md:24`） |
| 置信度 | confirmed 与 inferred 混在一起 | `confirmed` / `inferred` / `to_verify` 保持区分，inferred 的设计不等于批准（`SKILL.md:25`） |
| 变更权限 | Agent 直接往下做 | 默认只读基线；改代码、部署、改数据库、发布 GitHub、访问密钥前必须人工批准（`SKILL.md:15`、`SKILL.md:26`） |
| 验收 | 作者自己签字 | 验收岗位独立执行，且不得在验收过程中顺手修产品（`SKILL.md:27`） |

左列描述的是这些规则针对的失败模式，不是对某个具体 Agent 的评价。

## 岗位构成

四个岗位 Skill，各自是独立公开仓库，当前都发布在 `v0.2.0`。下面是 `SKILL.md:18-21` 里的**准确调用名**，与 [`manifest.json`](manifest.json) 的 `coordinated_skills` 一致：

| 调用名 | 独立包 | 该包在自己 Skill 描述里声明的范围 |
| --- | --- | --- |
| `$kang-product-architect` | [kang-product-architect](https://github.com/KanG-ciyuan/kang-product-architect) | 入口、角色、权限、核心任务、信息架构、状态归属、交接、可观测的完成标准。明确不负责视觉样式、实现，以及产品结构已批准后的孤立 UX 缺陷。 |
| `$kang-enterprise-process-reviewer` | [kang-enterprise-process-reviewer](https://github.com/KanG-ciyuan/kang-enterprise-process-reviewer) | 角色、触发条件、输入、规则、证据、交接、异常、授权、升级、人工决策门。明确不负责导航设计、视觉 UX 批评、实现，也不做一线员工访谈。 |
| `$kang-b2b-ux-auditor` | [kang-b2b-ux-auditor](https://github.com/KanG-ciyuan/kang-b2b-ux-auditor) | 首屏、角色导航、任务路径、表格、筛选、抽屉、批量操作、响应式行为，以及 loading / empty / error / waiting / stale / conflict / permission 各类状态。明确不只看视觉品味，也不负责后端实现和业务流程归属。 |
| `$kang-product-acceptance-auditor` | [kang-product-acceptance-auditor](https://github.com/KanG-ciyuan/kang-product-acceptance-auditor) | 对已发布或候选发布产品做独立的场景化验收：真实用户路径、权限、交接、恢复、证据、发布阻塞。明确不写代码、不做重新设计、不做纯单测或纯 API 测试，也不允许一边验收一边悄悄修缺陷。 |

有两件事不包含在"四"这个数字里，而且都很重要：

- **总控本身是第五个入口。** 这套包按五个各自可发现的 `SKILL.md` 设计——总控一个、岗位四个。把岗位包嵌进总控目录会造成重复发现和调用歧义；打包测试 `test_root_has_one_discoverable_skill` 就是用来保证本仓库根目录只有一个 `SKILL.md`。
- **顺序里有两个角色不是 Skill。** `human product decision` 和未命名的 `implementation team` 出现在默认顺序中（`SKILL.md:31-38`）。所以它是"四个岗位 Skill + 一次人工决策 + 一个实施团队"，不是"六个 Agent"。

还有一点值得知道：`SKILL.md` 只写岗位名称和顺序，**并没有**重述每个岗位负责什么。岗位职责写在各自的包里（以及上表），不在总控里。

## 协作机制

`SKILL.md` 规定了一条默认的产品复核顺序（`SKILL.md:31-38`）：

```text
$kang-product-architect
  -> $kang-enterprise-process-reviewer
  -> $kang-b2b-ux-auditor
  -> human product decision
  -> implementation team
  -> $kang-product-acceptance-auditor
```

约束这条顺序的规则有三条：

- `Skip a role only when the run manifest records why it is irrelevant.`（`SKILL.md:40`）
- `Add a role only when its output and permission boundary are defined first.`（`SKILL.md:40`）
- 只加载当前岗位的说明；岗位之间的产物以文件形式传递，而不是摘要（`SKILL.md:22`、`SKILL.md:24`）。

**每次运行的记账是"被要求了"，但没有形状。** `SKILL.md:16` 要求创建 run manifest，包含 `run_id`、objective、scope、permissions、input paths、output paths 和 approval status。但本仓库里没有 run manifest 的 schema、模板或示例，也没有任何代码读写它。因此 run manifest 只能算 `TO_VERIFY`。

`SKILL.md:42-44` 定义了输出：一份简短的状态摘要，指向交接文件，并报告证据、不确定性和尚待人工决策的部分。

### 示例

一个真实的调用示例——这是说明性示例，不是测试结果：

```text
$kang-agent-workforce  审查这个内部审批产品。
                       只读。走默认顺序。
                       任何代码改动之前先停下来。
```

总控随后会逐个点名它需要的岗位，每个岗位在下一个岗位开始前写出自己的交接记录。

## 交接合同

[`contracts/handoff.schema.yaml`](contracts/handoff.schema.yaml)（18 行）是本仓库唯一的机器可读合同。它要求八个字段：

| 字段 | 含义 |
| --- | --- |
| `run_id` | 标识本次运行 |
| `skill_name` | 这份交接由哪个岗位产出 |
| `skill_version` | 该岗位包的版本 |
| `objective` | 这一步要达成什么 |
| `input_paths` | 读取了哪些文件 |
| `output_path` | 产出了哪个文件 |
| `evidence_status` | 三个证据取值之一 |
| `next_action` | 下一步应该做什么 |

- **证据状态**只有三个取值：`confirmed`、`inferred`、`to_verify`（`contracts/handoff.schema.yaml:11-14`）。
- **权限**默认为 `read_only`；`implementation` 和 `deployment` 为 `requires_human_approval`（`contracts/handoff.schema.yaml:15-18`）。

比字段清单更重要的三条说明：

1. **`SKILL.md` 和 schema 描述的不是同一组字段。** `SKILL.md:24` 只列了六个——`skill_name`、`skill_version`、`input_paths`、`output_path`、`evidence_status`、`next_action`——漏掉了 `run_id` 和 `objective`。
2. **没有任何东西消费这份合同。** 仓库里没有模板、没有示例实例，也没有任何代码读写交接记录。
3. **这份合同与 `kang-agent-collab` 的合同不能互换**（见下）。

### 与 kang-agent-collab 的边界

> Workforce defines the team. Collab protects the handoff.

这句话是生态层面的**意图分工**——是随本批文档引入的新表述，不是两个项目任何已交付文件里的原文。它的具体含义是：

- **本仓库负责团队构成与调用顺序。** 它点名四个岗位、固定顺序、定义"跳过/新增岗位"的规则。
- **[kang-agent-collab](https://github.com/KanG-ciyuan/kang-agent-collab) 负责跨会话的状态传递、接管与漂移判定。** 它的交接/接管合同字段更多、也完全不同——任务与仓库身份、`result_state`、HEAD、分支与工作区状态、`do_not_do`——外加带 `D0`–`D3` 漂移等级的 Takeover Check。Collab 自己的 `SKILL.md` 明确声明不做编排，并把团队构成的路由指回这里。

两者**尚未集成，目前也不互通**：

- 两份合同只有一个字段名相同：`next_action`。本仓库的键（`run_id`、`skill_name`、`evidence_status` 等）与 Collab 的键（`task_ref`、`result_state`、`completed_and_evidence` 等）其余完全不重叠；`evidence_status`（`confirmed` / `inferred` / `to_verify`）和 Collab 的 `result_state` 是两套无关的词表。
- 本仓库**自带**一份交接记录，并没有把机制让给 Collab；而且它**完全没有提到过** `kang-agent-collab`——`SKILL.md`、`manifest.json`、`contracts/` 里都没有。
- 两者之间没有共享的 runner、校验器或适配层。

所以现状是：编排只有一份团队名册，交接却有两份不同的记录。把它们对齐是一件待办事项，不是已交付的能力。

## 复核关卡

frontmatter 描述里写的是复数 `review gates`（`SKILL.md:3`）。规则里实际规定的只有**一个**关卡：

| 关卡 | 实际规定的内容 | 位置 |
| --- | --- | --- |
| 独立验收 | `Run the acceptance Skill independently after implementation. It must not silently fix the product or treat a passing API response as usability proof.` | `SKILL.md:27` |

**没有**规定的东西：没有关卡判据、没有 pass/fail 定义、没有证据阈值、没有严重度分级、也没有返工路径。

失败处理是真实缺口，不是隐藏功能。这里没有 **failure return**（把工作退回给更早岗位的机制）：`SKILL.md` 和 `contracts/` 里没有任何 failure、reject 或 escalation 规则，`evidence_status` 没有 `failed` 取值，`next_action` 是没有任何失败语义的自由文本。请把描述里的复数理解为意图，而不是已实现的多关卡体系。

## 人工决策边界

这是整份规范里最具体、最强的部分：

- **默认只读。** `Start with a read-only baseline unless the user explicitly authorizes implementation.`（`SKILL.md:15`）
- **高风险动作前必须停下来问。** `Stop and request human approval before code changes, deployment, database changes, GitHub publication, or secret access.`（`SKILL.md:26`）
- **人工决策是流程中的一步。** `-> human product decision` 位于三个复核岗位与实施之间（`SKILL.md:35`）。
- **合同带同样的边界。** `default: read_only`，`implementation` 和 `deployment` 为 `requires_human_approval`（`contracts/handoff.schema.yaml:15-18`）；[`manifest.json`](manifest.json) 对 `implementation`、`deployment` 以及额外的 `publication` 做了同样声明。
- **不做等价声明。** `Never claim that a digital employee is equivalent to a senior human specialist; report evidence, uncertainty, and the remaining human decisions.`（`SKILL.md:44`）

这个边界是**规范里的声明，不是机器强制的**。没有任何代码读取 `contracts/handoff.schema.yaml`；它在整个仓库里唯一的引用是测试中的一处字面子串断言（`tests/test_workforce_contract.py:23`）。

仓库里完全没有覆盖的部分：没有数据范围或隐私规则，除 `secret access` 这两个词之外没有凭据处理规则，没有升级路径，也没有审计日志。这些是缺口，不是特性。

## 适用与不适用

| 适用 | 不适用 |
| --- | --- |
| 任务需要显式的岗位委派、交接合同、复核关卡或多 Agent 交付（`SKILL.md:3`） | 当作产品运行时工作流——这是协同规范，不是被执行的流水线（`SKILL.md:3`） |
| 你想要的是一支有名有姓的团队，而不是一个 Agent 扮演多个角色 | 替代人工产品决策（`SKILL.md:3`、`SKILL.md:26`） |
| 你想先做只读复核，实施前留下书面批准 | 四个岗位包尚未安装的场景——总控里没有它们（`SKILL.md:23`） |
| 跨项目的产品研发，且每一步复核都必须可独立归因 | 把数字员工当成资深人类专家的等价物（`SKILL.md:44`） |

## 当前验证状态

下面每一条要么是实际跑过的，要么是仓库自己承认缺失的。没有一条是从意图推断出来的。

| 声明 | 状态 | 依据 |
| --- | --- | --- |
| 协同四个岗位 Skill，且使用准确名称 | `VERIFIED` | `SKILL.md:18-21`；`manifest.json` 的 `coordinated_skills`；`v0.1.0`–`v0.1.5` 每个 tag 上都是同样四个名字 |
| 默认顺序（四个 Skill + 一次人工决策 + 一个实施团队） | `VERIFIED` | `SKILL.md:31-38` |
| 交接合同含 8 个必填字段和 3 值证据枚举 | `VERIFIED`（作为合同定义） | `contracts/handoff.schema.yaml:2-14`；但没有模板、示例或消费方 |
| 默认只读；实施与部署需要人工批准 | `VERIFIED`（作为声明） | `contracts/handoff.schema.yaml:15-18`；`manifest.json`；`SKILL.md:26` |
| 独立验收关卡 | `VERIFIED`（作为规则，**但没有判据**） | `SKILL.md:27` |
| 打包合同测试通过 | `VERIFIED` | 3 个测试，`Ran 3 tests ... OK`（见下） |
| 编排行为真的能跑通、岗位接线正确 | `TO_VERIFY` ——**没有任何测试覆盖** | 见"测试：仅打包合同" |
| run manifest 有确定的形状 | `TO_VERIFY` ——`SKILL.md:16` 要求了，但形状未定义、无模板 | 见"协作机制" |
| `evals/trigger_cases.json` 9/9 | `VERIFIED`，但性质是**已记录的 fixture**（关键词匹配、可确定性复现） | `reports/trigger-eval.json` |
| `evals/trigger_cases.yaml` 的路由用例 | `TO_VERIFY` ——定义了 3 个用例，**从未执行** | 仓库里既没有 runner 也没有记录结果 |
| `reports/skill-ir.json` 声明 `"maturity_tier": "production"` | `UNVERIFIED_CLAIM` | 同一文件里 `inputs`、`outputs`、`exclusions` 为空，四个 `workflow` 数组为空，`gates` / `permissions` 对象也为空 |
| `manifest.json` 里那 8 条 `release_gates` 真的执行过 | `TO_VERIFY` | 没有 CI、没有 gate 报告、仓库里没有任何产物可证明 |

### 测试：仅打包合同

```bash
python3 -m unittest discover -s tests -v
```

结果：`Ran 3 tests` / `OK`。测试套件只用标准库 `unittest`——当前环境没有安装 `pytest`，仓库也没有声明任何测试依赖。

[`tests/test_workforce_contract.py`](tests/test_workforce_contract.py) 里三个测试实际断言的是：

1. `test_identity_matches_manifest`——`manifest.json` 的 `name` 是 `kang-agent-workforce`，`SKILL.md` 含 `name: kang-agent-workforce`，且含从 manifest 插值出的版本字符串。这是一条版本漂移哨兵。
2. `test_root_has_one_discoverable_skill`——整棵树里只有一个 `SKILL.md`。这是打包断言。
3. `test_permission_and_handoff_gates_are_explicit`——四个字面子串存在：`SKILL.md` 中的 `read-only baseline`、`human approval`；合同中的 `default: read_only`、`requires_human_approval`。

它们**没有**断言的是：没有任何测试提到四个岗位名、`coordinated_skills`、调用顺序、交接字段集或 `evidence_status` 枚举。把四个岗位名从 `SKILL.md` 里删掉，三个测试依然全部通过。所以这是**零编排行为覆盖的打包合同测试**；本仓库也**没有 CI**（没有 `.github/`），所有验证都是手工、本地的。

### 已记录的 fixture，不是模型评分的评估

`reports/trigger-eval.json` 记录了 [`evals/trigger_cases.json`](evals/trigger_cases.json) 九个用例的 `"ok": true, 9/9`（阈值 `0.3`，概念关键词匹配）。这个数字是真实的、可确定性复现的，但它是**子串/关键词分类器的结果**——衡量的是 fixture 自洽性，不是模型路由是否正确；而且本仓库不带 runner。

[`evals/trigger_cases.yaml`](evals/trigger_cases.yaml) 是另一套语料、另一个用途：针对四个岗位的三个 Skill **路由**用例，带 `expected_skill` 和 `rejected_skills`。它**没有任何记录结果，仓库里也没有 runner**。两个文件之间没有任何一个被声明为权威。

### 作者自己写下的缺失证据

`reports/creation-handoff.md:13` ——`缺失证据：尚未完成跨多个真实项目的长期运行评估。`

`reports/prior-art-research.md:16` ——`尚未进行公共 Skill 目录的外部候选调研；当前版本的价值来自本地工作流失败和安装行为验证，不主张优于其他多 Agent 框架。`

### 版本与状态，说清楚

版本 `0.1.5` 在 `SKILL.md`、`manifest.json`、`reports/skill-ir.json`、`reports/creation-handoff.md`、tag `v0.1.5`（等于 HEAD）以及 GitHub release `v0.1.5` 上完全一致，没有版本错配。

但 `v0.1.5` 是一个**pre-1.0 指针**，不是 1.x 级别的稳定版：它是 semver `0.1.5`，`manifest.json` 写着 `"lifecycle_stage": "initial-release"`，仓库共 7 个 commit、0 star，作者自己的交接说明也记录了长期运行评估尚未完成——尽管 GitHub 把该 release 标为 `prerelease=false`。

本仓库**自己声明的状态**是 `"public-release-candidate"`（`manifest.json`），本 README 也就按这个口径描述它：一个已发布且带正式 tag 的候选发布版本。已知的内部不一致，如实列出而不是掩盖：

- `manifest.json` 的 `updated_at` 和 `reports/skill-ir.json` 的 `generated_at` 都是 `2026-08-22`，而 `v0.1.5` 发布于 `2026-09-08`——元数据比它所在的 release 落后 17 天。
- `contracts/handoff.schema.yaml` 自己声明 `version: "0.1.0"`，比包版本低四个小版本，且与包版本的关系没有任何说明。
- 权限 token 在文件之间并不一致：合同用 `read_only`，manifest 用 `read-only`。

## 快速开始

本仓库没有经过验证的一行安装命令。它是一个 Skill 包：根目录一个 `SKILL.md`，四个岗位在四个独立仓库里。

**1. 先读。** [`SKILL.md`](SKILL.md) 只有 44 行，就是全部总控内容。

**2. 安装。** 仓库自己的文档指向 Agent Skills 安装器：

```bash
npx skills add KanG-ciyuan/kang-agent-workforce
npx skills add KanG-ciyuan/kang-product-architect
npx skills add KanG-ciyuan/kang-enterprise-process-reviewer
npx skills add KanG-ciyuan/kang-b2b-ux-auditor
npx skills add KanG-ciyuan/kang-product-acceptance-auditor
```

这条路径在本次审计中**未经验证**——它依赖一个第三方 npm CLI，本次既没有安装也没有执行。请把它当作"仓库文档给出的路径"，而不是"已测试过的路径"。它要满足的设计要求是真的：总控和四个岗位必须作为**五个各自可发现的包**安装。绝不要把岗位包嵌进总控目录，那会造成重复发现和调用歧义。

**3. 验证这个包。** 在克隆下来的仓库目录里执行：

```bash
python3 -m unittest discover -s tests -v
```

这会跑上面说的 3 个打包合同测试。可选地，兄弟项目 [`kang-meta-skill`](https://github.com/KanG-ciyuan/kang-meta-skill) 提供了包校验脚本 `scripts/validate_skill.py`。它**依赖 PyYAML**：有 PyYAML 时对本仓库返回 `{"ok": true}`；没有 PyYAML 时，同一条命令会静默报出 4 条形如 `agents/interface.yaml missing interface.display_name` 的**假失败**。那条静默路径是该校验器的缺陷，不是本仓库的缺陷。

**4. 调用。** `$kang-agent-workforce` 会自己点名岗位。符合这套设计的说法：

- "使用 `$kang-agent-workforce` 审查当前项目，先只读，不修改代码。"
- "使用 `$kang-product-architect` 检查这个 SaaS 的入口、角色权限和完成标准。"
- "使用 `$kang-enterprise-process-reviewer` 检查员工提交到负责人决策之间的交接依据。"
- "使用 `$kang-b2b-ux-auditor` 判断一线员工进入后是否知道第一步做什么。"
- "使用 `$kang-product-acceptance-auditor` 从干净入口做独立验收，不要在验收中修代码。"

**前置条件：** 一个支持 `$skill-name` 调用和按需加载单个 Skill 的运行时，并已安装四个岗位包。仓库里没有密钥、没有 `.env` 文件，也不需要任何外部服务凭据。

<details>
<summary>仓库结构</summary>

| 路径 | 是什么 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | 全部总控内容：frontmatter、8 条强制规则、默认顺序、输出约定（44 行） |
| [`manifest.json`](manifest.json) | 包身份、权限、`coordinated_skills`、8 条声明的 `release_gates` |
| [`contracts/handoff.schema.yaml`](contracts/handoff.schema.yaml) | 唯一的机器可读合同（18 行） |
| [`agents/interface.yaml`](agents/interface.yaml) | 展示元数据与适配目标；[`agents/openai.yaml`](agents/openai.yaml) 重复了其中三个字段，且没有任何文件引用它 |
| [`evals/trigger_cases.json`](evals/trigger_cases.json) | 触发分类语料（阈值 `0.3`，9 个用例） |
| [`evals/trigger_cases.yaml`](evals/trigger_cases.yaml) | 3 个 Skill 路由用例——已定义，从未执行 |
| [`reports/`](reports/) | 作者自述报告与一份已记录的触发 fixture 结果。不是发布门证据 |
| [`tests/test_workforce_contract.py`](tests/test_workforce_contract.py) | 3 个打包合同测试 |
| [`LICENSE`](LICENSE) | MIT |

</details>

## 生态位置

阶段 **BUILD & COORDINATE** · 定位：**Role-Based AI Product Workforce**。

```text
发现 DISCOVER
企业 AI 诊断 Skills
        ↓
定义 DEFINE
Kang Product Architect
Kang Enterprise Process Reviewer
        ↓
构建与协同 BUILD & COORDINATE
Kang Agent Workforce
Kang Agent Collab
Kang Frontend Standard
        ↓
验证 VERIFY
Kang B2B UX Auditor
Kang Product Acceptance Auditor
        ↓
交付 DELIVER
Kang GitHub README
Kang PPT Skill
```

> 这是一张生态地图，不是严格的运行时流水线。各阶段描述的是项目所处的工作位置，
> 而不是强制的执行顺序。

---

## 属于 Kang 开源 AI 体系

本项目是「面向企业 AI 转型、Agent 协作与 AI 原生产品交付的证据驱动体系」的一部分。

| 阶段 | 项目 | 作用 |
| --- | --- | --- |
| DISCOVER 发现 | [enterprise-ai-diagnostic-skills](https://github.com/KanG-ciyuan/enterprise-ai-diagnostic-skills) | 在自动化之前，先弄清企业真实业务如何运行 |
| DEFINE 定义 | [kang-product-architect](https://github.com/KanG-ciyuan/kang-product-architect) | 把模糊需求转化为可实施、可审查的产品契约 |
| DEFINE 定义 | [kang-enterprise-process-reviewer](https://github.com/KanG-ciyuan/kang-enterprise-process-reviewer) | 审查流程是否可执行、可追责、可恢复 |
| BUILD & COORDINATE 构建与协同 | [kang-agent-workforce](https://github.com/KanG-ciyuan/kang-agent-workforce) | 角色化的 Agent 数字员工团队与显式交接 |
| BUILD & COORDINATE 构建与协同 | [kang-agent-collab](https://github.com/KanG-ciyuan/kang-agent-collab) | Agent 协作与交接协议 |
| BUILD & COORDINATE 构建与协同 | [kang-frontend-standard](https://github.com/KanG-ciyuan/kang-frontend-standard) | AI 构建界面的前端质量标准 |
| VERIFY 验证 | [kang-b2b-ux-auditor](https://github.com/KanG-ciyuan/kang-b2b-ux-auditor) | 用户能否真正把工作做完 |
| VERIFY 验证 | [kang-product-acceptance-auditor](https://github.com/KanG-ciyuan/kang-product-acceptance-auditor) | AI 构建产品的独立验收 |
| DELIVER 交付 | [kang-github-readme](https://github.com/KanG-ciyuan/kang-github-readme) | 证据感知的 README 工程 |
| DELIVER 交付 | [kang-ppt-skill](https://github.com/KanG-ciyuan/kang-ppt-skill) | 证据感知的演示文稿设计 |

**横向基础设施：** [kang-meta-skill](https://github.com/KanG-ciyuan/kang-meta-skill) —
Skill 工程化、评估与发布治理。

**早期工作：** [ai-agent-rules](https://github.com/KanG-ciyuan/ai-agent-rules)、
[workflow-five-steps](https://github.com/KanG-ciyuan/workflow-five-steps)、
[renovation-agent](https://github.com/KanG-ciyuan/renovation-agent)。

<!-- kang-author:start -->
## 作者

由 [Kang](https://github.com/KanG-ciyuan) 创建并维护。
<!-- kang-author:end -->

## 开源许可证

本项目采用 [MIT License](LICENSE) 开源。
