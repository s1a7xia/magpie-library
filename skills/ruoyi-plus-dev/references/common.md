# RuoYi-Vue-Plus Common Baseline

适用于 RuoYi-Vue-Plus 6.x。技术事实以目标工程源码为准；项目自己的 `AGENTS.md` 或 `docs/agents/coding-standards.md` 有更具体约定时，按更具体且不冲突的规则执行。本文件只保留跨后端、前端、数据库共用的流程、目录、复用入口和交付门禁。

## 1. 四步工作流

1. **探查底座与参考实现**：确认目标工程版本、模块、构建命令和前端位置；读取本次要修改的邻近实现。新增标准 CRUD 前先读生成器模板和 demo。
2. **对齐数据与契约**：DDL、Entity、BO、VO、API、TypeScript 类型、字典值和页面标签逐项对齐。先判断能否复用组织、账号、角色、字典、参数、文件等框架能力。
3. **按最小范围实现**：只实现当前任务需要的接口和交互，不机械生成全套 CRUD，不为假想需求新增抽象、中间件或跨模块依赖。
4. **执行交付门禁**：修改 Entity/BO/VO 映射后必须执行目标工程的 Maven 编译，让 MapStruct 生成实现；前端按实际脚本构建或类型检查。可见页面是否可用、是否好看，必须另走渲染验收。

## 2. 防幻觉红线

- 严禁混入原版 RuoYi 语法：`SecurityUtils`、`@PreAuthorize`、`AjaxResult`、`TableDataInfo`、`BeanUtils.copyProperties`。
- 调用前读取接口、实现和必要调用点；不臆造类、方法、字段、权限字符、字典值或配置项。
- 修改已有功能时保留其 API、权限、校验、事务、缓存和交互契约；范围外的重构不做。
- 不把目录存在当成依赖已接入，不把示例路径当成目标工程事实，不把编译通过当成功能或页面验收通过。
- 项目规则、执行权限、提交与外部写入遵循当前 `AGENTS.md`；数据库执行、部署和远端写入不因连接已配置而自动获得授权。

## 3. 目标工程目录

以下为 6.x 常见结构；以目标仓库实际模块为准，不为每个业务功能新建 Maven 子模块。

```text
ruoyi-admin/                    # 启动、应用依赖、环境配置
ruoyi-api/                      # 跨模块接口与 DTO
ruoyi-common/                   # core、mybatis、satoken、redis、web 等通用能力
ruoyi-modules/ruoyi-<module>/
├─ controller/XxxController.java
├─ domain/Xxx.java
├─ domain/bo/XxxBo.java
├─ domain/vo/XxxVo.java
├─ mapper/XxxMapper.java
└─ service/{IXxxService.java,impl/XxxServiceImpl.java}
ruoyi-extend/                   # 独立扩展服务
plus-ui/src/                    # 前端存在时
├─ api/<module>/<business>/{index.ts,types.ts}
├─ views/<module>/<business>/index.vue
├─ components/ hooks/ utils/
└─ assets/styles/               # 主题、token、页面壳样式
script/sql/                     # MySQL 及按方言分目录的脚本
```

新增模块时核对父 POM 聚合、依赖管理、主应用依赖和权限菜单。前端是独立仓库时，按项目实际位置读取，不要假设后端仓库里一定存在 `plus-ui/`。

## 4. Repository Reuse Check

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
| 字典、权限、分页、树面板 | `components/DictTag`、`useDict`、`v-hasPermi`/`checkPermi`、`pagination`、`TreePanel` |
| 页面壳、搜索卡片、表格工具栏、主题 token | 先看实际 `assets/styles` 和两三个兄弟页面 |

## 5. 模板与示例入口

生成器实际加载 classpath 下的 `fm/`；`plus-ui/gen/` 是前端参考模板。可以直接参考模板写代码，无需先运行生成器。

| 用途 | 目标工程入口 |
|---|---|
| Java 分层 | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/java/` |
| Vue API、类型、列表与树表 | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/vue/`、`plus-ui/gen/` |
| Mapper XML | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/xml/` |
| 配套 SQL | `ruoyi-modules/ruoyi-gen/src/main/resources/fm/sql/` |
| 模板选择与输出路径 | `ruoyi-modules/ruoyi-gen/src/main/java/org/dromara/gen/util/TemplateEngineUtils.java` |
| 标准后端示例 | `ruoyi-modules/ruoyi-demo/src/main/` |
| 标准 Vue 页面与 API | `plus-ui/src/views/demo/`、`plus-ui/src/api/demo/` |

## 6. 交付检查

- [ ] 代码中无原版 RuoYi API，模块边界和包布局与邻近实现一致。
- [ ] 业务配置优先 `sys_config`，枚举优先 `sys_dict_*`，并附目标数据库配套 SQL。
- [ ] Controller 分页签名为 `(XxxBo, PageQuery)`，Service 返回 `PageResult<Vo>` 而非 `R<T>`，Controller 返回 `R<PageResult<Vo>>`。
- [ ] JSON 对象字段使用 `autoResultMap = true` + `JacksonTypeHandler`，Entity/BO/VO 类型同构；映射改动已编译。
- [ ] 无登录态任务不强行依赖 `LoginHelper`；后台身份、归属字段和数据范围已明确。
- [ ] 前端主键/关联 ID 使用 `string | number`，组件 `name` 与菜单路由 `name` 一致，权限和字典未绕过。
- [ ] 适用检查有命令和结果；可见页面未做真实渲染验收时，不能宣称页面完成或颜值达标。
