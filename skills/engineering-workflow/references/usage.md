# Magpie 通用 AI 工程使用指南



这套配置按“指令决定入口、技能承载流程、MCP 执行操作、RTK 压缩输出”组织。所有开发、检查、调研和收尾均由主代理完成；工程编排 Hook 与子代理已于 2026-11-06 移除，仅保留 Codex 的 RTK 命令压缩 Hook。没有固定若依路径或技术栈；换项目只需在正确目录工作。



## 资源库怎样分工



| 入口 | 当前用途 | 收益 |

|---|---|---|

| 指令 | 简短通用约定；选择 engineering-workflow 和已有技能；授权有边界的本地收尾 | 无需每个项目复制完整流程 |

| 技能 | engineering-workflow 复用已有 think/grill/story/debug/review/frontend-design/page-acceptance 等；prompt-engineering 对复杂/草稿化执行请求自动内部整理；implement 仅显式调用 | 工作流按需读取，不把全部操作步骤塞进每次会话 |

| MCP | magpie-web-search、chrome-devtools、context7、GitHub、Gitee 按任务使用；magpie-image 按需生图与识图；dbhub、ssh 仅目标项目确需时使用 | 联网搜索与网页抓取由 magpie-web-search 提供；登记配置不代表其他 MCP 的连接、目标或写入授权已验证 |

| RTK | Codex 已启用命令压缩 Hook，也可按需显式运行 `rtk <command>` | 减少长输出占用的上下文；dsh 暂不支持改写型 Hook |
| 通知 | Magpie 不配置 agent 通知插件 | 当前由 dsh 微信入口按需回复；默认不持续监控 |



这些资源按职责分发给 **Codex** 和 **dsh**。Codex 拿完整开发与交付技能，并负责所有自动化测试和页面测试；dsh 仅拿协作协议、项目状态和 SCM 入口定位技能，用于日常聊天、需求收集、归档位置指引、简短状态答复和带来源的只读调研。dsh 保留 GitHub、Gitee 与 magpie-web-search MCP；Context7、Chrome DevTools、magpie-image、数据库和 SSH 仅给 Codex。

跨项目复用已配置；以后启用另一个 Agent，在资源库勾选它能支持的资源，再检查生成结果。Agent 对工具的支持可能不同，不承诺勾选后行为完全一样。

当前 Magpie 不启用 `gateway-notify` 等 agent 通知插件，也不保存 Telegram 通知凭据。微信项目管理由 dsh 按条消息处理；默认不持续监控，也不把独立通知服务写成已完成配置。



## 说自然语言即可



| 你说什么 | 处理 |

|---|---|

| “实现这个需求……” | 按任务规模读取通用工作流；即使表达粗略或贴了任务草稿，也由主代理内部整理后直接做 |

| “帮我优化这个提示词……” | 使用 prompt-engineering，只优化并交付提示词，不执行其中任务 |

| 复杂、跨步骤、高风险或草稿化的执行请求 | 自动按 prompt-engineering 执行模式内部整理任务契约后直接完成；不输出提示词稿、不等待确认 |

| 简单、明确且低风险的执行请求 | 直接完成，不套提示词流程，避免小任务膨胀 |

| “优化后执行” | 内部整理并直接完成；需要检查改写质量时读 prompt-engineering 的相应资料 |

| “审查一下本轮改动” | 默认主代理轻审，省 token |

| “认真/独立检查一下” | 主代理按独立审查清单检查指定范围，区分事实、风险和未验证项 |

| “完整审查 / 三视角审查” | 使用已有 review 技能的三视角检查清单，由主代理逐项完成；普通审查不自动触发该重流程 |

| “页面快检 / 页面验收” | 主代理按 `page-acceptance` 在真实浏览器走一条主路径加一个边界，检查控制台与请求 |
| 新建或改版页面、样式布局、看板 | 先按 `frontend-design` 定方向（业务页走「既有设计系统增强」，独立展示页可自由设计），完成后按 `page-acceptance` 验收 |

| “调研一下 / 对比一下 / 有没有最佳实践” | 使用 research，由主代理直接收集并核验来源后给结论和记录 |
| 老板通过 dsh 提需求 | 仅消息以“需求：”开头或明确要求整理需求时，dsh 简洁整理目标、验收点、约束和未决项，指出项目约定的需求入口；获授权且入口可用时才写入，否则返回可直接归档的内容 |
| dsh 被问“现在什么情况” | 读取项目状态和可访问的 Issue/PR/Git 信息，按“当前/进展/卡点/下一步”简短答复；信息过期或缺失时明确指出 |
| dsh 被问普通问题 | 默认日常聊天，不读项目、不扫描 Git、不建需求；可直接回答 |
| dsh 收到“调研：” | 只做带来源的联网调研并返回手机易读结论；用户明确要求归档时才形成项目收件箱简报，不写正式 research 记录 |
| Codex 接收 dsh 交接 | Codex 读取任务和项目状态，核验事实后按需进入 think/grill/story/implement，并负责所有验证、页面测试、文档与 Git 收尾 |
| “初始化/重配这个项目” | 使用 setup-project；普通实现不强制先生成整套配置 |

| “测试没问题，可以收尾” | 同步必要文档，按规则本地 commit，并推送到已有正常上游；不必重复提醒 |
| 功能完成、准备交付 | 由主代理自检并直接完成文档与 Git 收尾；涉及 UI 或中高风险时由主代理补充对应检查 |

| “先别提交 / 先别改文档” | 遵循当前任务要求，之后明确“可以收尾”才恢复 |

| “推送/部署到……” | 只有明确的目标和授权下才执行；提交不隐含这些动作 |



这是 Agent 读取规则后的行为约定，不是 Magpie 在输入发送前自动改写消息的程序。内部整理不能补造关键业务规则或扩大授权；只有会实质改变结果的歧义才需要追问。新技能或角色加载失败时可明确说名称并让 Agent 检查配置。



## 双 Agent 项目协作

当 Codex 和 dsh 共同参与一个项目时，使用项目内的 `docs/agents/ai-collaboration.md` 作为角色和交接协议。项目初始化时由 `setup-project` 生成；没有该文件时使用 `ai-collaboration` 的默认约定：Codex 是唯一开发、验证（含页面测试）与交付负责人；dsh 只负责日常聊天、需求收集、项目需求入口定位、带来源的只读调研和依据共享事实源回答当前状态。Git 和项目 Issue/PR/MR 是共享事实源。

不要假设两个 Agent 共享本地文件、分支、未提交改动或会话历史。dsh 回答状态前读取项目状态文件，并在可访问时对照任务单与 Git/PR 状态；回复保持适合手机阅读的短格式，不从聊天记录推断进度。新需求按项目配置指向 Issue/PR/MR 或本地需求清单；远程写入仍需当前任务授权，写入不可用时只返回待归档内容，不声称已保存。dsh 可对当前问题做只读调研，但不执行代码或页面测试、不修改最终状态/验证记录、不操作业务 Git；需求和明确要求归档的调研简报只能经受控收件箱脚本发布。

## 换一个项目



1. 在新项目目录打开 Codex，确认工作目录正确；不用复制 Magpie 全局指令。

2. 有 AGENTS.md 就读取；没有时从已有目录、构建文件和说明取得项目情况，不强迫每个项目先生成一套文档。

3. 项目文件只补实际差异：技术栈/编码规范、源码和文档位置、真实启动及测试命令、测试环境、业务边界、特殊 Git 约束。通用技能按需读取这些信息。

4. 自动本地提交可跨项目使用，但只提交本任务能确定归属的改动；非 Git 目录、无身份、无关暂存或项目禁止自动提交时报告原因，不修改 Git 全局身份。



Python、Java、前端工程用同一个流程，测试命令和文档目录来自各自项目，不预设 `pnpm`、`mvn` 或 `docs/agents`。多仓库任务分别核对并提交，不保证跨仓库原子交付。



## 一次实战



```text

实现商品列表按状态筛选，保持现有权限和分页逻辑。

先不运行测试，先别提交。

```



```text

让页面快检员检查本地商品列表，复用现有服务和测试账号。

走状态筛选→查询→详情，再看清空筛选后的页码，不修改业务数据。

```



```text

修复上述问题，允许复测受影响路径，先别提交。

```



```text

审查一下本轮 diff，不运行额外测试。

```



```text

功能测试没问题，可以收尾。

```



最后一步自动判断文档影响、核对本任务 diff 并创建本地提交，再推送到已有正常上游。无须更新的文档不改；已有无关暂存则停止提交，不清理其他人的改动。受保护/默认分支、上游不明或项目明确禁止时不推送并说明。push 返回成功后还要核对远端引用与本地 HEAD 一致、`@{u}` 能解析；单分支浅克隆首次推送可能缺少 remote-tracking，补齐普通 fetch refspec 并 fetch 复验后再报告已推送。用户报告测试通过标为用户确认。



只做开发、不要求测试时，也可在独立任务完成后本地提交，但报告未测试；代码提交不等于验收完成。

审查、测试、修复、推送和部署分别按语义授权，不因“自动化”扩大范围。



## 实测与限制



### 已移除的能力（2026-11-06）



工程编排 Hook 与子代理已从资源库移除：`library.json` 不再含 `hooks` 与 `subagents`，专用 Codex 子代理配置已移出活动目录。原 Hook 脚本、子代理配置和角色定义已移入 `C:\Users\s1a71\.config\magpie\backups`，需要时可取回。Codex 的 `~/.codex/hooks.json` 仅保留 RTK 命令改写 Hook；这是终端输出压缩，不负责会话提醒、任务编排、测试或 Git 收尾。



会话开始提醒、任务边界核对和收尾提醒现在全部由主代理按指令与技能直接执行，不再有脚本注入或外部触发点。



此前的 Hook 与全量验证记录已随失效配置一并删除；如需追溯，到资源库溯源仓库的 Git 历史中查找。



已在独立无依赖 Demo 验证过这套工作流（该验证记录已随失效配置一并删除，见溯源仓库 Git 历史）。基线 `1cab964` 到功能提交 `3013c82`：Codex CLI 自然语言实现状态筛选、读取工程技能、通过现有 6 项测试、更新 README、只暂存相关文件并提交；随后主代理用 Chrome DevTools 实际操作筛选与分页，关键状态/计数符合预期。该 Demo 早于本次移除，其中的角色与 Hook 环节不再是当前配置。



隔离 Git 案例中，修改 README 后能识别出预存的 `user-note.txt`，保留暂存区并停止提交；这条行为现在由主代理按指令直接执行。仍未通过/未验证项：提示词 CLI 曾把 PowerShell 命令错误交给 `cmd.exe`；Sol 故障降级未测。以上样本不代表所有 CLI/App 会话或路由都可靠；每次仍应核对实际结果。



完整通用权限、测试、历史续接和停止规则由 Magpie 指令维护；本技能只提供流程。提示词不是工具权限沙箱。模型/意图路由沿用现有配置；不要把请求模型名当成实际供应商证据，关键任务在 Sol 不可用时尤其要确认实际降级路由。



Git 收尾先对照任务开始时的暂存区；有既有/归属不明暂存就保留并阻止自动提交。无既有暂存时，只暂存本任务路径并复核暂存差异后再提交。



通用规则改 Magpie「指令」，工作流改资源库「技能」，不要只改 Codex 生成副本。MCP 按当前项目核对目标。备份在 `C:\Users\s1a71\.config\magpie\backups\generic-workflow-20261104-215744` 和 `constraints-20261104-221631`；其中含私人配置，不上传、不提交，恢复前先备份并按 manifest 选择。



## 全量真实验证（2026-11-06）

2026-11-06 对资源库做了一次全组件真实验证，覆盖当时的 6 个 MCP、4 个子代理、3 个 Hook、3 个插件、意图分类器与模型路由，以及真实 RuoYi-Vue-Plus 仓库上的实现→测试→审查→文档→提交→推送闭环。逐项证据与修复记录已随失效配置一并删除（见溯源仓库 Git 历史）；其中的子代理与 Hook 已于当日移除。要点：

- **MCP**：exa、github、context7、dbhub、ssh、chrome-devtools 六项在当时均有真实调用成功；Exa 曾因匿名额度被移除，后于 2026-11-06 恢复并改为自有 API key 认证。2026-11-07 Exa MCP 已卸载，当前为 8 个 MCP：chrome-devtools、context7、dbhub、gitee、github、magpie-image、magpie-web-search、ssh。ssh 修复了 profiles 配置（原指向 `~/.ssh` 目录，改指 `~/.codex/ssh-profiles.json`）。
- **子代理与 Hook（已移除）**：change-reviewer、page-checker、research-scout、delivery-closer 四个角色和三条 Hook 当时均有实测证据，现均已从资源库删除，改由主代理按指令和技能直接完成相同环节。
- **外部缺口**：初次验证时 Exa 匿名 MCP 额度耗尽，后配置自有 API key 解决；Exa MCP 本身已于 2026-11-07 卸载，联网搜索改由 magpie-web-search 统一提供。GitHub fork（s1a7xia 的 RuoYi-Vue-Plus）禁用了 Issues（`issue_write` 返回 410），issue 驱动开发需先启用 Issues 或换仓库。
- **一个环境问题**：本机 8080 被用户真实业务后端占用且 HTTP 无响应（只诊断未重启），页面快检的接口层验证因此受阻。

## 资源库维护与自检

源配置在 `C:\Users\s1a71\.config\magpie\library`，Codex 实际读取的是同步后的 `C:\Users\s1a71\.codex`。改指令或技能后，先同步再检查：

```powershell
magpie library sync
python C:\Users\s1a71\.config\magpie\library\skills\engineering-workflow\scripts\verify-library.py
```

自检是只读的结构检查：`library.json`、指令正文与哈希、全部技能副本。正常结果是 `0 errors`。自检不能证明 MCP 已连通、模型供应商可用、插件正常或项目测试通过。

插件查看用 `magpie plugin list`，模型组用 `magpie group <组名>`，实际请求去向用 `magpie usage --csv --last 2h` 的 `served_model` 核对。不要把 `magpie plugin list --json` 当轻量清单：它可能输出整份供应商目录，日常看状态用普通 `magpie plugin list`。

当前工程组合库启用两个插件：`magpie-deja` 历史召回（同项目、本地优先，参考历史仍需核对当前代码）和 Our Free Model（提供轻任务与分类器渠道）。Magpie 不保留通知插件；微信侧由 dsh 按需答复，不做持续监控。免费模型插件若报 `dataDir` 被占用，先确认另一个 Magpie 服务是否重复启动；这类插件错误不等同于工程技能损坏，也不能据此宣称模型组不可用，实际是否命中看 `usage --csv`。

免费通道不稳定时先看意图分类器：`group/ruoyi-daily` 的规则 2–4 带 `intent` 条件，由单一分类器模型判断；它坏掉时这些规则全部匹配不上，请求退到规则 5（Sol medium），不会报错但会静默降级。2026-11-06 实测 `our-free-model/qodercn/dfmodel` 连续 502/499，`loomy/DeepSeek-V4.1-Flash` 与 `qoder/dfmodel` 正常，已将分类器改为 `our-free-model/loomy/DeepSeek-V4.1-Flash`。核对方式：`magpie group group/ruoyi-daily` 看 classifier；`magpie usage --csv --last 60m` 看非 200 的 `requested_model`、`served_model`、`error_message`；必要时直接向 `http://127.0.0.1:3425/v1/chat/completions` 发一条 `ping` 实测通道。换通道后复验一次，不要重装插件。

MCP 报 `Transport send error ... /mcp/magpie/hub/codex` 时，先分别检查：Magpie 进程是否在、端口是否监听、当前 Codex 会话是否仍持有旧连接。端口可用但工具仍失败，按当前会话重连处理，不要同时重装 Magpie、改资源库和重建 MCP；一次只改一个变量。2026-11-06 实测：同一会话持续报错，新会话重连后 GitHub `get_me` 与搜索工具立即恢复，确认是会话级连接问题，不需要重装资源库。重连后仍应在当前会话实际调用一次搜索与 GitHub 再判定恢复。
## 历史召回插件维护



`@vshulcz/magpie-deja` 由 Magpie 插件管理，通过网关注入历史参考，不需要另配 MCP 或 Codex 原生 Hook。保持项目隔离默认值；历史参考仍需核对当前代码与任务状态。



2026-11-05 对 0.24.0 做了本机兼容修复：删除安装包重复的 `main` 入口，保留 `magpie.hooks`，真实跨会话召回已通过。升级或重装可能覆盖本机修复，需要复核加载状态。已安装 zstd 并完成历史增量索引，原先的 47 个压缩历史输入路径已补读；活动会话可能在持续写入时暂时显示一项待索引，不等同于历史覆盖缺口。详情见 [修复记录](C:/Users/s1a71/.config/magpie/backups/deja-repair-20261105-161031/repair-report.md)。


## 联网搜索与 GitHub 接入验证（2026-11-05 / 2026-11-07 更新）

2026-11-05 当时通过 Magpie MCP 路由实际调用了 Exa 的 `web_search_exa` 和 `web_fetch_exa`，并调用 GitHub MCP 的 `search_repositories` 与 `get_file_contents`：Exa 找到官方仓库后，GitHub 搜索定位到同一仓库并成功读取 README。详细记录见 [Exa + GitHub 验证记录](C:/Users/s1a71/.config/magpie/backups/exa-github-validation-20261105-165309/validation.md)。该记录是历史证据；当时使用的 Exa MCP 已于 2026-11-07 卸载，现由 magpie-web-search 提供搜索与抓取能力。

联网搜索统一使用 **magpie-web-search** MCP，对外提供 `web_search` 与 `web_fetch`，同时分发给 Codex 与 dsh。它底层调用 Magpie「设置 → 联网搜索」中的 provider，当前依次配置 Tavily、Exa、You 三家（`searchAll` 开启）：Tavily 与 Exa 使用用户自有 API key，You 走内置通道。**Exa MCP 与 Exa 搜索 API 是两层**——MCP 已于 2026-11-07 卸载，Exa API 仍保留在上述 provider 列表中，不要记成“已完全不用 Exa”。Key 通过 Magpie 的敏感值引用保存，不写入文档。

2026-11-06 当时 `magpie tool web_fetch` 已验证可读取普通网页（`example.com`、`baomidou.com`、GitHub 仓库页）；本机对 `api.github.com` 的抓取仍报 `EOF`，而 PowerShell 直连同一 API 返回 200，说明是该链路访问 GitHub API 的特定问题，不是全部联网能力故障。需要 GitHub API 数据时优先走 GitHub MCP。

搜索失败时按顺序排查：`magpie tools` 是否仍列出 `web_search`/`web_fetch`、Magpie 网关是否在监听、当前 provider 的 key 与额度、当前会话是否持有旧连接。不要在未确认原因前改 provider 顺序、卸载插件或重建 MCP。

GitHub 联用（2026-11-05 后续验证）：用户更新凭据后，Magpie 路由当时已暴露 GitHub 工具。当时 Exa 搜索 → GitHub 仓库搜索 → GitHub README 读取全链路通过。本轮只读，无远程写入；验证记录不包含凭据。

## 跨项目状态与编译检查

按需使用 `project-context`，并在项目初始化时由 `setup-project` 选择是否创建 `docs/agents/project-state.md`、`project-decisions.md`、`verification.md`。这些文件分别记录当前状态、确认决策和版本化验证证据；不是聊天归档。未初始化的普通项目不会被自动创建这些文件。

默认只检查本次改动涉及的前后端能否编译，不再选择交付档位或重复询问验证授权。前后端均有改动时分别编译；仅改一端时只编译该端，纯文档或不影响编译的配置改动只核对差异。复用项目已有编译/构建命令，跳过测试，不独立运行 lint、类型检查或自动化测试；已有构建命令内置的编译类型检查可保留。用户明确要求额外检查或暂不编译时按当次要求执行。编译失败或环境缺失时如实报告，不把编译通过等同于功能验收。

功能开发阶段只保证受影响的前后端能编译；`page-acceptance`（页面测试）是开发完成后的独立阶段，由用户主动发起，不在实现流程中自动执行。界面可见改动在页面测试通过前只记为“开发完成、未验收”。

GitHub、GitLab、Gitee 和本地 Issue 使用统一任务流程，由 `scm-collaboration` 按当前仓库选择平台传输方式：GitHub 与 Gitee 走 Magpie 内的 MCP，GitLab 走 `glab` CLI。2026-11-06 实测：Gitee MCP 认证后 `get_user_info` 返回账号 `x_X067`，25 个工具同时出现在 Codex 与当时的 WorkBuddy（2026-11-06 之后已换成 dsh）的 hub 中；`glab mcp serve` 可用但会暴露约 220 个工具、36 万字符 schema，因此不接入 hub，改用 CLI 按需调用。连接不等于写入授权；创建或更新 Issue、PR/MR、评论、推送和合并仍按当前任务授权执行。自动本地提交前，`engineering-workflow` 扫描暂存文本中少数高置信度凭证模式；它不是完整的秘密扫描器。

### 固定交付流程

可交付改动统一走“主代理自检 → 主代理直接更新文档与 Git”路径。按切片推进时，每个切片完成后各提交并推送一次，提交信息带该切片说明；同一需求只用一个分支。整批完成后停下等用户发起页面测试，测试或 review 发现的确认缺陷自动进入 `debug`，修完只重测受影响切片。

文档按 `project-context` 的事实规则增量更新；已有混杂暂存、冲突/变基、敏感信息、无提交身份、受保护/默认分支或归属不明时停止。常规功能分支在已持续授权时可普通 push 到已有上游；不强推、不自动建 PR/合并/发布，也不修改历史。若只完成提交不能安全推送，报告“已提交，未推送”。

收尾时由主代理自行核对本轮 Git 与文档变化，不依赖外部提醒；结论以真实代码和 Git 证据为准。
