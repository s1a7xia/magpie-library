# Magpie 当前环境、插件与记忆清单

核对日期：2026-11-19。本文件记录实际本机配置，不把“已登记”“已启用”当作“已连通/已生效”。用于公开溯源与换机配置，不是含凭据的全量运行备份。

## 总览

- Magpie：CLI 实测 `0.1.4395`。
- 技能清单以当前 Magpie 资源库和 [脱敏快照](config/environment.snapshot.json) 为准。`sharedSkills=false`、`mcpHub=true`、`skillRouter=true`；Magpie 资源库只剩 4 个本地技能，全部只分发给 Codex。`ruoyi6`、`database-design` 直接暴露，`frontend-design`、`answer-me-with-html` 进入 `magpie-skills` 聚合层。Matt Pocock 的 16 个简体中文技能由 Codex 插件 `mattpocock-skills-zh@magpie-mattpocock-zh` 提供，不再复制到 Magpie 或 `~/.codex/skills`。
- MCP 配置以当前 `library.json` 和脱敏快照为准；内置插件 13 个启用、budget 关闭。工具可见不等于获得写操作授权。
- Alma 已退出本资源库的团队与分发链：其 `USER.md` 为空，技能目录没有 Magpie Junction，`mcp.json` 为空。Alma 的聊天、记忆、通知、微信、Herdr 及其自身 bundled/personal 配置由 Alma 独立维护，不由本仓库管理。
- 自动备份：每 24 小时、保留 3 份、包含登录态；密码及备份文件不公开。没有执行备份或恢复演练，不能保证未核验的数据一定被整包覆盖。

## MCP：9 项资源库配置

| 服务 | 传输 | Agent | 用途 |
|---|---|---|---|
| context7 | http | codex | 库与框架文档 |
| dbx | stdio | codex | 数据库查询与获授权操作；目标按当前会话配置 |
| gitee | http | codex | Gitee 代码与 Issue/PR |
| github | http | codex | GitHub 代码与 Issue/PR |
| magpie-image | stdio | codex | 图片生成 |
| magpie-memory | stdio | codex | 结构化记忆 |
| magpie-vision | stdio | codex | 图像识别 |
| magpie-web-search | stdio | codex | 联网搜索 |
| ssh | stdio | codex | 已登记 SSH 目标操作 |

公开端点与无密钥启动命令见脱敏快照。dbx 连接参数、HTTP Authorization、SSH 主机/用户名/密码/密钥均不入库。`magpie-vision` 是独立识图入口，不能因为有 image 就漏记。`magpie mcp ...` 在本机使用已安装可执行文件，换机先确认 PATH 和生成配置。

当前 Magpie 资源库登记 9 项 MCP。`library.json` 中 `dbx`、`gitee`、`github`、`magpie-image`、`magpie-memory`、`magpie-vision`、`magpie-web-search`、`ssh` 仍带有 `alma` 分发勾选，但这只是残留配置；Alma 的 `mcp.json` 已清空，运行时没有连接这些开发 MCP。当前实际开发使用方是 Codex。Codex 宿主另有浏览器、computer-use、app-tools 等内置工具，它们不是资源库 MCP，换机时按 Codex 自身配置恢复。工具注册、MCP hub 状态、当前会话暴露和目标写入权限是四件事；本轮未做全部业务写入测试。

## 社区插件：2 个

| 插件 | 当前来源/版本 | 状态与作用 |
|---|---|---|
| magpie-our-free-model | `github:mu-zi-lee/magpie-our-free-model`，0.9.4 | CLI 显示 on；社区模型供应商入口。登录态不公开，不依赖其名称承诺长期免费或稳定 |
| @vshulcz/magpie-deja | 本地 `~/.config/magpie/local-plugins/magpie-deja`，package 版本 0.24.0 | CLI 显示 on，async gateway `onRequest` hook；按项目召回历史会话 |

## Codex 技能插件：1 个

| 插件 | 当前来源/版本 | 状态与作用 |
|---|---|---|
| `mattpocock-skills-zh` | 本地 marketplace `magpie-mattpocock-zh`，1.0.8；内容来自 [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) commit `d97aa0788b120c9363ebddfd47b87618d9314c3e` | Codex CLI 显示 `installed, enabled`；提供 16 个按用户选择裁剪并适配 Codex 执行与授权边界的简体中文工程技能 |

运行插件源是本机 Codex marketplace `magpie-mattpocock-zh`，公开只读镜像在 `plugins\mattpocock-skills-zh\`。安装缓存由 Codex 管理，不手工编辑；更新顺序是修改插件源、提升版本、先执行 `codex plugin remove "mattpocock-skills-zh@magpie-mattpocock-zh"`，再执行 `codex plugin add "mattpocock-skills-zh@magpie-mattpocock-zh"`，最后核对 `codex plugin list` 与缓存版本。

来源：[our-free-model](https://github.com/mu-zi-lee/magpie-our-free-model)、[deja-vu Magpie 扩展](https://github.com/vshulcz/deja-vu/tree/main/extensions/magpie)。本轮未比较 deja 本地插件和上游字节，不能保证直接 npm 安装就复现本机本地包。

恢复入口（需明确同意安装第三方代码；本轮没有运行）：

```powershell
magpie plugin add github:mu-zi-lee/magpie-our-free-model
magpie plugin add @vshulcz/magpie-deja
```

deja 当前显式参数：`requestTimeoutMs=800`、`maxBytes=4000`、`recallRemote=false`、`allowUnscoped=false`。本地包依赖 `@vshulcz/deja-vu ^0.24.0`。按插件本地 README，需建立会话索引才有召回；不能只安装插件就声称已恢复记忆。

**隐私边界**：deja 在本地检索，但召回片段会附加到请求并发送给当前上游模型。按项目作用域召回和两层脱敏不是“绝无泄漏”保证。保持禁止无项目召回、禁止远端召回，不擅自放宽。不要为核对而输出原始会话。

## 内置插件

CLI `magpie plugin builtin` 实测：

- 开：gateway、groups、library、middleware、otel、redact、rotation、routing、search、sessions、tools、usage、warmups。
- 关：budget。
- 本机 `plugins.yml` 使用 `preset: all`，budget 显式关闭。开关代表配置，不代表每项功能本轮都经过运行验证；otel 开启也不能据此推断遥测接收端和数据流。

这里的 Magpie gateway hook 不是工程提交/测试 Hook。工作流“默认不安装工程 Hook”不意味着本机没有 gateway 插件，两者不要混淆。

## 记忆：三层不要混为一谈

| 层 | 本机状态 | 正确用途 |
|---|---|---|
| 项目文档 | 项目 Git 内的规范、PRD、决定和验证记录 | 审批与业务事实源，随代码审阅 |
| Magpie 结构化记忆 | `~/.config/magpie/memory/`；当前 3 条 active 记忆，通过 magpie-memory 分发给 Codex | 可复用的背景与偏好，不替代当前源码和项目审批 |
| deja 历史召回 | 本地插件启用；存在用户数据目录 `~/AppData/Roaming/deja/`，本轮只查看文件名 | 从历史会话检索背景，不自动当现行指令或已完成证据 |

结构化记忆的权威运行源是本机 `~/.config/magpie/memory/`。公开仓库只镜像其中 3 条不含凭据、业务机密和机器路径、并已由用户确认可公开的工程偏好正文，位置是 `memory/*.md`；`index.json`、`meta.json` 中的索引、removed、used、written 运行状态不公开。公开镜像不是运行目录，覆盖它不会改变当前会话的记忆，权威运行记忆仍由 Magpie 备份维护。记忆正文属于用户提供的事实背景，不替代当前源码和项目审批，也不能被当作已执行或已验收的证据。Magpie `distill.json` 中 `on=true`、`dream=true`，但最近 distill 与 dream 错误字段均非空：因此只能说配置开启，不能说自动整理健康。错误正文未公开，本轮没有诊断/修复或触发蒸馏。

deja README 使用 `~/.deja` 举例，本机该目录不存在；Windows 数据落点不能硬编码为此例。存在目录/notes 文件也不证明索引完整或当前请求已注入召回。本轮未运行索引、召回或恢复演练。

## 其他配置需要怎么留档

| 类别 | 公共 GitHub 记录什么 | 私下恢复什么 |
|---|---|---|
| 模型供应商与路由 | 机制、所需 API 类型、使用方法；不承诺模型永久可用 | providers、profiles、groups、选择状态与供应商密钥 |
| 搜索/识图 | 所需服务和入口、是否登记 | 搜索 API key、模型与计费配置 |
| SSH / 数据库 | 依赖与只读核对方法 | 主机、账号、DSN、证书与密码 |
| Agent 插件 | 本文只清点 Magpie 的插件 | Codex 等宿主自带插件独立管理，缓存目录不是 Magpie 插件清单 |
| 会话/记忆 | 机制、路径类型、权限与已知健康状态 | 会话、结构化记忆、召回索引及相关授权 |
| 加密同步 | 使用 Magpie 支持的备份/同步机制 | 同步位置、密码、登录态与真实备份 |

不复制原始 settings/providers/plugins/library/sync/memory JSON 到公开库。`environment.snapshot.json` 是明确白名单字段提取：除 Magpie 的指令 Agent、本地技能和 MCP 元数据外，还包括 Codex 插件版本、16 个插件技能名和 3 条公开记忆的正文文件索引；不包含 MCP 认证头、插件运行缓存、记忆索引或机器路径。

## 恢复与后续维护

1. 按 [DEPENDENCIES.md](DEPENDENCIES.md) 安装 Magpie、必要 CLI，恢复授权的加密备份；备份包含范围以该版本帮助与恢复演练为准。
2. 用本仓库恢复规则与技能；按快照登记 MCP/插件/分发开关；凭据从私有安全渠道配置。
3. deja 的本地包/索引、Magpie 结构化记忆分别确认是否已恢复，不能假设 Magpie 备份覆盖第三方索引。
4. 执行必要的只读配置核对；实际连接、模型调用、索引/蒸馏、备份恢复等动作按当前授权进行。
5. 修改 MCP、插件、记忆机制或分发时，同时更新本文、脱敏快照和依赖说明，核对差异/敏感字段后按授权推送。

公共库保存“机制、使用与配置清单”；私有加密备份保存“可以恢复的运行状态”。二者一起才完整，不能用公开上传所有机器状态换取表面完整。
