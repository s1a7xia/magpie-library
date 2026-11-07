# RuoYi-Vue-Plus 6.0 编码规范总则

适用于 RuoYi-Vue-Plus 6.0.0 后端与 plus-ui 6.0.0 前端。这里规定“代码应该怎么写”；具体接口、页面和数据库细节分别读 [api-contract.md](api-contract.md)、[backend.md](backend.md)、[backend-capabilities.md](backend-capabilities.md)、[frontend.md](frontend.md)、[frontend-components.md](frontend-components.md)、[database.md](database.md)。

## 1. 分层与职责

- 后端调用方向固定为 `Controller -> Service 接口 -> ServiceImpl -> Mapper`。Controller 不直接调用 Mapper；Service 不返回 `R<T>`。
- Entity 只表达持久化结构；BO 承载新增、修改和查询请求；VO 承载页面展示、翻译、脱敏和导出；跨模块 DTO 放在 `ruoyi-api`。
- 不新增独立 DAO 层。数据访问由 `ServiceImpl` 直接依赖 `BaseMapperPlus` 子接口完成。
- 前端按 `views -> hooks/components -> api -> utils/request` 组织。页面不直接调用 Axios 或 `fetch`，业务请求统一放 `api/`。
- 单模块业务规则留在所属模块；只有稳定、跨模块复用的技术能力才放到 `ruoyi-common-*`，跨模块契约放 `ruoyi-api`。

## 2. 命名

### 后端

| 类型 | 规则 | 示例 |
|---|---|---|
| Controller | `{业务}Controller` | `TestDemoController` |
| Service 接口 | `I{业务}Service` | `ITestDemoService` |
| Service 实现 | `{业务}ServiceImpl` | `TestDemoServiceImpl` |
| Mapper | `{业务}Mapper` | `TestDemoMapper` |
| Entity | `{业务}` | `TestDemo` |
| 请求对象 | `{业务}Bo` | `TestDemoBo` |
| 视图对象 | `{业务}Vo` | `TestDemoVo` |
| 跨模块 DTO | `{业务}DTO` | `UserDTO` |
| 权限字符 | `{module}:{business}:{action}` | `demo:demo:add` |

- Controller 方法沿用项目动作：`list`、`getInfo`、`add`、`edit`、`remove`、`export`、`importData`、`changeStatus`、`updateSort`。
- Service 方法沿用项目动作：`queryById`、`queryPageList`、`queryList`、`insertByBo`、`updateByBo`、`deleteWithValidByIds`。
- Java 包名全小写；类名大驼峰；方法和变量小驼峰；常量全大写下划线。
- 不另造 `I*Dao`、`*Manager`、`*Repository` 等平行数据访问层。

### 前端

| 类型 | 规则 | 示例 |
|---|---|---|
| 页面 | `views/<module>/<business>/index.vue` | `views/demo/demo/index.vue` |
| API | `api/<module>/<business>/{index.ts,types.ts}` | `api/demo/demo/index.ts` |
| 类型 | `VO` / `Form` / `Query` | `DemoVO`、`DemoForm`、`DemoQuery` |
| hook | `useXxx` | `useFormDialog` |
| store | `useXxxStore` | `useUserStore` |
| 组件 | 大驼峰文件与组件名 | `DictTag.vue`、`Pagination.vue` |

- API 函数使用动作前缀：`list`、`get`、`add`、`update`、`del`、`export`、`import`。
- CSS 类名使用小写连字符；变量和函数使用小驼峰；常量使用全大写下划线。
- 页面入口文件固定 `index.vue`，内部业务组件再使用大驼峰文件名。

## 3. 方法、对象与空值

- 一个方法只做一件事；Controller 只做参数接收、校验、权限和响应转换，业务判断放 Service。
- BO 校验用 `AddGroup`、`EditGroup` 分组；查询条件用 `QueryGroup` 时按项目现有写法处理。
- 集合可能为空时返回空集合，不返回 `null`；ID 集合为空时直接返回空结果，禁止生成无条件全表查询。
- 优先复用 `ObjectUtil`、`StringUtils`、`CollUtil`、`StreamUtils`、`MapstructUtils`，不要为同一行为再写工具类。
- 对象转换用 `MapstructUtils`，鉴权用 `LoginHelper`，统一响应用 `R<T>`，分页返回 `PageResult<T>`。
- 不在代码里散落字典值、权限字符、状态值和配置键；固定枚举放常量/字典，运行参数放 `sys_config`。

## 4. 校验、异常与日志

- Controller 使用 `@Validated`；新增/修改请求使用 `@Validated(AddGroup.class)` / `@Validated(EditGroup.class)`。非 Controller 层需要校验时使用 `ValidatorUtils`。
- 业务阻断抛 `ServiceException`，由全局异常处理统一转成 `R`；不要在每个 Controller 里手写错误响应。
- 不吞异常、不用空 `catch`、不把底层异常原文直接暴露给用户；需要补充上下文时保留 cause。
- 写操作按项目现有约定加 `@Log(title = "...", businessType = ...)`；日志不得记录密码、令牌、密钥、完整身份证件或不必要的个人信息。
- 对重复提交敏感的 POST/PUT 使用 `@RepeatSubmit`；不要给所有接口机械添加。

## 5. 事务与并发

- 单表单次写入不为了“规范”强行加事务。
- 多表写入、主从数据同步、需要原子性的读改写，在 Service 公共方法上使用 `@Transactional(rollbackFor = Exception.class)`。
- 事务注解必须落在 Spring 代理调用的公共方法上；同类自调用不会开启新事务。
- 事务内不调用长时间远程服务、不等待人工操作、不执行大批量无关计算。
- 唯一性优先由数据库唯一约束保证；并发更新使用 `@Version`、条件更新或现有锁，并检查受影响行数。
- 缓存更新与数据库写入的顺序、失效范围和失败补偿要明确；不能只删缓存或只写数据库。

## 6. 注释与文档

- Controller、Service 接口、Entity/BO/VO 字段、复杂业务方法和非直观 SQL 使用简洁 JavaDoc。
- 注释解释“为什么”和契约，不复述代码；字段注释与页面标签、字典名称、数据库注释保持同一业务术语。
- 前端 API 函数、复杂 hook、非直观组件生命周期写简短 JSDoc；模板中只保留解释结构的注释，不写无信息量的分隔线。
- `TODO` 必须说明待补条件和影响范围；不把未完成逻辑藏在 `TODO` 里却不报告。

## 7. 安全与数据完整性

- SQL 使用参数绑定或 Wrapper，不拼接用户输入；排序字段使用白名单或项目现有校验。
- 前端隐藏不等于权限控制；敏感字段在 VO/序列化出口脱敏，写操作在 Service 校验数据范围。
- 不把密钥、真实令牌、个人敏感信息写入代码、配置样例、日志、截图、提交或文档。
- 文件上传校验真实类型、大小和访问权限；导出复用列表查询的数据权限。
- 数据库变更、批量更新、删除和外部写入必须有明确授权和可恢复条件。

## 8. 交付检查

- [ ] 命名、包路径、文件位置与同模块邻近实现一致。
- [ ] Controller 没有业务编排，Service 没有返回 `R<T>`，没有新增 DAO 层。
- [ ] BO 分组校验、`ServiceException`、`@Log`、`@RepeatSubmit` 按需使用。
- [ ] 多表写操作有正确事务边界；唯一性和并发有数据库或条件更新保障。
- [ ] 空集合、空 ID、可空字段和逻辑删除行为明确。
- [ ] 鉴权、响应、转换使用本项目既有封装，无重复工具、硬编码配置或敏感信息。
- [ ] 后端映射改动已实际编译；前端已按项目脚本构建。页面可见改动仍按 `page-acceptance` 单独验收。

## 9. 编码顺序

1. 先读同模块现有实现，确认命名、包路径、请求封装和页面壳。
2. 定字段契约：表名、Java/TS 类型、查询方式、新增/编辑、列表、字典、权限。
3. 沿文件链一次写完，不留“稍后补”的接口、类型或权限。
4. 改映射就编译；改前端就构建；改 SQL 就核对方言和可执行性。
5. 输出复用证据和实际检查结果，不把计划、构建通过或页面未验收混成完成。
