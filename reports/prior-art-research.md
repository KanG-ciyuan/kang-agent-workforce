# Prior Art Research

## Scope

本次设计优先复用当前 Codex 的子代理机制、独立 Skill 发现机制和 Kang Meta Skill 的发布门，不引入外部编排框架。

## Keep / Adapt / Reject / Invent

- Keep：Codex 按需加载独立 Skill，避免把全部岗位说明放入总控上下文。
- Adapt：用文件交接合同代替子代理之间不可验证的口头传递。
- Reject：把多个可发现的 `SKILL.md` 嵌套在一个总控安装目录；这会造成重复发现和调用歧义。
- Invent：Kang 的人工批准门、证据状态和显式岗位调用顺序。

## Missing Evidence

尚未进行公共 Skill 目录的外部候选调研；当前版本的价值来自本地工作流失败和安装行为验证，不主张优于其他多 Agent 框架。
