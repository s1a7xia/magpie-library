# Matt Pocock Skills 简体中文裁剪版

这是 [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) 的本地 Codex 插件，按用户勾选保留 16 个工程技能，并针对 Codex 的执行语义、授权边界和可靠交付做了适配。

- 上游中文内容 commit：`d97aa0788b120c9363ebddfd47b87618d9314c3e`
- 插件版本：`1.0.10`
- 许可证：MIT；见 [LICENSE](LICENSE) 和 [LICENSE.zh-CN.md](LICENSE.zh-CN.md)
- 插件名：`mattpocock-skills-zh`
- Marketplace：`magpie-mattpocock-zh`

## 包含的技能

```text
需求与决策
  ask-matt
  triage
  wayfinder
  grill-with-docs
  grilling
  domain-modeling

证据与规格
  research
  prototype
  to-spec
  to-tickets
  setup-matt-pocock-skills

实现、审查与交付
  implement-spec
  code-review
  retro
  handoff
  writing-for-agents
```

## 推荐路径

```text
Codex 自带技能匹配 + 可选 ask-matt 导航
  -> 小而明确：直接实现
  -> 会话内可收敛：grill-with-docs
  -> 大型、跨会话、未知互相阻塞：$mattpocock-skills-zh:wayfinder
       -> research：外部事实未明
       -> prototype：设计需要看效果
       -> grilling + domain-modeling：业务决策和领域术语
  -> $mattpocock-skills-zh:to-spec
  -> $mattpocock-skills-zh:to-tickets（仅多个纵向切片或真实依赖）
  -> 默认由 Codex 直接实现；显式 $mattpocock-skills-zh:implement-spec 时走隔离 worktree 编排
  -> 按授权验收
  -> $mattpocock-skills-zh:code-review / $mattpocock-skills-zh:retro 按需
```

`ask-matt` 是显式导航器，不替代 Codex 自带路由，也不强制每个任务走完整流程。路径清楚时无需调用它；路径不清时由 Codex 先说明理由，用户确认后再进入。

导航后需要进入下一阶段时，使用完整名，例如 `$mattpocock-skills-zh:wayfinder`、`$mattpocock-skills-zh:to-spec`。`wayfinder` 内部的 `research`、`prototype`、`grilling`、`domain-modeling` 通过相对路径读取，不要求这些技能被隐式选择。

## 调用策略

- **自动调用**：仅 `grill-with-docs`。它对应本项目“单会话内出现会改变结果的真实歧义”这一条优先触发；`ruoyi6`、`database-design` 由 Magpie 本地指令单独触发。
- **显式调用**：其余 15 个技能全部为 explicit-only：`ask-matt`、`triage`、`wayfinder`、`grilling`、`domain-modeling`、`research`、`prototype`、`to-spec`、`to-tickets`、`setup-matt-pocock-skills`、`implement-spec`、`code-review`、`retro`、`handoff`、`writing-for-agents`。它们不会进入模型的隐式技能列表；需要时在 Codex 中点名完整技能名。

在 Codex 中调用插件技能必须带命名空间：

```text
$mattpocock-skills-zh:wayfinder
$mattpocock-skills-zh:to-tickets
$mattpocock-skills-zh:code-review
```

单独写 `$wayfinder` 不会加载插件技能。`grill-with-docs` 虽然可自动匹配，也仍可用同一完整名显式调用。`grill-with-docs` 内部的 `grilling`、`domain-modeling` 通过相对路径读取，不依赖它们可被隐式选择。

## 本机适配

- `to-spec` 默认写 `.scratch/<feature-slug>/spec.md`，`to-tickets` 默认写 `.scratch/<feature-slug>/issues/`，`wayfinder` 默认写 `.scratch/<effort>/wayfinder.md` 与 `tickets/`；均不默认写远端 Issue。
- `triage`、`setup-matt-pocock-skills` 在未授权时只做只读分析或本地草案，不评论、打标签、assign、close、创建 label 或修改 remote。
- `research` 被当前任务调用后即启动后台调研子代理，主会话继续推进；如果后台子代理不可用，则在当前会话完成并说明。
- `implement-spec` 显式调用后即授权隔离 worktree 的探索、实现和合并子代理，以及这些任务分支上的本地提交；push、PR、Issue 写入、测试和发布仍需当前任务明确授权。
- `code-review` 是显式技能，不参与自动匹配。显式调用即授权启动两个并行的只读 Standards/Spec 审查子代理；该授权仅限只读审查，不允许修改、测试、提交、推送、部署或写外部系统。如果当前环境无法并行，则在当前会话串行完成两轴，并明确标记为降级执行。
- `grilling` 对范围足够大的环境事实调查，可启动全新 context window 的只读探索子代理；不得借它修改、测试、提交或写外部系统。
- 项目初始化写入 `AGENTS.md`；`CLAUDE.md` 只作为其他 harness 的兼容参考，未获明确要求时不修改。
- `prototype` 默认保留本地可复查工件；分支、提交、Issue pointer、push 和 PR 都需要当前任务明确授权。
- 技能之间的协作通过读取对应 `SKILL.md` 完成，不假设存在 Claude Code 的通用 Skill 工具或斜杠命令。
- 当前不包含 `tdd`。需要 TDD 时按项目既有测试规范手工执行，不会声称调用不存在的技能。

## 安装与更新

从包含 `.agents` 的 marketplace 根目录安装：

```powershell
codex plugin marketplace add "<本仓库目录>"  # 仓库根含 .agents/plugins/marketplace.json
codex plugin add "mattpocock-skills-zh@magpie-mattpocock-zh"
codex plugin list
```

更新时：

1. 比对上游中文仓库；
2. 修改本目录技能并更新 `.codex-plugin/plugin.json` 的版本；
3. 先移除旧安装，再重新执行 `codex plugin add "mattpocock-skills-zh@magpie-mattpocock-zh"`；
4. 核对 `codex plugin list` 显示 `installed, enabled`，并确认缓存版本与技能数。

不要手工修改 `~/.codex/plugins/cache`；它是安装结果。

## 排除项

`tdd`、`implement`、`diagnosing-bugs`、`codebase-design`、`improve-codebase-architecture`、`pr`、`grill-me`、`wizard`、`teach`、`wait-what`、`to-questionnaire`、`claude-handoff`、`loop-me`、`in-progress/*`、`misc/*` 和写作类实验技能未纳入本插件。需要时应按当前任务直接处理，或先取得明确授权后再安装，不要按上游 README 假设它们可用。
