# 通用资源库全量真实验证记录（2026-11-06）

> **历史档案。** 本文验证的是 2026-11-06 当时包含 Hooks 与子代理的配置；这些组件已当日晚些时候从资源库移除，故其中的角色与 Hook 结论不再适用于当前配置。仍需参考的是 MCP、插件、模型路由、外部限制等项目级结论。

目标：不只验证“核心闭环”，而是把资源库里的指令、技能、子代理、Hook、MCP、插件、模型组在真实项目和真实会话中逐项跑一遍，暴露缺口并修复，形成一份可交付的稳定基线结论。

## 结论

资源库的**全部组件类别**都已在本轮取得实测证据：当时的 6 个 MCP、4 个子代理、3 个 Hook、3 个插件、意图分类器与模型路由、真实 RuoYi-Vue-Plus 仓库上的实现→测试→审查→文档→提交→推送闭环。

> 后续变更（2026-11-06）：Exa 曾因匿名额度耗尽从资源库移除；用户提供自有 API key 后已恢复 Exa MCP，并实测读取 MyBatis-Plus 官方网页成功。当时联网搜索统一走 Exa，Magpie 原生搜索 provider 当日清空；当时资源库为 6 个 MCP。本文中的首次匿名额度故障仍作为历史证据保留。

> 后续变更（2026-11-07）：Exa MCP 已从资源库卸载，联网搜索改由 `magpie-web-search` MCP（`web_search` / `web_fetch`）统一提供，并同时分发给 Codex 与 dsh。当前资源库为 8 个 MCP：chrome-devtools、context7、dbhub、gitee、github、magpie-image、magpie-web-search、ssh。注意 Exa 仅卸载了 MCP，其搜索 API 仍保留在 Magpie「设置 → 联网搜索」的 provider 列表（Tavily → Exa → You，`searchAll` 开启）。上文 2026-11-06 的“统一走 Exa、原生 provider 已清空”结论已被本次变更取代，首次匿名额度故障仍作为历史证据保留。

同时暴露并处理了 4 个真实问题：

1. **SSH MCP 配置指向目录而非文件**（本轮修复，见下）。
2. **research-scout 无输出上限导致首次调用 `max_output_tokens` 失败**（本轮修复，见下）。
3. **Exa 免费 MCP 命中速率上限**：返回 `You've hit Exa's free MCP rate limit`。这是账号额度问题，不是路由故障；需要自有 Exa API key 才能解除。后续处理：2026-11-06 曾将该 MCP 移除后以自有 key 恢复，2026-11-07 已卸载 Exa MCP，搜索改由 magpie-web-search 统一提供（见文首“后续变更 2026-11-07”）。
4. **GitHub fork `s1a7xia/RuoYi-Vue-Plus` 禁用了 Issues**：`issue_write` 返回 `410 Issues has been disabled in this repository`。写入链路本身已通（请求到达 API 并返回业务错误），但 issue 驱动开发在该仓库不可用，需在仓库设置中启用 Issues，或换用启用了 Issues 的仓库。

项目环境侧另有 1 个非资源库问题：本机 8080 端口由用户真实业务后端 `D:\FDE\RuoYi-Vue-Plus` 的 jar 占用，TCP 在监听但 HTTP 完全不响应（`/actuator/health` 6s 超时）。该服务属用户业务进程，本轮只诊断、未重启，因此 `page-checker` 对后端接口的完整验证受此阻塞。

## MCP 逐项实测（本会话真实调用）

| MCP | 调用 | 结果 |
|---|---|---|
| exa | `web_search_exa` | 返回官方文档结果（dromara/plus-doc、RuoYi-Vue-Plus 仓库页）；随后命中免费额度上限 |
| github | `get_me` / `get_file_contents` / `search_issues` / `issue_write` / `list_issues` | 读通过（账号 `s1a7xia`）；`issue_write` 到达 API 但仓库 Issues 被禁用（410） |
| context7 | `resolve_library_id` + `query_docs` | 查到 MyBatis-Plus 官方分页文档，`/websites/baomidou` 命中 High 信誉 |
| dbhub | `execute_sql` | 连到项目真实 PostgreSQL，`information_schema.tables` 返回 152 表 |
| ssh | `ssh_monitor list` + `ssh_snapshot` + `ssh_audit_baseline` | 读到 `codex-ubuntu`，快照 26 容器/33 端口，审计发现 PermitRootLogin/Password 等红线 |
| chrome-devtools | `list_pages` + 截图 | 读到运行中的 `http://127.0.0.1:5173/login` 页面 |

## 子代理逐项实测

| 角色 | 实测内容 | 结果 |
|---|---|---|
| `change-reviewer` | 审查 `ruoyi-p0` 的 `9227f62..7757575` | 未发现可证实问题，正确判断 null 处理与断言有效 |
| `page-checker` | 真实页面快检 `127.0.0.1:5173` | 登录页表单渲染成功；接口失败定位为后端不可用，结论准确 |
| `research-scout` | RuoYi-Vue-Plus 6.X 是否支持 PostgreSQL；分页 DbType 配法 | 修复输出上限后返回 400 字内紧凑证据包，不再超限 |
| `delivery-closer` | 隔离仓库 `feature/add-multiply` 完整收尾 | 正确核对暂存基线、只暂存任务路径、按事实增量写文档、未编造测试通过、正确报告“已提交，未推送” |

## Hook 逐项实测（隔离 Git 仓库）

- `SessionStart`：注入会话上下文 JSON，exit 0。
- `UserPromptSubmit`：写入本轮 Git 基线状态文件。
- `Stop`：改动工程文件但未同步运行态记录时，输出 `{"decision":"block","reason":...}` 中文提醒；文档同步并提交后再次触发保持静默。

## 修复记录

### 1. SSH MCP profiles 文件

- 症状：`ssh_monitor` 报 `EISDIR: illegal operation on a directory, read`。
- 根因：`library.json` 的 `env.SSH_PROFILES_FILE` 指向 `~/.ssh`（目录），而 `@hypnosis/ssh-mcp-server` 需要 JSON profiles 文件。
- 处理：新建 `C:\Users\s1a71\.codex\ssh-profiles.json`（profile `codex-ubuntu`），并把配置改指该文件，`magpie library sync` 后实测通过。
- 备份：`library.json.bak-before-ssh-fix`。

### 2. research-scout 输出上限

- 症状：首次委派返回 `errored: Incomplete response returned, reason: max_output_tokens`。
- 根因：角色提示词只规定“输出证据包”，未限制长度，长证据链超出模型输出上限。
- 处理：在角色提示词末尾加入硬上限——“正文总计不超过 400 字；先一句话结论，再证据列表，最后不确定项”。
- 备份：`library.json.bak-before-scoutfix`。
- 复验：再次委派同类调研，返回 400 字内结构化结果，`completed`。

## 未解决/待外部条件

- Exa 匿名额度耗尽：后续已用用户自有 API key 恢复；Exa MCP 已于 2026-11-07 卸载，现由 magpie-web-search 提供搜索与抓取，需按当前会话实际调用复验。
- GitHub fork Issues：需在仓库设置启用 Issues，或改用启用了 Issues 的仓库做 issue 驱动开发验证。
- GitLab/Gitee：仍只有统一工作流语义，未接入远程 MCP/CLI。
- 通知插件：配置与加载已确认，未发送真实 Telegram 测试消息（避免打扰）。
- 8080 后端：属用户业务进程无响应，未重启，`page-checker` 的接口层完整验证因此未完成。

## 维护命令

```powershell
magpie library sync
python C:\Users\s1a71\.config\magpie\library\skills\engineering-workflow\scripts\verify-library.py
```

正常结果 `0 errors`；`delivery-closer is self-managed` 为预期警告。
