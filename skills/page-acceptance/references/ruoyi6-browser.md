# RuoYi 6.x React 页面验收速查

这是 `page-acceptance` 的 RuoYi-Vue-Plus 6.x + React 补充，不替代主技能的分层判定。所有操作必须通过真实前端 UI；请求拦截器负责鉴权与加解密，禁止用 `curl`、Python、Node 脚本直接请求 API 来“证明功能”。

## 0. 运行环境

验收连接项目已登记、已经运行的开发环境，不负责构建或部署：

- 不为验收重复打包：不每个修复跑一遍 `mvn package`，不重建镜像，不为了看页面去部署。
- 启动方式以项目登记的命令为准，本地直接跑应用进程即可。本机当前验证过的后端启动方式是：

  ```powershell
  java -jar ruoyi-admin\target\ruoyi-admin.jar --spring.profiles.active=dev
  ```

  后端监听 `8080`。前端在 `plus-ui-React` 目录启动：

  ```powershell
  pnpm dev
  ```

  前端监听 `80`，请求代理到 `http://localhost:8080`。上述命令是当前项目的本地示例；换项目时以 `docs/agents/project-state.md` 的 `Compile and run` 为准。本地不建议把应用放进容器，代码和配置改起来不直接；Docker 留给部署形态的环境。
- 前端或后端不可达时记为 `blocked`，说明缺哪个服务，让用户启动或按项目登记命令启动一次，不擅自更换启动方式。
- 只改 React/TSX/CSS 用 HMR 或刷新页面；改 Java、后端配置或 Mapper 时由环境所有者为**已运行的开发进程**重载一次；只改 SQL 不重启。
- 一轮 review 的行为修复先合并完成，再重载一次并做一次修复点验收；禁止每个修复重启一次。
- 后端重启由环境所有者完成，不属于页面验收。验收过程不打包 jar、不起容器、不写进程管理包装脚本；需要重载时，请用户停止当前进程后用上面的 `java -jar` 命令重启一次。服务不可达就记 `blocked`。

## 1. 会话与登录态

优先复用已存在的 `agent-browser` 会话：

```powershell
agent-browser skills get core
agent-browser --session ruoyi get url
```

- 如果未打开或停在 `/login`，用项目实际前端地址打开。
- `snapshot -i` 只取可交互元素标号；不要抓完整 HTML/DOM。Ant Design 组件嵌套很深，全量 DOM 会迅速撑爆上下文。
- 用项目配置的测试账号登录；凭据从项目环境或用户输入读取，不写入技能、报告、提交或截图。
- 验证码开关的实际位置和默认值以当前后端配置为准；如果登录被验证码拦住，暂停并请开发者确认是否按项目约定关闭开关，不要尝试破解验证码。
- 登录成功后保存状态（路径按项目约定，例如 `.ruoyi-auth.json`），后续复用同一 `--session ruoyi`。

## 2. 快照刷新红线

以下动作发生后，旧的 `@e` 标号立即失效，必须重新执行 `agent-browser --session ruoyi snapshot -i`：

- 路由跳转；
- 打开或关闭 Ant Design `Modal` / `Drawer`；
- 展开或收起 `Select`、`TreeSelect`、`DatePicker`；
- 表格刷新、分页、搜索、重置；
- `Popconfirm`、`Modal.confirm` 等二次确认框出现或消失。

Ant Design 下拉/树选择/日期选择的操作顺序固定为：`click` 展开 → `snapshot -i` → `click` 具体选项。不要凭旧标号连续点击。

## 3. 首屏健康度

1. `snapshot -i` 确认搜索区、`ProTable`、分页和主要按钮已渲染。
2. `agent-browser --session ruoyi errors` 检查 React 渲染错误、未捕获异常和浏览器警告。
3. `agent-browser --session ruoyi network` 检查本次页面依赖的请求：401（未登录/令牌失效）、403（Sa-Token 权限字符不匹配）、500（后端 SQL/接口异常）。
4. 记录 URL、角色、路由、视口和实际看到的结果；不要只写“页面正常”。

## 4. 标准 CRUD 冒烟

按顺序执行，失败就停在该步定位，不跳步：

### Step 1 — Create

- 点击“新增” → 重新 `snapshot -i` 识别 `ModalForm` / `Modal` 内的表单项。
- 填写必填项，使用可检索的测试标识（例如 `AI_TEST_01`）。
- `Select` / `TreeSelect` / `DatePicker` 按“展开 → 快照 → 选项”操作。
- 点击“确定” → 检查 `errors` 和 `network` → 重新 `snapshot -i`，确认弹窗关闭且列表出现测试记录。

### Step 2 — Read

- 在搜索区输入 `AI_TEST_01` → 点击“搜索” → 重新 `snapshot -i`，确认表格过滤正确。
- 点击“重置” → 重新 `snapshot -i`，确认列表恢复。

### Step 3 — Update

- 在测试记录行点击“修改” → 重新 `snapshot -i`。
- 重点检查表单是否回显原值，而不是默认值或空值。
- 修改一个字段（例如 `AI_TEST_01_MODIFIED`）→ 确定 → 检查 `errors`/`network` → 重新快照确认列表已更新。

### Step 4 — Delete / cleanup

- 点击该行“删除” → 重新 `snapshot -i` 识别 `Popconfirm` 或 `Modal.confirm`。
- 点击确认 → 检查接口与提示 → 重新快照确认记录消失。
- 中途失败也要尽量清理测试数据；无法清理时在报告中明确留下什么。

## 5. 视觉与边界

视觉结论必须来自渲染截图，不来自源码：

- 窄视口下无意外横向滚动；
- 按钮文字不折行；
- 深色模式正文、次要文字、边框、禁用态可读；
- `.ant-modal`、`.ant-select-dropdown`、`.ant-picker-dropdown`、`.ant-tooltip`、`.ant-drawer` 无 z-index 遮挡；
- 空状态、加载态、无权限态至少检查一个与本次改动相关的边界。

RuoYi 业务页的视觉边界见 [前端规范和样式边界](../../ruoyi6/references/frontend.md#样式与设计)。

## 6. 失败闭环

出现错误提示、控制台报错、点击确定后弹窗不关闭或列表不刷新时：

1. 读取 `agent-browser --session ruoyi errors` 和 `network`。
2. 结合后端日志定位：字段名/类型不一致、MyBatis-Plus 映射、字典值缺失、Sa-Token 权限字符不匹配、校验分组、事务回滚。
3. 在授权范围内修根因，不通过放宽校验、吞异常或绕过权限让页面“看起来通过”。
4. `reload` 后从失败步骤重测；验证 → 修复 → 重测最多三轮，超限报告具体阻塞。

## 7. 记录

验收结果写入 `docs/agents/verification.md`，至少包含：日期、环境/URL、角色、路由、主路径、边界、控制台/网络结果、截图路径、测试数据清理情况、结论。通过只代表本次声明范围，不代表其他角色、其他页面或全量回归。
