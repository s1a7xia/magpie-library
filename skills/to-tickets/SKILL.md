---
name: to-tickets
description: 把 plan、spec 或当前对话拆成带 blocking edges 的 tracer-bullet tickets；默认写成项目内每票一个文件，只有明确授权时才发布到外部 tracker。
disable-model-invocation: true
---

# 拆成 tickets

把 plan、spec 或 conversation 拆成一组 **tickets**：tracer-bullet vertical slices，每个 ticket 都声明 **block** 它的 tickets。Tickets 是带依赖边的 task graph，不是按技术层排列的步骤清单。

## 授权与存储

- **默认**：写到项目内 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，每 ticket 一个文件，按 blockers-first 编号；不创建或修改外部 Issue。
- **只有用户明确要求发布到外部 tracker**，才按 `setup-matt-pocock-skills` 建立的配置调用 `gh`/`glab`/其他工具创建 issue、建立 blocking links、挂 sub-issue 或应用标签。
- 发布前先把拆分方案给用户确认；外部写入失败时保留本地文件并报告，不重试无关操作。
- 不 close 或 modify 任何 parent issue，除非当前任务明确要求。

## 流程

### 1. 收集 context

使用 conversation context 中已经存在的内容。如果用户把 reference（spec path、issue number 或 URL）作为参数传入，获取并完整读取其 body 和相关讨论。

### 2. 探索 codebase（可选）

如果还没有探索 codebase，先理解 code 当前状态。Ticket title 和 description 应使用项目 domain glossary vocabulary，并遵守相关 ADRs。寻找 prefactor code、让 implementation 更容易的机会：“Make the change easy, then make the easy change.”

### 3. 起草 vertical slices

把工作拆成 **tracer bullet** tickets。

<vertical-slice-rules>

- 每个 slice 都要贯穿每一层（schema、API、UI、tests）形成窄而完整的路径；必须是 vertical slice，不是某一层的 horizontal slice。
- 完成的 slice 可独立 demo 或 verify。
- 每个 slice 的大小必须能放进一个 fresh context window。
- 任何 prefactoring 都应先完成。
- 每个 ticket 声明真正 gate 它的 **blocking edges**；没有 blockers 的 ticket 可以立即开始。

</vertical-slice-rules>

**Wide refactors 是 vertical slicing 的例外。** 一个影响整个 codebase 的机械变更（例如 rename column 或 retype shared symbol）按 **expand–contract** 排序：先 expand，在旧形式旁加入新形式并保持可用；再按 package、directory 等 blast radius 分批迁移 call sites，每批一个 ticket 且被 expand block；最后 contract，在没有 caller 残留后移除旧形式。若单个批次无法独立保持 green，仍保留 sequence，但共享 integration branch，并让所有批次 block 最后的 integrate-and-verify ticket，只在最后承诺 green。

### 4. 向用户快速确认

把建议的拆分作为 numbered list 展示。每个 ticket 包含：

- **Title**：简短的描述性名称
- **Blocked by**：必须先完成的其他 tickets（如有）
- **What it delivers**：这个 ticket 打通的 end-to-end behaviour

询问用户：粒度是否合适、blocking edges 是否正确、是否需要合并或拆分。迭代到用户批准拆分。除非用户已经明确说“直接拆并落盘”，不要跳过这个确认点。

### 5. 写入 tickets

#### 默认：项目内本地文件

在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md` 下每 ticket 写一个文件，按 dependency order（blockers 优先）从 `01` 编号。每个文件的 “Blocked by” 列出它依赖的 number/title；每个文件只放一个 ticket，绝不合并成一个总文件。

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** 这个 ticket 从用户视角打通的 end-to-end behaviour，而不是逐层 implementation list。

**Blocked by:** gate 这个 ticket 的 numbers/titles，或 “None（can start immediately）”。

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

#### 显式授权：外部 issue tracker

按 dependency order（blockers 优先）每 ticket 发布一个 issue，让 blocking edges 能引用真实 identifiers。平台支持时使用 native blocking relationship，否则把 blocking issues 写进每个 ticket 的 “Blocked by”。如果来源是一个已存在的 issue，把每个 ticket 挂为它的 sub-issue。除非用户另有指示，可应用 `ready-for-agent` 标签；不要把这些 tickets 再送去 triage。

<issue-template>

## Parent

Tracker 上 parent issue 的 reference（如果来源是 existing issue；否则省略本 section）。

## What to build

这个 ticket 从用户视角打通的 end-to-end behaviour，而不是逐层 implementation list。

## Blocked by

gate 这个 ticket 的 references，或 “None（can start immediately）”。

## Acceptance criteria

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</issue-template>

### 6. 报告 frontier

列出所有 blockers 已完成的 tickets（可直接开始的 frontier）、仍需等待的 tickets，以及建议下一步。没有外部发布授权时，报告本地文件路径即可。
