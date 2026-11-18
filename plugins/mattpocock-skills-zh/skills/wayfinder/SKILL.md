---
name: wayfinder
description: 把单个 agent session 装不下的一大块工作规划成共享决策地图和 decision tickets，逐一解决直到路线清晰；默认使用项目内本地 Markdown，只有明确授权时才写入外部 issue tracker。
disable-model-invocation: true
---

# Wayfinder

一个松散想法出现了：它太大，单个 agent session 装不下，而且被 fog 包围；从这里到 **destination** 的路还看不见。Wayfinding 的目标是找到这条路，而不是朝 destination 猛冲。这个技能把路径绘制成共享地图，再逐个处理 **decision tickets**（承载需要决策才能解决的问题，而不是要执行的 build slices），直到路线清晰。

不同 effort 的 destination 不同，为它命名是 charting 的第一个动作；它塑造每个 ticket。它可能是一份要 hand off 并迭代的 spec、一个必须在 planning 前确定的 decision，或 data-structure migration 之类原地完成的 change。Map 与领域无关：engineering work、course content，或任何符合这个形状的事项都可以。

## 只规划，不动手

Wayfinder 默认用于 **planning**：每个 ticket 解决一个 decision；当别人动手前已经没有任何事情需要决定、路径完全清晰时，map 才算完成。想直接做工作的冲动通常表示已经到达 map 边缘，该 hand off 了。Effort 可以在 **Notes** 中覆盖这个默认值，把 execution 纳入 map；否则只产出 decisions，不产出 deliverables。

## 授权与存储

- **默认使用项目内本地 Markdown**：地图放在 `.scratch/<effort>/wayfinder.md`，tickets 放在 `.scratch/<effort>/tickets/<NN>-<slug>.md`。这是无外部 tracker 授权时的 canonical artifact。
- **只有用户明确授权写入外部 issue tracker**，才按项目配置把 map 和 tickets 建成 Issue、设置 labels、assignee、native blocking links 或 resolution comments。
- 用户已配置外部 tracker 但本次未授权写入时，可以只读现有 Issue 作为事实来源；新建和修改仍留在本地。
- 调用 wayfinder 即授权为 research ticket 启动只读调查子代理；该授权不包含 worktree、分支、push、PR、测试或其他外部发布。
- 不读取或输出凭据；敏感信息只记录存放位置。

## 用名称引用

每张地图和每个 decision 都有 **name**（title）。在所有给人看的内容里，包括叙述和 Decisions-so-far，都用 name 引用，不要只写裸 id、number 或 slug。一堵 `#42, #43, #44` 很难读；name 一眼就能看懂。Id/URL 可以放在 name 的链接里，但不单独替代 name。

## 共享地图

Map 是 **index**，不是 store。它列出已经做出的 decisions，并指向保存细节的 tickets；一个 decision 只存在一个地方，也就是它的 ticket。因此 map 不复述细节，只给 gist 和 link。

地图和 tickets 的物理表达取决于存储位置：本地 Markdown 使用文件路径和显式 `Blocked by`；真实 tracker 使用 issue id 和 native dependency links。没有 tracker 时默认本地。

### Map 正文

Map 是低分辨率的全局视图，每个 session 加载一次。Open tickets 不列在里面；它们是 open child items，通过目录/查询找到。

```markdown
# <Effort name> — Wayfinder Map

## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort; storage mode and authorization boundary>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

每个 ticket 的 body 是一个问题，大小控制在一个 100K token agent session 内：

```markdown
# <Ticket title>

## Question

<the decision or investigation this ticket resolves>

## Type

<research | prototype | grilling | task>

## Blocked by

<file names/links or issue references; None if immediately available>

## Status

open
```

`wayfinder:<type>` labels 只用于外部 tracker 表达类型；本地文件用 `## Type`。这些是 decisions，不是 implementation work，绝不带 `ready-for-agent` 这类 triage label。

Session **claim** ticket 的方式，是在任何工作开始前先把 ticket 标记为 assigned/in-progress，这样并发 sessions 会跳过它。Local 模式在文件里写 `Status: in-progress` 和 claim 时间/session 标识；外部 tracker 使用 assignee。

Blocking 在外部 tracker 优先使用 native dependency relationship；只有不支持时才退回 body convention。一个 ticket 的所有 blockers 都满足后，它就是 **unblocked**；**frontier** 是 open 且 unblocked 的 tickets，也就是已知世界的边缘。

答案不写进 ticket 的 Question，而是在 resolution 时记录。解决 ticket 时产生的 assets 用路径/链接引用，不粘贴进 body。

## Ticket 类型

每个 ticket 都是 **HITL**（human in the loop，与能代表自己发言的人类一起处理）或 **AFK**（agent 独立驱动）。HITL ticket 只能通过 live exchange 解决；agent 绝不能替人类回答。一旦 grilling agent 自问自答，它就已经坏了。

- **Research**（AFK）：阅读 documentation、third-party APIs，或 knowledge bases 等 local resources，找出某项 decision 正在等待的事实。交给只读调查子代理调用 `research`；主会话继续推进不依赖该事实的 tickets。当需要当前 working directory 外的知识时使用。
- **Prototype**（HITL）：通过 cheap、rough、concrete artifact 提高讨论 fidelity，例如 outline、rough take、stub，或调用 `prototype` 写 UI/logic code。Prototype 作为 asset 链接。当核心问题是 "how should it look" 或 "how should it behave" 时使用。
- **Grilling**（HITL）：Conversation。默认类型。始终读取并遵循 [`grilling`](../grilling/SKILL.md) 和 [`domain-modeling`](../domain-modeling/SKILL.md) 两个技能的 `SKILL.md`。
- **Task**（HITL 或 AFK）：做出 _decision_ 前必须完成、但本身没有要 decide、prototype 或 research 的 manual work。例如注册服务以评估其 API、配置访问权限、移动数据以看清 shape。这是唯一会 _do_ 而不是 decide 的类型；它凭借解锁 decision 而存在，而不是交付 destination。Agent 能独立完成时采用 AFK，否则给人类精确 checklist（HITL）。工作完成后 resolved；答案记录做了什么，以及后续 tickets 依赖的事实（credentials location、new URLs、row counts 等）。

## 战争迷雾

Map 是 _有意_ 不完整的：不要描绘你还看不见的东西。Tickets 之外是 fog：那些你能感觉到以后会来的 decisions 和 investigations，但它们悬在仍未解决的问题之上，暂时还无法钉住。解决一个 ticket 会清掉它前方的一片 fog，把现在已经能说明的问题升级成新的 tickets；一次一个，直到通向目标的路清楚且没有 tickets 剩下。

Map 的 **Not yet specified** section 用来记录这种朦胧视野：怀疑中的问题、之后要回访的区域。这里是通往 destination、尚未探索的 frontier；所有内容都在 scope 内，只是还不够清晰，无法成为 ticket。可以按视野允许的粗细来写；它也是协作者阅读这个 effort 走向时的路标。

**Fog or ticket?** 测试标准是你现在能不能把问题说清楚，而不是现在能不能回答它。

- **Ticket when** 问题已经清晰，即使它被 blocked、现在不能处理。
- **Not yet specified when** 你还不能把它说得那么清楚。不要把 fog 预先切成 ticket-sized pieces：fog 比 ticket 粗，frontier 到达后，一片 fog 可能升级成多个 tickets，也可能一个都没有。

**Not yet specified** 排除已经决定的内容（Decisions so far）、已经是 live ticket 的内容，以及 out of scope 的内容。

## 超出范围

Fog 只会聚集在通往 destination 的方向。Destination 固定 scope，因此超出它的工作是 **out of scope**，不是 fog，也不属于 **Not yet specified**。它写进 map 单独的 **Out of scope** section：你有意识地排除在这个 effort 之外的工作。决定它属于这里的是 scope，而不是 sharpness。

Out-of-scope work 永远不会 graduate；frontier 会停在 destination。只有重画 destination 时它才会回来，而且应成为新的 effort，不是 resumption。

把某事排除出 scope 是 scoping act，不是 route 上的一步。如果已有 ticket 被发现位于 destination 之外（charting 时被错误地划入 scope，或被某次 resolution 暴露），应 **close it**，并在 **Out of scope** section 中留一行：gist 加上它为何 out of scope，并链接到 closed ticket。不要把它放进 **Decisions so far**；后者只记录真正走过的路线，scope 边界不是路线上的一步。

## 调用

两种模式。无论哪种，**每个 session 绝不要 resolve 超过一个 ticket**，research tickets 除外。

### 绘制地图

用户带着松散想法调用。

1. **Name the destination.** 读取并遵循 [`grilling`](../grilling/SKILL.md) 和 [`domain-modeling`](../domain-modeling/SKILL.md) 两个技能的 `SKILL.md`，确定 map 要找到的 spec、decision 或 change。Destination 固定 scope，所以先解决它。
2. **Map the frontier.** 再 grill 一次，这次采用 **breadth-first**：覆盖整个空间，而不是深入一条 thread，浮现 open decisions 和现在可开始的 first steps。**如果没有 fog**，说明路径已经清晰，整个 journey 一个 session 就能完成，你不需要 map。停止并询问用户如何继续。
3. **Create the map**：填好 Destination 和 Notes，Decisions-so-far 为空，把 fog 勾勒进 **Not yet specified**。默认写入 `.scratch/<effort>/wayfinder.md`。
4. **Create the tickets you can specify now** 作为 map 的 child items，然后第二遍再 wire blocking edges：
   - 本地模式：每个 ticket 一个文件，使用相对路径互相引用；不要用会误解的占位符。
   - 外部 tracker：issues 需要 ids 后才能互相引用，再设置 native blocking links。
   Wiring 会把它们分成 frontier 和 blocked；现在还说不清的都留在 **Not yet specified**。
5. **处理 research tickets。** 对刚创建的每个 research ticket 启动使用全新 context window 的只读调查子代理去调用 `research`；只读查证，不做实现。findings 写入本地 notes 文件，并从 ticket 留 context pointer。不创建 branch、不 push、不开 PR。
6. 停止。Charting 是一个 session 的工作；不要在这个 session 中手动 resolve tickets。

### 沿着地图推进

用户用 map（路径、URL 或 number）调用。Ticket 是 **optional**；没有 ticket 时，你选择下一个 decision，而不是用户选择。

1. 加载 **map**：低分辨率视图，而不是每个 ticket body。
2. 选择 ticket。用户点名就用它；否则按顺序拿第一个 frontier ticket。**Claim it**：任何工作开始前先标记 in-progress/assign 给自己。
3. 按它的 `## Type` 或 `wayfinder:<type>` label 所命名的类型 resolve 它。读类型，而不只是 body。按需 **zoom**，只在需要时获取相关或已关闭 ticket 的完整内容；读取 `## Notes` 提到的技能。不确定时读取并遵循 [`grilling`](../grilling/SKILL.md) 和 [`domain-modeling`](../domain-modeling/SKILL.md) 两个技能的 `SKILL.md`。
4. 记录 resolution：
   - 本地模式：在 ticket 追加 `## Resolution`，把状态改为 `resolved`，并向 map 的 Decisions-so-far 追加 context pointer。
   - 外部 tracker（已授权）：把答案作为 resolution comment 发布，close issue，并更新 map 的 Decisions-so-far。
5. 添加新浮现的 tickets；把答案已经说清的 fog graduate 成 ticket，并从 **Not yet specified** 清掉每个已升级 patch。如果答案表明某个 ticket 位于 destination 之外，将其 **rule out of scope**，而不是当作路线的一部分解决。如果这个 decision 使 map 其他部分失效，更新或删除那些 tickets。

用户可能并行运行 unblocked tickets，所以要预期其他 sessions 同时编辑 tracker。若没有明确的多写入者协调授权，默认只有一个写入者。
