# Magpie 组合拳依赖与换机恢复

本文记录这套组合拳在本机的实际依赖，以及换电脑后怎样恢复成同一套工作环境。

核对日期：2026-11-11。MCP、插件和记忆的最新清单见 [ENVIRONMENT.md](ENVIRONMENT.md)，白名单快照见 [config/environment.snapshot.json](config/environment.snapshot.json)。版本和路径会变化，恢复后以实际命令输出为准。

## 1. 什么必须一致

要得到相同的工作方式，以下五类内容需要一起恢复：

| 类别 | 作用 | 是否在本仓库 |
|---|---|---|
| 全局协作指令 | 通用协作、权限和已有改动保护；工作流与收尾策略在项目 AGENTS.md | 正文在 `instructions.md`，生成副本不在本仓库 |
| 16 个技能 | 各阶段的方法、模板和检查门槛 | 在 `skills/` |
| `library.json` | 哪些技能和 MCP 分发给哪些 Agent | 不在本仓库，属于机器状态 |
| MCP 与 CLI | 搜索、文档、代码托管、数据库、SSH、浏览器等执行能力 | 配置不在本仓库，程序需另行安装 |
| 凭据和登录态 | 模型供应商、代码托管、数据库、SSH、浏览器会话 | **永不入库** |

只克隆本仓库，得到的是可阅读和可追溯的技能文本，不是一套已经生效的运行环境。

## 2. 本机基线

### 2.1 核心程序

| 依赖 | 本次核对版本 | 必要性 | 用途 |
|---|---:|---|---|
| Magpie | `0.1.3488` | 必需 | 指令、技能、MCP 的统一分发与托管 |
| Codex | 随桌面端安装 | 必需 | 当前主要开发 Agent |
| Git | `2.54.0.windows.1` | 必需 | 版本追溯、切片提交、推送 |
| Node.js | `v24.17.0` | 必需 | `answer-me-with-html` 要求 Node.js 20+；部分 MCP 通过 `npx` 启动 |
| npm / npx | `11.13.0` | 必需 | 启动 stdio MCP 和部分技能工具 |
| Python | `3.13.14` | 必需 | 运行资源库健康检查和暂存区密钥扫描 |
| PowerShell | `7.6.9` | 当前平台必需 | Windows 主要命令环境 |

### 2.2 按平台或场景选用

| 依赖 | 本次核对版本 | 必要性 | 用途 |
|---|---:|---|---|
| `gh` | `2.103.2` | 可选 | GitHub CLI 兜底；MCP 不可用时的只读排查 |
| `glab` | `1.128.0` | 可选 | GitLab 任务和 MR；当前明确不启用 `glab mcp serve` |
| `rtk` | `1.1.0` | 可选 | 压缩终端输出，减少上下文占用 |
| `agent-browser` | 0.41.2（2026-11-11 核对，已在 PATH） | 可选 | 浏览器自动化；未安装 CLI 时页面验收使用当前 Agent 已有浏览器能力 |
| Google Chrome | 已安装 | 页面验收时使用 | `C:\Program Files\Google\Chrome\Application\chrome.exe` |
| Microsoft Edge | 已安装 | 页面验收后备 | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` |

Java、Maven、pnpm 等属于具体项目的构建依赖，不属于这套通用资源库的固定前置条件。项目初始化时从仓库实际构建文件读取并写入 `docs/agents/project-state.md`。

### 2.3 可选安装命令

只在确实缺少且用户同意时安装：

```powershell
# 浏览器自动化 CLI
npm install -g agent-browser
agent-browser install

# 代码托管 CLI，按实际平台选用
winget install GitHub.cli
winget install GLab.GLab

# RTK
winget install rtk-ai.rtk
```

安装后重新打开终端，并实际运行一次版本命令确认 PATH 生效。不要仅凭安装程序退出码判断可用。

## 3. 技能分发

### 3.1 共享目录

当前配置：

- `sharedSkills = true`
- `mcpHub = true`
- 技能数：16
- 资源库源：`C:\Users\<user>\.config\magpie\library\skills\`
- Agent 共享目录：`C:\Users\<user>\.agents\skills\`

本机 `~\.agents\skills` 下 16 项均是指向资源库的 Junction，不是独立副本。修改源文件后，共享目录立即看到同一内容；`magpie library sync` 负责重新写入各 Agent 的加载配置和生成物。

`sharedSkills` 和逐 Agent 勾选是两个独立控制：

- `sharedSkills=true`：技能同时放进 `~/.agents/skills`，供支持该共享目录的 Agent 和工具读取；
- `skills[].agents`：Magpie 在界面里勾选该技能由哪些 Agent 正式启用。

“共享目录里看得到”不等于“每个 Agent 都已启用”。

### 3.2 当前逐 Agent 勾选

| 技能 | 当前 Agent |
|---|---|
| `agent-browser` | claude, codex, dsh, qoder, workbuddy |
| `answer-me-with-html` | claude, codex, dsh, qoder, workbuddy |
| `debug` | codex |
| `database-design` | codex |
| `frontend-design` | codex |
| `grill` | codex |
| `implement` | codex |
| `page-acceptance` | codex |
| `powershell-windows` | codex |
| `research` | codex |
| `review` | codex |
| `rules` | codex |
| `ruoyi6` | codex |
| `setup-project` | codex |
| `story` | codex |
| `think` | codex |

全局指令当前只分发给 `codex`：

```text
instructions.agents = ["codex"]
```

这意味着：换到 Claude、Qoder 或其他 Agent 时，即使共享目录读得到技能，也不自动获得同一套全局规则和逐项启用状态。需要先在 Magpie 中明确勾选并重新同步。

## 4. MCP 清单

当前登记 9 个 MCP。因为 `mcpHub = true`，Agent 会话通常只看到一个由 Magpie 托管的聚合入口，实际服务由 Magpie 启动和转发；下表是逻辑服务清单。

不要在本仓库记录真实令牌、完整认证头或 DSN。

| MCP | 传输 / 地址 | 当前 Agent | 作用与依赖 |
|---|---|---|---|
| `context7` | HTTP `https://mcp.context7.com/mcp` | codex | 查框架和库的官方用法 |
| `dbhub` | stdio `npx -y @bytebase/dbhub@1.5.0 --transport stdio` | codex | 本机 PostgreSQL；完整 DSN 在 `library.json`，不在此展开 |
| `gitee` | HTTP `https://api.gitee.com/mcp` | codex, dsh | Gitee Issue/PR；Bearer Token 在 `library.json` |
| `github` | HTTP `https://api.githubcopilot.com/mcp/` | codex, dsh | GitHub 仓库和 Issue/PR；Bearer Token 在 `library.json`；`gh` 可作为 CLI 兜底 |
| `magpie-image` | stdio `magpie.exe mcp image` | codex | 图片生成与识图；依赖本机 Magpie 可执行文件和模型配置 |
| `magpie-vision` | stdio `magpie mcp vision` | codex | 独立图像识别入口；依赖 Magpie 和模型配置 |
| `magpie-memory` | stdio `magpie.exe mcp memory` | claude, codex, dsh, qoder, workbuddy | 跨 Agent 共享的项目记忆；依赖本机 Magpie 可执行文件 |
| `magpie-web-search` | stdio `magpie.exe mcp search` | codex, dsh | 联网搜索；`research` 的首选搜索入口 |
| `ssh` | stdio `npx -y @hypnosis/ssh-mcp-server` | codex | SSH 目标操作；读取 `SSH_PROFILES_FILE=~/.codex/ssh-profiles.json` |

说明：

- `dbhub` 不是通用数据库万能入口；当前配置只指向本机 PostgreSQL。换项目时先核对目标库。
- `ssh` 只有在 `~/.codex/ssh-profiles.json` 中有对应配置时才可用。
- `github` 与 `gitee` 的 HTTP 头部包含真实认证信息，由 Magpie 保存；不要复制到聊天、文档或截图。
- 登记成功、进程在监听、MCP hub 显示绿色，都不等于当前 Agent 会话已挂载或已获写权限。

### 4.1 实际连通性

本次核对了配置和进程级依赖；**没有对所有 MCP 做全量连通测试**。

恢复后应按用途做一次最小只读验证：

| MCP | 最小验证 |
|---|---|
| `context7` | 查一个已安装库的官方用法 |
| `magpie-web-search` | 搜一条带来源的公开信息 |
| `github` / `gitee` | 读取当前仓库或一个已知 Issue；不做写入测试 |
| `dbhub` | 连接目标库并只读查询版本或一张已知表 |
| `ssh` | 连接已登记目标并运行只读命令 |
| `magpie-image` | 仅在当前请求授权时识别本地测试图；不为连通性检查自动生成付费图片 |

不要用“写入成功”作为首次连通性检查。写入必须另有明确授权，并先确认目标环境。

## 5. 凭据与机器状态

以下位置只记录用途，不记录值：

| 路径 | 内容 |
|---|---|
| `~/.config/magpie/library.json` | 技能与 MCP 分发、HTTP 认证头、dbhub DSN 等 |
| `~/.config/magpie/sync.json` | WebDAV/S3/GitHub 同步目标和加密配置 |
| `~/.config/magpie/sync-state.json` | 同步游标与状态 |
| `~/.config/magpie/providers.json` | 模型供应商及密钥 |
| `~/.config/magpie/logins.json` | 订阅登录状态 |
| `~/.config/magpie/settings.json` | Magpie 运行设置 |
| `~/.config/magpie/backups/`、`auto-backups/` | Magpie 本机备份 |
| `~/.codex/config.toml` | Codex 模型、MCP 等运行配置 |
| `~/.codex/AGENTS.md` | Magpie 生成的全局指令副本 |
| `~/.codex/ssh-profiles.json` | SSH MCP 的目标配置 |
| `~/.agents/skills/` | 16 个技能的共享 Junction |
| 项目内 `.ruoyi-auth.json`、浏览器状态 | 页面验收登录态；本地生成，不入库 |

原则：

- 加密整包备份可以包含这些机器状态；普通 Git 仓库不能。
- `library.json` 含有认证信息，不能直接提交或发到聊天里。
- 浏览器登录态和 `.ruoyi-auth.json` 不由本仓库保存。
- `*.magpie-backup`、`sync.json`、`sync-state.json`、`sync.lock` 已在 `.gitignore` 中排除。

## 6. 换机恢复

### 方案 A：推荐，恢复 Magpie 加密备份

这是恢复完整工作方式的路径。备份可含供应商、密钥、模型设置、Agent 配置和资源库。

旧电脑：

```powershell
magpie backup --sign-ins C:\path\to\magpie-full.magpie-backup
```

`--sign-ins` 会把订阅和插件登录态一并封装备份；不需要时省略。备份文件本身仍受 passphrase 保护，但应视为敏感文件。

新电脑：

1. 安装 Magpie。
2. 恢复整包：

   ```powershell
   magpie restore C:\path\to\magpie-full.magpie-backup
   ```

3. 重新同步技能和指令：

   ```powershell
   magpie library sync
   ```

4. 运行结构校验：

   ```powershell
   python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
   ```

5. 补装不属于 Magpie 整包的 CLI：Node.js、Python、Git、`gh` / `glab`、RTK、`agent-browser`，按实际项目需要选择。
6. 打开新的 Agent 会话，实际调用技能和一个只读 MCP，确认不是“配置存在但会话未挂载”。

如果同步由 WebDAV、S3 或 GitHub 加密仓库负责，安装 Magpie 后也可以配置同一同步地址，让机器状态自动回来；恢复后仍执行 `magpie library sync` 和健康检查。

### 方案 B：只有 Git 仓库

适用于阅读、比对或重建技能文本，不适用于一键恢复。

```powershell
git clone git@github.com:s1a7xia/magpie-library.git
```

还需要另外完成：

1. 在 Magpie 中创建或恢复 `library.json`；
2. 重新登记 8 个 MCP 和认证信息；
3. 重新配置模型供应商；
4. 重新勾选技能分发给哪些 Agent；
5. 执行 `magpie library sync`；
6. 重新建立 SSH、数据库和浏览器登录态。

不要把仓库直接当成完整的 Magpie 配置目录：本仓库没有 `library.json`，也不保存密钥和机器状态。

## 7. 恢复后校验

### 7.1 结构与同步

```powershell
magpie --version
magpie library sync
python "$env:USERPROFILE\.config\magpie\library\scripts\verify-library.py"
```

健康检查验证：

- `library.json` 可解析；
- 技能和 MCP 列表非空；
- Codex 指令块存在且与资源库正文一致；
- 资源库与 `~/.agents/skills` 的文件哈希一致。

它**不验证**：

- MCP 是否连通；
- 模型供应商是否可用；
- 浏览器、数据库、SSH 目标是否正确；
- 项目业务测试是否通过。

### 7.2 Agent 与技能

```powershell
magpie ls
Get-ChildItem "$env:USERPROFILE\.agents\skills" | Select-Object Name,LinkType,Target
Get-Content "$env:USERPROFILE\.codex\AGENTS.md" -TotalCount 20
```

预期：

- `magpie ls` 能看到 Codex；
- `~/.agents/skills` 有 16 项，并指向资源库；
- `~/.codex/AGENTS.md` 含 `<!-- magpie:begin` 到 `<!-- magpie:end -->` 的指令块。

### 7.3 MCP

```powershell
magpie healthcheck
magpie tools
```

`magpie healthcheck` 只能说明 Magpie 网关有响应，不能证明每个 MCP 已连通。最终以当前 Agent 会话中的一次实际只读调用为准。

### 7.4 浏览器

```powershell
agent-browser --version
```

2026-11-11 本机已核对 `agent-browser 0.41.2` 且在 PATH。换机需重新确认；CLI 可选，优先遵守项目/用户指定工具并复用现有宿主会话，目录存在不能证明命令可用。

## 8. 常见故障

| 现象 | 先检查什么 | 处理 |
|---|---|---|
| 技能改了但不生效 | 是否直接改了镜像仓库 | 改 `~/.config/magpie/library/`，再 `magpie library sync` |
| Agent 看不到某个技能 | `skills[].agents` 是否勾选、Agent 是否重启 | 在 Magpie 中勾选，重新同步，开新会话 |
| 全局规则不一致 | `verify-library.py` 的哈希检查 | 修正资源库 `instructions.md`，重新同步，不要手改生成副本 |
| MCP 显示已配置但调用失败 | 当前会话是否挂载、Magpie 是否运行、认证是否过期 | 先查实际错误，再修目标；不要无变化重复重试 |
| `dbhub` 连接失败 | 本机 PostgreSQL、端口、DSN、目标库 | 核对 DSN 和目标环境；不要把 DSN 贴进报告 |
| `github` / `gitee` 返回 401 | Token 过期或认证头无效 | 在 Magpie 中更新凭据，开新会话验证只读接口 |
| `ssh` 无目标 | `~/.codex/ssh-profiles.json` | 补配置并确认从当前工作目录出发的目标主机 |
| 基线页不能生成 | Node.js 是否 20+ | 升级 Node.js LTS，再运行 `am.mjs` |
| 页面验收被登录或验证码拦住 | 目标环境、账号、验证码开关 | 报告阻塞；不要在未授权时破解验证码或改认证逻辑 |
| 页面验收通过但项目仍显示 `Dev Complete` | 验证结论是否落盘 | 更新 PRD/切片状态和 `docs/agents/verification.md` |
| `review` 被当成页面验收 | 当前阶段是否真的走过浏览器 | 回到 `page-acceptance`；代码审查不能替代渲染验证 |
| 推送后远端不一致 | 本地 `HEAD`、`origin/main`、远端引用 | 先 fetch 核对，不强制推送，不改写历史 |
| Codex 报 `Incomplete response returned, reason: max_output_tokens` | 见 §8.1 | 两种根因，先用 `output_tokens` 区分：≈4096 是输出上限未覆盖；很小且工具参数 JSON 不完整是模型退化 |

### 8.1 `Incomplete response returned, reason: max_output_tokens`（输出上限截断）

**不是上下文超限**。这是模型这一轮生成的**输出预算**（`max_tokens`）在写工具调用/长回答时用尽，上游返回 `finish_reason=length`，本地网关把响应标成 `status: incomplete / reason: max_output_tokens`，Codex 原样报出。该会话 `input_tokens` 往往远小于模型 `context_window`（例：2026-11-09 失败轮 `input_tokens=109901`，窗口 1048576），所以先排除“上下文太长”。

**证据怎么取（顺序）：**

1. 失败会话的 rollout：`~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl`
   - `event_msg` → `task_complete` 的 `error.message` 就是这句话；紧邻的 `function_call` 参数常在某一列被切断（`EOF while parsing a string`）。
   - 同轮 `token_usage_record`：确认 `input_tokens` 远小于 `context_window`（排除上下文问题）。
2. Magpie 应用日志：`~/AppData/Local/magpie/logs/app.log`
   - `gateway: …'s call to <group> on our-free-model failed: …`（含 499/502、`Upstream SSE ended without a completion marker` 等）。
3. Magpie 设置：`~/.config/magpie/settings.json` 的 `modelOutputs`（`magpie model output` 的落盘处），以及 `~/.config/magpie/our-free-model/settings.json` 的 `defaultMaxTokens`（本机为 `131072`）。

**机制（本地代码，非猜测）：**

- 组模型（如 `group/ds4.1-high`）在 `~/.config/magpie/providers.json` 定义为轮询/轮转组，成员是多个 `our-free-model/…deepseek-v4.1-flash`。
- 免费通道插件把 Responses 请求转成 Chat Completions，生成上限压成
  `max_tokens = min(模型容量, 关卡上限, 插件默认)`：见
  `~/.config/magpie/plugins/node_modules/magpie-our-free-model/vendor/ofm/src/effort.js` 的 `budgetFor()`（`capacity = Math.min(model.maxOutput, requested, fallback)`），
  以及 `adapter.js` 的 `ceiling = Math.min(entry.maxOutput, state.settings.defaultMaxTokens ?? 32768)`。
- 上游返回 `length` 时固定标成 incomplete：见 `vendor/ofm/src/forward.js`
  `incompleteDetails = outcome => outcome.truncated === true ? { reason: 'max_output_tokens' } : undefined`。
- 被输出上限切断的回合有一次自动续写：`vendor/ofm/src/recovery.js` 的 `continuationMessages()`（受 `our-free-model/settings.json` 的 `streamRecovery` 与 `defaultMaxTokens` 影响）。

**根因（两种，先用 `output_tokens` 区分）与修法：**

同一句话其实对应**两种不同**的截断，看失败轮的 `output_tokens` 就能分开（本项目 deja 索引中两种都出现过）：

1. **`output_tokens` ≈ 4096（大截断）** —— **该成员未上报自己的输出上限**。供应商没报 `max_tokens` 时 Magpie 按默认 **4096** 处理该模型；轮询落到这种成员时，长工具调用/长回答被切在 4096（`reasoning_output_tokens` 往往占满）。
   - 修法：用命令给**确实未上报上限**的成员设上限——`magpie model output <provider/model> 128k`（撤销用 `--reset`）。该命令写到 `~/.config/magpie/settings.json` 的 `modelOutputs`；手工编辑这一项也有效，但**不要写 `providers.json` 里的 `outputs`**，那里写的会被丢弃、无效。
   - **不要盲目给全组成员都设**：vendor 已自带上限的成员（`magpie model output` 已显示 `100k`/`128k` 的）无需覆盖。2026-11-06 实例：`loomy`、`qoder/dfmodel`、`qodercn/dfmodel`、`codearts` 未上报、被当 4096，已用命令设为 `128k`；`raccoon` 自带 `100k`、`buddy` 自带 `128k`，**无需覆盖**（本文件更早一版曾误写为“应补进 `modelOutputs`”，已更正）。
   - 先查哪些成员真的缺上限：`magpie model output <provider/model>`（显示 `what the vendor's list and models.dev say` 即 vendor 自带，显示 `what you said it answers with` 即你设过）。批量核对：`magpie model specs` 列出所有已设 spec 的模型。

2. **`output_tokens` 很小（几十到几百），且失败轮的工具调用 args 是坏 JSON** —— **模型自身退化，不是缺上限**。免费 DeepSeek 在写某个工具调用参数时播出了内部标记（`<|DSML|…>` 之类的控制串），随后 args 在字符串中途断掉，宿主报 `failed to parse function arguments: EOF while parsing a string`。这条 args 永远解析不了，被上游标记为“截断”后归成同一个 `max_output_tokens`。
   - 判据（三条同时成立即这种）：`output_tokens` 远小于 4096；`token_usage_record` 同轮 `function_call` 的 args 结尾是半截字符串（或含 `<|DSML|`）；紧邻的 `function_call_output` 是 `failed to parse function arguments: EOF while parsing a string`。
   - 这不是可配的上限，`magpie model output` 改不动。可行的缓解：直接重发该轮（多数情况下下一次采样不再吐出该标记）；或把会话临时切到同组里更稳的成员/付费模型。
   - 例：2026-11-09 `group/ds4.1-high` 两轮，`output_tokens` 分别 228、678，args 结尾 `"powershell</|DSML|: 4000}` / `--glob openai.yaml", "powershell</|DSML|: 4000}`，宿主均报 args 解析失败。

**快速命令（PowerShell）：**

```powershell
# 1) 最近失败原因
Get-ChildItem ~/.codex/sessions -Recurse -Filter rollout-*.jsonl |
  Sort-Object LastWriteTime -Descending | Select-Object -First 5 |
  ForEach-Object { Select-String -LiteralPath $_.FullName -Pattern 'Incomplete response returned' -List }

# 2) 当前组的成员
(Get-Content ~/.config/magpie/providers.json -Raw | ConvertFrom-Json).groups |
  Where-Object id -eq 'ds4.1-high' | Select-Object -ExpandProperty members

# 3) 已设上限的模型（同: settings.json 的 modelOutputs）
magpie model specs

# 4) 某个成员的上限：显示 vendor 自带 还是 你自己设的
magpie model output our-free-model/raccoon/sn-deepseek-v4-1-flash-1017
```

## 9. 已知缺口

这些是当前事实，不在本文里假装已经解决：

1. **全局规则只分发 Codex**：其他 Agent 需要单独确认是否能承载相同约束。
2. **逐 Agent 技能启用不统一**：多数流程技能只勾选 Codex；共享目录存在不等于所有 Agent 已启用。
3. **浏览器跨机器差异**：本机已安装 `agent-browser 0.41.2`；新机器仍需检查工具/会话可用性，不强制 CLI 替代宿主能力。
4. **MCP 未做全量连通测试**：只核对了配置和依赖，恢复后必须逐项做最小只读验证。
5. **`dbhub` 绑定本机 PostgreSQL**：换项目或换机器时目标可能变化，需要重新核对。
6. **`magpie-image` 绑定本机 Magpie 路径**：换机后路径和模型配置可能不同。
7. **版本没有锁定文件**：本文记录的是核对时版本；Magpie、Node、Python 和 CLI 升级后需要重新验证。
8. **仓库不是可执行安装包**：它只保存可读文本；恢复运行环境仍依赖 Magpie 备份或手工重配。

## 10. 最小验收清单

换机或重配完成后，至少确认：

- [ ] `magpie --version` 正常；
- [ ] `magpie library sync` 成功；
- [ ] `verify-library.py` 零错误；
- [ ] `~/.agents/skills` 有 16 项；
- [ ] Codex 新会话能读取全局规则；
- [ ] `setup-project`、`think`、`grill`、`story`、`implement`、`page-acceptance`、`review` 能被正确路由；
- [ ] 至少一个搜索 MCP 和一个代码托管 MCP 完成只读调用；
- [ ] 已记录目标项目真实构建命令；只有当前请求授权时运行受影响侧构建，否则记未验证；
- [ ] 页面验收有可用浏览器、账号和目标 URL；
- [ ] 未把任何密钥、DSN、认证头或登录态提交到 Git。
