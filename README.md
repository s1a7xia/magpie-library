# Magpie 工程组合拳（私有）

这是 Magpie 资源库里那套跨项目工程技能与通用协作指令的版本化副本。仓库私有，用于**溯源**：看清每个技能随时间的改动、diff 与回滚点。

跨机恢复**不依赖本仓库**——那由 Magpie 的同步负责（WebDAV/S3/GitHub 加密整包，含 providers、密钥、模型设置与本资源库）。本仓库解决的是「可读、可 diff、可回滚、可阅读」。

## 内容

| 路径 | 说明 |
|---|---|
| `instructions.md` | 通用协作指令（写入各 Agent `AGENTS.md` 的正文） |
| `skills/` | 21 个技能目录 |

技能分四组：

- **流程**：`engineering-workflow`、`think`、`grill`、`story`、`implement`、`debug`、`review`、`research`、`prompt-engineering`
- **质量**：`page-acceptance`、`frontend-design`、`rules`
- **工具与环境**：`agent-browser`、`powershell-windows`、`find-skills`、`answer-me-with-html`
- **项目与协作**：`setup-project`、`project-context`、`ai-collaboration`、`scm-collaboration`、`ruoyi-plus-dev`

## 唯一事实源

**技能与指令的编辑源是 Magpie 资源库，不是本仓库。**

- 源：`~/.config/magpie/library/`（Windows: `C:\Users\<user>\.config\magpie\library\`）
- 本仓库是该目录的镜像，供阅读与历史追溯

改技能的正确顺序：

1. 改资源库源文件；
2. 跑 `magpie library sync` 写入各 Agent；
3. 跑 `python skills/engineering-workflow/scripts/verify-library.py` 校验副本一致；
4. 把改动同步到本仓库并提交，提交信息写清改了什么、为什么。

直接在本仓库改、再指望它生效是不成立的：`magpie library sync` 会以资源库为准，覆盖本地的差异。

## 不含什么

本仓库只放技能与通用指令这类可公开阅读的文本。以下内容**永不入库**：

- API 密钥、令牌、认证头（在 `library.json` 与 Magpie 设置里，由同步加密托管）
- 登录态、订阅凭据
- 机器专属的同步配置与密码
- 运行时缓存、`__pycache__`、编辑产生的 `*.bak-*`

## 上手（新电脑）

1. 装 Magpie，用同一 WebDAV/S3/GitHub 同步地址 + password + passphrase 恢复整包（providers、密钥、模型、资源库一并回来）。
2. 需要阅读或追溯历史时，克隆本仓库：

   ```
   git clone git@github.com:s1a7xia/magpie-library.git
   ```

恢复后的 `~/.config/magpie/library/` 即权威源；本仓库用于对照与回溯。
