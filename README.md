# Kang Agent Workforce

English | [简体中文](README.zh-CN.md)

[![Release](https://img.shields.io/github/v/release/KanG-ciyuan/kang-agent-workforce?display_name=tag&sort=semver&style=flat-square)](https://github.com/KanG-ciyuan/kang-agent-workforce/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/KanG-ciyuan/kang-agent-workforce?style=flat-square)](https://github.com/KanG-ciyuan/kang-agent-workforce/commits/main)

**A role-based AI product team with explicit responsibilities, handoff contracts, independent review gates, and human decision boundaries.**

One orchestrator Skill names four specialist product-development Skills, fixes the order in which they are called, and requires a file-based handoff record between steps. Do not let one agent define the requirements, check the process, review the experience, and then accept its own work.

`kang-agent-workforce` is a **coordination specification, not a runtime**. `SKILL.md` (44 lines) is the entire behavioural content of the repository, and the repository contains no orchestration code. It is written for people running a Skill-aware agent runtime who want role separation on real product work instead of one general-purpose agent doing all of it. This public repository contains reusable orchestration logic only; the enterprise AI process diagnosis product and its private runtime Skills are separate and are not included.

## Why Not One General-Purpose Agent?

The orchestrator's own instruction states the premise (`SKILL.md:11`):

> You are the coordinator for a small, explicit product-development team. You do not pretend to be all specialists at once. You select the smallest set of named Kang Skills, pass only the required project artifacts, and preserve a reviewable handoff.

An agent that writes the requirements, checks the process, reviews the experience and then accepts its own work cannot be contradicted: everything it produces agrees with everything else it produced. Four rules in `SKILL.md` are written specifically against that self-agreement.

| Rule | Wording |
| --- | --- |
| One role at a time | `Load a specialist's full instructions only for that specialist's turn.` (`SKILL.md:22`) |
| Artifacts, not summaries | `Pass artifacts through files, not summaries alone.` (`SKILL.md:24`) |
| Evidence that cannot be merged | `Keep confirmed, inferred, and to_verify distinct. An inferred design is not approval.` (`SKILL.md:25`) |
| A reviewer who is not the author | `Run the acceptance Skill independently after implementation. It must not silently fix the product or treat a passing API response as usability proof.` (`SKILL.md:27`) |

The design's stated origin is local workflow failures and install behaviour, not a comparison against other multi-agent frameworks — `reports/prior-art-research.md` says so explicitly and explicitly declines the comparison.

## General-Purpose Agent vs Specialist Workforce

| Concern | One general-purpose agent | What this Skill prescribes |
| --- | --- | --- |
| Role identity | Roles described loosely inside one prompt | `Invoke specialist Skills by their exact names, never by vague role labels` (`SKILL.md:17`) |
| Context | Every role's instructions loaded at once | Only the current specialist's instructions are loaded (`SKILL.md:22`) |
| Transfer between steps | Summaries carried in the conversation | Artifacts passed through files (`SKILL.md:24`) |
| Confidence | Confirmed and inferred statements blur together | `confirmed` / `inferred` / `to_verify` stay distinct; an inferred design is not approval (`SKILL.md:25`) |
| Change authority | The agent proceeds | Read-only baseline by default; human approval before code changes, deployment, database changes, GitHub publication, or secret access (`SKILL.md:15`, `SKILL.md:26`) |
| Acceptance | The author signs off | The acceptance Skill runs independently and must not fix the product while accepting (`SKILL.md:27`) |

The left column describes the failure mode these rules are written against; it is not a claim about any particular agent.

## The Roles

Four specialist Skills, each a separate public repository, each currently published at `v0.2.0`. These are the exact invocation names from `SKILL.md:18-21`, corroborated by `coordinated_skills` in [`manifest.json`](manifest.json):

| Invocation name | Independent package | Scope, as that package declares it in its own Skill description |
| --- | --- | --- |
| `$kang-product-architect` | [kang-product-architect](https://github.com/KanG-ciyuan/kang-product-architect) | Entry points, actors, permissions, core jobs, information architecture, state ownership, handoffs, observable completion criteria. Explicitly not visual styling, implementation, or isolated UX defects. |
| `$kang-enterprise-process-reviewer` | [kang-enterprise-process-reviewer](https://github.com/KanG-ciyuan/kang-enterprise-process-reviewer) | Actors, triggers, inputs, rules, evidence, handoff, exceptions, authorization, escalation, human decision gates. Explicitly not navigation design, visual UX critique, implementation, or raw employee interviewing. |
| `$kang-b2b-ux-auditor` | [kang-b2b-ux-auditor](https://github.com/KanG-ciyuan/kang-b2b-ux-auditor) | First viewport, role navigation, task paths, tables, filters, drawers, bulk actions, responsive behaviour, and the loading / empty / error / waiting / stale / conflict / permission states. Explicitly not visual taste alone, backend implementation, or business-process ownership. |
| `$kang-product-acceptance-auditor` | [kang-product-acceptance-auditor](https://github.com/KanG-ciyuan/kang-product-acceptance-auditor) | Independent, scenario-based acceptance of a released or release-candidate product: real user paths, permissions, handoffs, recovery, evidence, release blockers. Explicitly not coding, redesign, unit-only or API-only testing, and not accepting while silently fixing defects. |

Two things the count of four does not include, and both matter:

- **The orchestrator itself is a fifth entrypoint.** The package is designed as five separately discoverable `SKILL.md` files — the orchestrator plus the four roles. Nesting a specialist package inside the orchestrator's directory causes duplicate Skill discovery and ambiguous invocation; the packaging test `test_root_has_one_discoverable_skill` enforces exactly one `SKILL.md` at this repository's root.
- **Two actors in the sequence are not Skills.** `human product decision` and the unnamed `implementation team` appear in the default sequence (`SKILL.md:31-38`). It is four specialist Skills plus one human decision plus an implementation team — not "six agents".

Worth knowing: `SKILL.md` names the roles and fixes their order, but it does **not** restate what each role is responsible for. Per-role scope lives in each specialist package (and in the table above), not in the orchestrator.

## How Coordination Works

`SKILL.md` prescribes one default product-review sequence (`SKILL.md:31-38`):

```text
$kang-product-architect
  -> $kang-enterprise-process-reviewer
  -> $kang-b2b-ux-auditor
  -> human product decision
  -> implementation team
  -> $kang-product-acceptance-auditor
```

Three rules govern the sequence:

- `Skip a role only when the run manifest records why it is irrelevant.` (`SKILL.md:40`)
- `Add a role only when its output and permission boundary are defined first.` (`SKILL.md:40`)
- Only the current specialist's instructions are loaded, and artifacts move between roles as files rather than as summaries (`SKILL.md:22`, `SKILL.md:24`).

**Per-run bookkeeping is specified but not shaped.** `SKILL.md:16` requires a run manifest with `run_id`, objective, scope, permissions, input paths, output paths and approval status. No run-manifest schema, template or example exists anywhere in this repository, and nothing reads or writes one. Treat the run manifest as `TO_VERIFY`.

`SKILL.md:42-44` defines the output: a concise status summary that points at the handoff files, plus the evidence, the uncertainty and the human decisions still outstanding.

### Example

A realistic invocation — illustrative, not a test result:

```text
$kang-agent-workforce  Review this internal approval product.
                       Read-only. Use the default sequence.
                       Stop before any code change.
```

The orchestrator then names the specialists it needs, one at a time, and each one writes a handoff record before the next begins.

## Handoff Contract

[`contracts/handoff.schema.yaml`](contracts/handoff.schema.yaml) (18 lines) is the only machine-readable contract in the repository. It requires eight fields:

| Field | Meaning |
| --- | --- |
| `run_id` | Identifies the run |
| `skill_name` | Which specialist produced this handoff |
| `skill_version` | Version of that specialist package |
| `objective` | What this step was for |
| `input_paths` | Files consumed |
| `output_path` | File produced |
| `evidence_status` | One of the three evidence values |
| `next_action` | What should happen next |

- **Evidence status** is limited to `confirmed`, `inferred`, `to_verify` (`contracts/handoff.schema.yaml:11-14`).
- **Permissions** default to `read_only`; `implementation` and `deployment` are `requires_human_approval` (`contracts/handoff.schema.yaml:15-18`).

Three caveats that matter more than the field list:

1. **`SKILL.md` and the schema do not describe the same field set.** `SKILL.md:24` lists six fields — `skill_name`, `skill_version`, `input_paths`, `output_path`, `evidence_status`, `next_action` — and omits `run_id` and `objective`.
2. **Nothing consumes the contract.** There is no template, no example instance, and no code that reads or writes a handoff record anywhere in the repository.
3. **The contract is not interchangeable with `kang-agent-collab`'s** (see below).

### Where this sits relative to kang-agent-collab

> Workforce defines the team. Collab protects the handoff.

That sentence is the ecosystem's **division of intent** — a new framing introduced with this batch of documentation, not a quotation from any shipped file in either project. What it means concretely:

- **This repository owns team composition and invocation order.** It names the four roles, fixes the order, and defines the skip/add rule.
- **[kang-agent-collab](https://github.com/KanG-ciyuan/kang-agent-collab) owns cross-session state transfer, takeover and drift classification.** Its handoff/takeover contract carries a different, larger field set — task and repository identity, `result_state`, HEAD, branch and working-tree state, `do_not_do` — plus a Takeover Check with drift levels `D0`–`D3`. Collab's own `SKILL.md` deliberately disclaims orchestration and routes team composition here.

They are **not integrated and currently not interoperable**:

- The two contracts share exactly one field name: `next_action`. This repository's keys (`run_id`, `skill_name`, `evidence_status`, …) and Collab's keys (`task_ref`, `result_state`, `completed_and_evidence`, …) are otherwise disjoint, and `evidence_status` (`confirmed` / `inferred` / `to_verify`) and Collab's `result_state` are unrelated vocabularies.
- This repository ships **its own** handoff record rather than delegating the mechanism, and it names `kang-agent-collab` **nowhere** — not in `SKILL.md`, `manifest.json`, or `contracts/`.
- No shared runner, validator or adapter connects the two.

So: one roster authority for orchestration, two different handoff records today. Aligning them is an open item, not a shipped feature.

## Review Gates

The frontmatter description advertises `review gates`, plural (`SKILL.md:3`). The rules specify **one** gate:

| Gate | What is actually specified | Where |
| --- | --- | --- |
| Independent acceptance | `Run the acceptance Skill independently after implementation. It must not silently fix the product or treat a passing API response as usability proof.` | `SKILL.md:27` |

What is **not** specified: no gate criteria, no pass/fail definition, no evidence threshold, no severity scale, and no rework path.

Failure handling is a real gap rather than a hidden feature. There is no **failure return** — no mechanism for sending work back to an earlier role: `SKILL.md` and `contracts/` contain no failure, rejection or escalation rule, `evidence_status` has no `failed` value, and `next_action` is a free-text field with no failure semantics. Read the plural in the description as intent, not as an implemented multi-gate system.

## Human Decision Boundary

The strongest and most concrete part of the specification:

- **Read-only default.** `Start with a read-only baseline unless the user explicitly authorizes implementation.` (`SKILL.md:15`)
- **A stop-and-ask gate before risky action.** `Stop and request human approval before code changes, deployment, database changes, GitHub publication, or secret access.` (`SKILL.md:26`)
- **The human decision is a step in the pipeline.** `-> human product decision` sits between the three review roles and implementation (`SKILL.md:35`).
- **The contract carries the same boundary.** `default: read_only`, with `implementation` and `deployment` set to `requires_human_approval` (`contracts/handoff.schema.yaml:15-18`); [`manifest.json`](manifest.json) declares the same for `implementation`, `deployment` and additionally `publication`.
- **No equivalence claim.** `Never claim that a digital employee is equivalent to a senior human specialist; report evidence, uncertainty, and the remaining human decisions.` (`SKILL.md:44`)

The boundary is a **declaration in the specification, not machine-enforced**. No code reads `contracts/handoff.schema.yaml`; its only reference anywhere is a literal-substring assertion inside a test (`tests/test_workforce_contract.py:23`).

Not covered anywhere in the repository: no data-scope or privacy rule, no credential-handling rule beyond the two words `secret access`, no escalation path, and no audit log. These are gaps, not features.

## Use / Not Use

| Use it when | Do not use it for |
| --- | --- |
| A task needs explicit role delegation, handoff contracts, review gates or multi-agent delivery (`SKILL.md:3`) | A product runtime workflow — this is a coordination specification, not an executed pipeline (`SKILL.md:3`) |
| You want a named team rather than one agent impersonating several roles | A substitute for human product decisions (`SKILL.md:3`, `SKILL.md:26`) |
| You want read-only review first and a recorded approval before implementation | Anything where the four specialist packages are not installed — the orchestrator does not contain them (`SKILL.md:23`) |
| The work is product development across projects, with reviews that must stay independently attributable | Treating a digital employee as equivalent to a senior human specialist (`SKILL.md:44`) |

## Current Validation Status

Everything below is either something that was run or something the repository itself says is missing. Nothing here is inferred from intention.

| Claim | Status | Evidence |
| --- | --- | --- |
| Four specialist Skills are coordinated, by exact name | `VERIFIED` | `SKILL.md:18-21`; `coordinated_skills` in `manifest.json`; the same four names at every tag `v0.1.0`–`v0.1.5` |
| The default sequence (four Skills, one human decision, one implementation team) | `VERIFIED` | `SKILL.md:31-38` |
| A handoff contract with 8 required fields and a 3-value evidence enum | `VERIFIED` as a contract definition | `contracts/handoff.schema.yaml:2-14`; no template, example or consumer exists |
| Read-only default; human approval for implementation and deployment | `VERIFIED` as a declaration | `contracts/handoff.schema.yaml:15-18`; `manifest.json`; `SKILL.md:26` |
| Independent acceptance gate | `VERIFIED` as a rule, **with no criteria** | `SKILL.md:27` |
| Package contract tests pass | `VERIFIED` | 3 tests, `Ran 3 tests ... OK` (below) |
| Orchestration behaviour works, roles are correctly wired | `TO_VERIFY` — **nothing tests this** | see "Tests: package contract only" |
| Run manifest with a defined shape | `TO_VERIFY` — required by `SKILL.md:16`, shape undefined, no template | § How Coordination Works |
| `evals/trigger_cases.json` scoring 9/9 | `VERIFIED` as **recorded fixtures** (keyword-based, deterministic) | `reports/trigger-eval.json` |
| `evals/trigger_cases.yaml` routing cases | `TO_VERIFY` — three cases defined, **never executed** | no runner and no recorded result anywhere |
| `reports/skill-ir.json` declaring `"maturity_tier": "production"` | `UNVERIFIED_CLAIM` | the same file has empty `inputs`, `outputs`, `exclusions`, all four `workflow` arrays, and empty `gates` / `permissions` objects |
| The 8 `release_gates` in `manifest.json` actually ran | `TO_VERIFY` | no CI, no gate report, no artifact in the repository |

### Tests: package contract only

```bash
python3 -m unittest discover -s tests -v
```

Result: `Ran 3 tests` / `OK`. The suite is stdlib `unittest` only — `pytest` is not installed in this environment, and no test dependency is declared.

What the three tests in [`tests/test_workforce_contract.py`](tests/test_workforce_contract.py) assert:

1. `test_identity_matches_manifest` — `manifest.json`'s `name` is `kang-agent-workforce`, `SKILL.md` contains `name: kang-agent-workforce`, and `SKILL.md` contains the version string interpolated from the manifest. A version-drift canary.
2. `test_root_has_one_discoverable_skill` — exactly one `SKILL.md` exists in the tree. A packaging assertion.
3. `test_permission_and_handoff_gates_are_explicit` — four literal substrings are present: `read-only baseline` and `human approval` in `SKILL.md`; `default: read_only` and `requires_human_approval` in the contract.

What they do **not** assert: no test names any of the four roles, `coordinated_skills`, the invocation sequence, the handoff field set, or the `evidence_status` enum. All four role names could be deleted from `SKILL.md` and all three tests would still pass. These are **package contract tests with zero orchestration-behaviour coverage**, and there is **no CI** in this repository (`.github/` does not exist) — every validation here is manual and local.

### Recorded fixtures, not model-scored evaluation

`reports/trigger-eval.json` records `"ok": true, 9/9` for the nine cases in [`evals/trigger_cases.json`](evals/trigger_cases.json) (threshold `0.3`, concept-keyword matching). The number is real and reproduces deterministically, but it is a **substring/keyword classifier result** — it measures fixture self-consistency, not whether a model routes correctly, and no runner ships in this repository.

[`evals/trigger_cases.yaml`](evals/trigger_cases.yaml) is a different corpus with a different purpose: three Skill-**routing** cases with `expected_skill` and `rejected_skills` for the four specialists. It has **no recorded result and no runner anywhere in the repository**. Neither file is declared authoritative over the other.

### The authors' own missing-evidence notes

`reports/creation-handoff.md:13` — `缺失证据：尚未完成跨多个真实项目的长期运行评估。` ("Missing evidence: a long-run evaluation across multiple real projects has not been completed.")

`reports/prior-art-research.md:16` — `尚未进行公共 Skill 目录的外部候选调研；当前版本的价值来自本地工作流失败和安装行为验证，不主张优于其他多 Agent 框架。` ("No external survey of public Skill catalogues was done; this version's value comes from local workflow failures and install-behaviour verification, and it makes no claim of superiority over other multi-agent frameworks.")

### Version and status, stated precisely

Version `0.1.5` is consistent across `SKILL.md`, `manifest.json`, `reports/skill-ir.json`, `reports/creation-handoff.md`, the tag `v0.1.5` (which equals HEAD), and the GitHub release `v0.1.5`. There is no version mismatch.

But `v0.1.5` is a **pre-1.0 pointer**, not a stable 1.x-class release: it is semver `0.1.5`, `manifest.json` says `"lifecycle_stage": "initial-release"`, the repository has 7 commits and 0 stars, and the author's own handoff note records that long-run evaluation has not happened — even though GitHub reports the release as `prerelease=false`.

The repository's **own declared status** is `"public-release-candidate"` (`manifest.json`), which is how this README describes it: a release candidate with a real, tagged, non-prerelease GitHub release. Known internal disagreements, reported rather than papered over:

- `manifest.json` `updated_at` and `reports/skill-ir.json` `generated_at` are `2026-08-22`, while the `v0.1.5` release is dated `2026-09-08` — stale metadata, 17 days behind the release it ships in.
- `contracts/handoff.schema.yaml` declares its own `version: "0.1.0"`, four minor versions behind the package, with no documented relationship to it.
- Permission tokens do not match between files: `read_only` (contract) versus `read-only` (manifest).

## Quick Start

There is no verified one-line install command for this repository. It is a Skill package: one `SKILL.md` at the repository root, with the four specialists living in four separate repositories.

**1. Read it first.** [`SKILL.md`](SKILL.md) is 44 lines and is the whole orchestrator.

**2. Install.** The repository's own documentation points at the Agent Skills installer:

```bash
npx skills add KanG-ciyuan/kang-agent-workforce
npx skills add KanG-ciyuan/kang-product-architect
npx skills add KanG-ciyuan/kang-enterprise-process-reviewer
npx skills add KanG-ciyuan/kang-b2b-ux-auditor
npx skills add KanG-ciyuan/kang-product-acceptance-auditor
```

This path was **not verified** in this audit — it requires a third-party npm CLI that was not installed or executed here. Treat it as the repository's documented route, not as a tested one. The design requirement it satisfies is real: install the orchestrator and the four roles as **five separate discoverable packages**. Never nest a specialist package inside the orchestrator's directory; that produces duplicate Skill discovery and ambiguous invocation.

**3. Verify the package.** From a clone of this repository:

```bash
python3 -m unittest discover -s tests -v
```

That runs the 3 package contract tests described above. Optionally, the sibling [`kang-meta-skill`](https://github.com/KanG-ciyuan/kang-meta-skill) project ships a package validator at `scripts/validate_skill.py`. It **requires PyYAML**: with PyYAML it returns `{"ok": true}` for this repository, and without it the same command silently reports four false `agents/interface.yaml missing interface.display_name`-style failures. That silent path is a defect of that validator, not of this repository.

**4. Invoke it.** `$kang-agent-workforce` names the specialists itself. Prompts that work with the design:

- "Use `$kang-agent-workforce` to review this project. Read-only first, no code changes."
- "Use `$kang-product-architect` to check this SaaS product's entry points, role permissions and completion criteria."
- "Use `$kang-enterprise-process-reviewer` to check the handoff evidence between an employee submission and a manager decision."
- "Use `$kang-b2b-ux-auditor` to judge whether a frontline employee knows what to do first."
- "Use `$kang-product-acceptance-auditor` for independent acceptance from a clean entry point. Do not fix code during acceptance."

**Requirements:** a Skill-aware agent runtime that supports `$skill-name` invocation and per-Skill loading, with the four specialist packages installed. The repository contains no secrets, no `.env` file, and requires no external service credentials.

<details>
<summary>Repository layout</summary>

| Path | What it is |
| --- | --- |
| [`SKILL.md`](SKILL.md) | The entire orchestrator: frontmatter, 8 mandatory rules, the default sequence, the output contract (44 lines) |
| [`manifest.json`](manifest.json) | Package identity, permissions, `coordinated_skills`, 8 declared `release_gates` |
| [`contracts/handoff.schema.yaml`](contracts/handoff.schema.yaml) | The only machine-readable contract (18 lines) |
| [`agents/interface.yaml`](agents/interface.yaml) | Display metadata and adapter targets; [`agents/openai.yaml`](agents/openai.yaml) duplicates three of those fields and is referenced by nothing |
| [`evals/trigger_cases.json`](evals/trigger_cases.json) | Trigger-classification corpus (threshold `0.3`, 9 cases) |
| [`evals/trigger_cases.yaml`](evals/trigger_cases.yaml) | 3 Skill-routing cases — defined, never executed |
| [`reports/`](reports/) | Authoring self-reports and one recorded trigger-fixture result. Not release-gate evidence |
| [`tests/test_workforce_contract.py`](tests/test_workforce_contract.py) | The 3 package contract tests |
| [`LICENSE`](LICENSE) | MIT |

</details>

## Ecosystem

Stage **BUILD & COORDINATE** · Positioning: **Role-Based AI Product Workforce**.

```text
DISCOVER
Enterprise AI Diagnostic Skills
        ↓
DEFINE
Kang Product Architect
Kang Enterprise Process Reviewer
        ↓
BUILD & COORDINATE
Kang Agent Workforce
Kang Agent Collab
Kang Frontend Standard
        ↓
VERIFY
Kang B2B UX Auditor
Kang Product Acceptance Auditor
        ↓
DELIVER
Kang GitHub README
Kang PPT Skill
```

> This is an ecosystem map, not a strict runtime pipeline. The stages describe where
> each project sits in the work, not a mandatory execution order.

---

## Part of the Kang Open-Source AI System

This project is one part of an evidence-driven system for enterprise AI transformation,
agent collaboration, and AI-native product delivery.

| Stage | Project | Role |
| --- | --- | --- |
| DISCOVER | [enterprise-ai-diagnostic-skills](https://github.com/KanG-ciyuan/enterprise-ai-diagnostic-skills) | Understand how the business actually works before automating it |
| DEFINE | [kang-product-architect](https://github.com/KanG-ciyuan/kang-product-architect) | Turn ambiguous requirements into an implementation-ready product contract |
| DEFINE | [kang-enterprise-process-reviewer](https://github.com/KanG-ciyuan/kang-enterprise-process-reviewer) | Review whether workflows are executable, accountable and recoverable |
| BUILD & COORDINATE | [kang-agent-workforce](https://github.com/KanG-ciyuan/kang-agent-workforce) | Role-based AI product workforce with explicit handoffs |
| BUILD & COORDINATE | [kang-agent-collab](https://github.com/KanG-ciyuan/kang-agent-collab) | Agent collaboration and handoff protocol |
| BUILD & COORDINATE | [kang-frontend-standard](https://github.com/KanG-ciyuan/kang-frontend-standard) | Frontend quality standard for AI-built interfaces |
| VERIFY | [kang-b2b-ux-auditor](https://github.com/KanG-ciyuan/kang-b2b-ux-auditor) | Can users actually finish the work? |
| VERIFY | [kang-product-acceptance-auditor](https://github.com/KanG-ciyuan/kang-product-acceptance-auditor) | Independent acceptance of AI-built products |
| DELIVER | [kang-github-readme](https://github.com/KanG-ciyuan/kang-github-readme) | Evidence-aware README engineering |
| DELIVER | [kang-ppt-skill](https://github.com/KanG-ciyuan/kang-ppt-skill) | Evidence-aware presentation design |

**Cross-cutting infrastructure:** [kang-meta-skill](https://github.com/KanG-ciyuan/kang-meta-skill) —
Skill engineering, evaluation and release governance.

**Earlier work:** [ai-agent-rules](https://github.com/KanG-ciyuan/ai-agent-rules),
[workflow-five-steps](https://github.com/KanG-ciyuan/workflow-five-steps),
[renovation-agent](https://github.com/KanG-ciyuan/renovation-agent).

<!-- kang-author:start -->
## Author

Created and maintained by [Kang](https://github.com/KanG-ciyuan).
<!-- kang-author:end -->

## License

Released under the [MIT License](LICENSE).
