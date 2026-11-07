# RuoYi-Vue-Plus 6.1.0 + Vue Common Baseline

适用于本地 `codex/p0-integration` 的 **RuoYi-Vue-Plus 6.1.0 后端 + plus-ui 6.1.0 前端**。技术事实以该分支源码为准；项目自己的 `AGENTS.md` 或 `docs/agents/coding-standards.md` 有更具体约定时，按更具体且不冲突的规则执行。本文件只保留跨后端、前端、数据库共用的流程、目录、复用入口和交付门禁。

## 1. 版本基线

| 层 | 本次核对到的事实 | 使用规则 |
|---|---|---|
| 后端 | `revision=6.1.0`，Java 21，Spring Boot 4.1.2，MyBatis-Plus 3.5.18 | 以 `codex/p0-integration` 的 `pom.xml` 和实际依赖为准 |
| 前端 | `plus-ui/package.json` 版本 6.1.0：Vue 3.5.44、Element Plus 2.14.7、Vite 8.3.5、pnpm 10.34.5 | 读取同分支 `plus-ui` 的锁文件和实际页面；不要把后端 revision 当成前端版本 |
| 文档参考 | `ruoyi-plus-uniapp-docs` 的 `practices/` 文档站，正文默认以 3.5.x 为主线 | 只借鉴章节组织和规范概念；6.1.0 的 API、类名和配置以本地源码为准 |

官方文档地图见 [docs-map.md](docs-map.md)。

## 2. 四步工作流

1. **探查底座与参考实现**：确认目标工程版本、模块、构建命令和前端位置；读取本次要修改的邻近实现。新增标准 CRUD 时读同模块的 Controller/Service/Mapper/Vue 页面和 demo，按现有分层直接手写完整代码。
2. **对齐数据与契约**：DDL、Entity、BO、VO、API、TypeScript 类型、字典值和页面标签逐项对齐。先判断能否复用组织、账号、角色、字典、参数、文件等框架能力。
3. **按最小范围实现**：只实现当前任务需要的接口和交互，不机械生成全套 CRUD，不为假想需求新增抽象、中间件或跨模块依赖。
4. **执行交付门禁**：修改 Entity/BO/VO 映射后必须执行目标工程的 Maven 编译，让 MapStruct 生成实现；前端按实际脚本构建或类型检查。可见页面是否可用、是否好看，必须另走渲染验收。

## 3. 防幻觉红线

- 严禁混入原版 RuoYi 语法：`SecurityUtils`、`@PreAuthorize`、`AjaxResult`、`TableDataInfo`、`BeanUtils.copyProperties`。
- 调用前读取接口、实现和必要调用点；不臆造类、方法、字段、权限字符、字典值或配置项。
- 修改已有功能时保留其 API、权限、校验、事务、缓存和交互契约；范围外的重构不做。
- 不把目录存在当成依赖已接入，不把示例路径当成目标工程事实，不把编译通过当成功能或页面验收通过。
- 项目规则、执行权限、提交与外部写入遵循当前 `AGENTS.md`；数据库执行、部署和远端写入不因连接已配置而自动获得授权。

## 4. 目标工程目录

以下为本地 6.1.0 的常见结构；以 `codex/p0-integration` 实际模块为准，不为每个业务功能新建 Maven 子模块。模块职责与跨模块调用边界见 [architecture.md](architecture.md)。

```text
ruoyi-admin/                    # 启动、应用依赖、环境配置
ruoyi-api/                      # 跨模块接口与 DTO
ruoyi-common/                   # core、mybatis、satoken、redis、web 等通用能力
ruoyi-modules/ruoyi-<module>/       # ruoyi-secops 是项目业务模块，不进入通用 skill
├─ controller/XxxController.java
├─ domain/Xxx.java
├─ domain/bo/XxxBo.java
├─ domain/vo/XxxVo.java
├─ mapper/XxxMapper.java
└─ service/{IXxxService.java,impl/XxxServiceImpl.java}
ruoyi-extend/                   # 独立扩展服务
script/sql/                     # MySQL、升级脚本及按方言分目录的脚本
```

`codex/p0-integration` 中前端位于同仓 `plus-ui/`：

```text
plus-ui/src/
├─ api/<module>/<business>/{index.ts,types.ts}
├─ views/<module>/<business>/index.vue
├─ components/ hooks/ utils/
└─ assets/styles/               # token、页面壳、搜索区、表格工具栏
```

新增模块时核对父 POM 聚合、依赖管理、主应用依赖和权限菜单。前端位置按项目实际结构读取，不要假设后端仓库里一定存在 `plus-ui/`。

## 5. Repository Reuse Check

在写任何公共操作、工具、Service 包装或前端 hook 之前，先证明目标工程没有可复用实现。实现和审查都执行这一步。

1. **先搜候选**：后端查 `ruoyi-common/ruoyi-common-core/src/main/java/org/dromara/common/core/` 下的 `utils/`（含子包）、`service/`、`constant/`、相关 common 模块和所属业务模块；前端查 `plus-ui/src/utils/`、`hooks/`、`components/`、现有 API 模块；数据库查现有表、字典、参数和菜单，不要先造同义结构。
2. **读实现与调用方**：核对方法签名、父类/委托方法、空值与重复键策略、排序、集合可变性、异常、时区、副作用、权限和事务语义。同名第三方类不能证明项目包装行为相同。
3. **按行为匹配复用**：现有方法满足需求就直接调用或组合业务规则；项目包装优先于底层库。改名、私有方法或一行转发不构成重复实现的理由。
4. **先记录缺口再加代码**：写下搜索路径/关键词和缺失的具体行为或依赖限制，只实现未覆盖部分。扩展共享工具必须兼容现有调用方；否则把最小实现留在所属模块。
5. **最后检查新增**：对照 diff 查 Service/Controller 中内嵌的重复逻辑。输出搜索范围、选中的 `path#method` 和调用方，或每个新增公共操作的必要理由。

### 后端常用候选

| 需要的能力 | 先查 |
|---|---|
| 集合映射、过滤、分组、连接、Map/Set 转换 | `utils/StreamUtils.java` 及调用方 |
| 树构建、多根、叶子、树路径 | `utils/TreeBuildUtils.java` 及调用方 |
| 字符串拆分/拼接/空值/命名转换 | `utils/StringUtils.java` 及其继承 API |
| 日期格式化、区间与校验 | `utils/DateUtils.java` |
| 对象转换、校验、脱敏 | `utils/MapstructUtils.java`、`ValidatorUtils.java`、`DesensitizedUtils.java` |
| 文件、IP、正则、反射、请求上下文 | 对应嵌套 `utils/` 包和实际实现 |
| 已有业务能力或跨模块契约 | 所属模块 `service/`、`ruoyi-api/`、core `service/` 与 `constant/` |

这些是搜索起点，不是可直接假设的 API 清单。比如集合转 Map 先看 `StreamUtils.toMap`/`toIdentityMap` 的重复键策略；多根树先看 `TreeBuildUtils.buildMultiRoot`/`buildTreeNodeMap` 及调用方。

### 前端常用候选

| 需要的能力 | 先查 |
|---|---|
| 请求、下载、错误提示 | `utils/request`、`plugins/modal` 及现有 API |
| 表格选择、加载态、查询重置/折叠 | `hooks/table`、`hooks/async`、`hooks/form` |
| 表单弹窗生命周期 | `hooks/dialog/useFormDialog` |
| 字典、权限、分页、树面板 | `components/DictTag`、`utils/dict` 的 `useDict`、`v-hasPermi`/`checkPermi`、`pagination`、`TreePanel` |
| 页面壳、搜索卡片、表格工具栏、主题 token | 先看 `assets/styles/tokens`、`components/_page-shell.scss`、`_search-panel.scss`、`_table-toolbar.scss` 和两三个兄弟页面 |

## 6. 邻近实现与 CRUD Fast Path

本项目没有代码生成器环节，也不执行「页面生成 → 下载 zip → 解压导入」。但 `ruoyi-gen` 的 FreeMarker 模板是 AI 可直接读取的完整 CRUD 结构清单，适合作为新增标准 CRUD 的起点；它不替代目标项目的真实实现，也不是交付步骤。

### 新增 CRUD 的最快路径

1. **先定字段契约**：列出表名、业务名、模块名、主键、每个字段的 Java/TS 类型、`query`/`insert`/`edit`/`list`、查询方式、字典、必填、状态、排序、树父级和权限前缀。契约不清时不要直接套模板。
2. **一次读齐骨架**：按需读 [后端模板入口](#后端模板)、[前端模板入口](#前端模板)，确认普通表还是树表，以及需要哪些条件分支。
3. **读一份最接近的真实实现**：同模块优先；没有同模块实现时读 `ruoyi-demo` 的 `TestDemo` / `TestTree` 和 `plus-ui` 的 `demo` / `system` 页面，校准当前分支的实际命名、hooks 和请求封装。
4. **AI 直接写目标文件**：按字段契约裁剪模板，不运行生成器、不生成中间 zip、不导入生成包。模板只提供结构和分支覆盖，最终代码服从目标模块现状。
5. **只做受影响一侧的编译/构建**；页面可见改动仍留到用户发起的页面验收。

模板适合补齐容易漏的分支；真实实现适合确认当前分支到底怎么接。两者冲突时，以真实源码为准。

### 字段契约检查表

模板按字段开关生成代码。字段契约至少写清：

| 字段 | 需要确认 |
|---|---|
| 标识 | 表名、模块名、业务名、类名、权限前缀 |
| 类型 | Java 类型、数据库类型、TypeScript 类型、是否大整数 |
| 查询 | 是否出现在查询区、查询方式（EQ/LIKE/BETWEEN 等） |
| 录入 | 是否出现在新增/编辑表单、校验分组、必填 |
| 列表 | 是否作为表格列、字典、状态、排序、树父级 |
| 能力 | 是否需要导出、状态切换、树结构、上传、翻译 |

字段契约不完整时，先补齐或按最接近的现有表推断并明确标注；不要在模板里“边写边猜”。

### 后端模板

目录：`ruoyi-modules/ruoyi-gen/src/main/resources/fm/`

| 模板 | 用途 |
|---|---|
| `java/domain.java.ftl` | Entity、`BaseEntity`、主键、逻辑删除、乐观锁、字段映射 |
| `java/bo.java.ftl` | BO、校验分组、必填、查询字段、日期范围参数 |
| `java/vo.java.ftl` | VO、Excel 注解、字典转换、翻译字段 |
| `java/mapper.java.ftl` | `BaseMapperPlus<Entity, Vo>` |
| `java/service.java.ftl` | Service 接口、分页/列表/增改删、状态、排序 |
| `java/serviceImpl.java.ftl` | 查询条件、唯一性、树维护、状态、排序、删除的完整实现分支 |
| `java/controller.java.ftl` | `R`、`PageResult`、`@SaCheckPermission`、`@Log`、`@RepeatSubmit` |
| `xml/mapper.xml.ftl` | 需要 XML 时的空壳 |
| `sql/mysql.sql.ftl` | 菜单、按钮权限 SQL；其他方言另有对应文件 |

只读本次需要的模板。普通单表 CRUD 不读树表分支，也不因为模板存在就实现导出、状态或排序。

### 前端模板

主目录：`ruoyi-modules/ruoyi-gen/src/main/resources/fm/vue/`

| 模板 | 用途 |
|---|---|
| `api.ts.ftl` | `AxiosPromise`、`request`、分页/树表返回、状态和排序接口 |
| `types.ts.ftl` | `VO` / `Form` / `Query`、主键宽度、树节点 `children` |
| `index.vue.ftl` | 普通 CRUD：搜索、表格、弹窗、字典、上传、状态、排序、导出 |
| `index-tree.vue.ftl` | 树表 CRUD：`row-key`、展开折叠、树父级选择 |

`plus-ui/gen/` 是另一份模板副本，不能默认与后端模板同步：`index.vue.ftl`、`types.ts.ftl` 当前一致，`api.ts.ftl`、`index-tree.vue.ftl` 存在差异。需要核对前端生成器实际输出时再比较，不要同时读两套全文。

| 用途 | 目标工程入口 |
|---|---|
| 标准后端分层 | `ruoyi-modules/ruoyi-demo/src/main/java/org/dromara/demo/`、`ruoyi-modules/ruoyi-system/` |
| 标准 Vue 页面与 API | `plus-ui/src/views/demo/`、`plus-ui/src/api/demo/`、`plus-ui/src/views/system/` |
| 框架公共能力 | `ruoyi-common/`、`plus-ui/src/{utils,hooks,components}/` |
| 跨模块契约 | `ruoyi-api/src/main/java/org/dromara/` |
| 前端请求、路由、状态与布局 | 见 [frontend-shell.md](frontend-shell.md) |

## 7. 交付检查

- [ ] 代码中无原版 RuoYi API，模块边界和包布局与邻近实现一致。
- [ ] 业务配置优先 `sys_config`，枚举优先 `sys_dict_*`，并附目标数据库配套 SQL。
- [ ] Controller 分页签名为 `(XxxBo, PageQuery)`，Service 返回 `PageResult<Vo>` 而非 `R<T>`，Controller 返回 `R<PageResult<Vo>>`。
- [ ] JSON 对象字段使用 `autoResultMap = true` + `JacksonTypeHandler`，Entity/BO/VO 类型同构；映射改动已编译。
- [ ] 无登录态任务不强行依赖 `LoginHelper`；后台身份、归属字段和数据范围已明确。
- [ ] 前端主键/关联 ID 使用 `string | number`，组件 `name` 与菜单路由 `name` 一致，权限和字典未绕过。
- [ ] 适用检查有命令和结果；可见页面未做真实渲染验收时，不能宣称页面完成或颜值达标。
