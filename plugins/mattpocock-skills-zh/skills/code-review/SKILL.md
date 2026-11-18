---
name: code-review
description: "从固定点（commit、branch、tag 或 merge-base）开始，按 Standards（代码是否符合本仓库记录的编码标准？）和 Spec（代码是否符合来源 issue/spec 的要求？）两个轴线审查变更；由两个并行只读子代理分别审查，再并排汇总。适用于用户要求审查 branch、PR、进行中的变更或“review since X”时。"
disable-model-invocation: true
---

对用户提供的 fixed point 与 `HEAD` 之间的 diff 做双轴 review：

- **Standards**：代码是否符合这个 repo 记录下来的 coding standards？
- **Spec**：代码是否忠实实现来源 issue / spec？

两个轴线由**两个并行只读子代理**分别完成，避免彼此的上下文互相污染，再由本技能汇总。每个子代理都从全新的 context window 开始。

用户显式调用或要求本技能进行审查，即授权启动这两个子代理。该授权只覆盖只读审查：子代理不得修改文件、运行测试、提交、推送、部署或写入外部系统。如果当前环境无法启动并行子代理，就在当前会话中依次完成两个轴线，并在报告中明确说明这是降级执行。

Spec 来源优先在本地 spec、issue reference 或项目文档中查找；外部 tracker 不存在或未授权访问时，明确报告“no spec available”，不要自行创建 Issue。

## 流程

### 1. 确定 fixed point

用户说的任何内容都是 fixed point：commit SHA、branch name、tag、`main`、`HEAD~5` 等。如果用户没有指定，就询问。

先捕获一次 diff command：`git diff <fixed-point>...HEAD`（three-dot，因此比较对象是 merge-base）。同时用 `git log <fixed-point>..HEAD --oneline` 记录 commits 列表。

继续前，确认 fixed point 能解析（`git rev-parse <fixed-point>`），并且 diff 非空。错误 ref 或空 diff 应该在这里失败，而不是进入后续审查阶段后才失败。

### 2. 找到 spec 来源

按以下顺序寻找来源 spec：

1. Commit messages 中的 issue references（`#123`、`Closes #45`、GitLab `!67` 等），按 tracker doc 中的 workflow 获取。
2. 用户作为 argument 传入的 path。
3. `docs/`、`specs/` 或 `.scratch/` 下与 branch name 或 feature 匹配的 spec 文件。
4. 如果什么都找不到，询问用户 spec 在哪里。如果用户说没有 spec，**Spec** 轴线跳过并报告 “no spec available”。

### 3. 找到 standards 来源

搜索 repo 中所有记录代码应该如何写的文件。当 `CODING_STANDARDS.md` 或 `CONTRIBUTING.md` 存在时，必须列入清单。

在 repo 自己记录的 standards 之外，Standards 轴线始终带有下面的 **smell baseline**：一组固定的 Fowler code smells（_Refactoring_ 第 3 章），即使 repo 没有任何约定也适用。有两条规则：

- **The repo overrides.** 已记录的 repo standard 永远优先；如果它认可 baseline 会标记的东西，就压制该 smell。
- **Always a judgement call.** 每个 smell 都是带 label 的 heuristic（例如 "possible Feature Envy"），不是硬性违规；和这里的其他 standard 一样，跳过 tooling 已经强制检查的内容。

每个 smell 按 _what it is_ -> _how to fix_ 读取，并对照 diff：

- **Mysterious Name**：function、variable 或 type 的名称没有说明它做什么或装什么。-> rename it；如果找不到诚实名称，设计本身可能浑浊。
- **Duplicated Code**：同一 logic shape 出现在多个 hunk 或 file 中。-> 抽出共享形状，让两边调用。
- **Feature Envy**：method 访问另一个 object 的 data 多于自己的 data。-> 把 method 移到它羡慕的数据上。
- **Data Clumps**：同几组 fields 或 params 总是一起出现。-> 包成一个 type 来传。
- **Primitive Obsession**：primitive 或 string 代替了值得拥有自有 type 的 domain concept。-> 给该 concept 一个小 type。
- **Repeated Switches**：对同一 type 的相同 `switch`/`if` cascade 在改动中重复。-> 换成 polymorphism，或共享一个 map。
- **Shotgun Surgery**：一个 logical change 迫使 diff 分散修改很多文件。-> 把一起变化的东西收拢进一个 module。
- **Divergent Change**：一个 file 或 module 因多个无关原因被修改。-> 拆分，让每个 module 只因一个原因变化。
- **Speculative Generality**：为 spec 没有的需求增加 abstraction、params 或 hooks。-> 删除它，inline 回来，直到有真实需要。
- **Message Chains**：caller 不该依赖的长链式导航 `a.b().c().d()`。-> 把这段导航藏到第一个 object 的一个 method 后面。
- **Middle Man**：class 或 function 基本只是在继续委托。-> 删掉它，直接调用真实目标。
- **Refused Bequest**：subclass 或 implementer 忽略或 override 了继承来的大部分内容。-> 去掉 inheritance，使用 composition。

### 4. 并行启动两个子代理

同时发起两个子代理调用，前台等待，并汇总它们返回的报告。

**Standards 子代理 prompt** 应包含：

- 完整 diff command 和 commit list。
- Step 3 找到的 standards-source files，以及 **完整粘贴 Step 3 的 smell baseline**（子代理没有其他途径获得它）。
- 任务简报："对每个相关 file/hunk，报告：(a) diff 违反已记录 standard 的位置，并引用 standard（file + rule）；(b) 发现的 baseline smell，写出名称并引用对应 hunk。区分硬违规与判断项：已记录 standard 的违反可以是硬违规；baseline smell 始终是判断项；repo 已记录的 standard 优先于 baseline。跳过工具已经强制检查的内容。400 字以内。"

**Spec 子代理 prompt** 应包含：

- diff command 和 commit list。
- spec 的 path 或已获取内容。
- 任务简报："报告：(a) spec 要求但缺失或只完成一部分的内容；(b) diff 中未被要求的行为（scope creep）；(c) 看似实现但实现方式错误的要求。每项发现都引用 spec 原文。400 字以内。"

如果缺少 spec，跳过 Spec 子代理，并在最终报告中注明。

两个子代理只返回审查报告，不得修改、测试、提交、推送或发布。若并行子代理不可用，在当前会话中依次完成同样两项审查，并明确标记为降级执行。

### 5. 汇总

在 `## Standards` 和 `## Spec` headings 下展示两个 reports，可原样或轻微清理。**不要**合并或重新排序 findings；这两个轴线刻意保持分离（见 _为什么是两条轴线_）。

最后用一行总结：每个轴线的 findings 总数，以及每个轴线内最严重的问题（如果有）。不要跨轴线选一个总冠军；分离就是为了避免这种 reranking。

## 为什么是两条轴线

一个变更可能通过其中一个轴线，但失败在另一个轴线：

- 代码符合所有 standard，但实现了错误的东西 -> **Standards pass, Spec fail.**
- 代码完全符合 issue 要求，但破坏了项目约定 -> **Spec pass, Standards fail.**

分开报告能避免一个轴线掩盖另一个轴线。

