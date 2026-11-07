# RuoYi-Vue-Plus 6.0 API 契约

本文件规定 RuoYi-Vue-Plus 6.0.0 后端接口与 plus-ui 6.0.0 前端请求层的契约。

## 1. URL 与方法

标准业务路径为 `/{module}/{business}`，权限字符为 `{module}:{business}:{action}`。

| 动作 | 方法与路径 | 入参 | 返回 |
|---|---|---|---|
| 分页列表 | `GET /{module}/{business}/list` | BO + `PageQuery` | `R<PageResult<Vo>>` |
| 详情 | `GET /{module}/{business}/{id}` | 路径主键 | `R<Vo>` |
| 新增 | `POST /{module}/{business}` | `@RequestBody Bo` | `R<Void>` |
| 修改 | `PUT /{module}/{business}` | `@RequestBody Bo`，BO 带主键 | `R<Void>` |
| 删除 | `DELETE /{module}/{business}/{ids}` | 路径主键数组/逗号串 | `R<Void>` |
| 导出 | `POST /{module}/{business}/export`；树表使用 `GET` | 查询 BO | 文件流 |
| 导入 | `POST /{module}/{business}/importData` | multipart 文件 | `R<Void>` |
| 状态 | `PUT /{module}/{business}/changeStatus` | 含主键和状态的 BO | `R<Void>` |
| 排序 | `PUT /{module}/{business}/updateSort` | 含主键和排序值的 BO | `R<Void>` |

- 修改使用 `PUT /{module}/{business}`，主键放在 BO。
- 普通表和树表的导出方法可能不同，按同模块既有接口实现，不机械统一。
- 删除使用 `@DeleteMapping("/{ids}")` 和 `@PathVariable Long[] ids`；不要新增 `/delete` 之类的动作路径。
- 查询参数走 query string，新增/修改走 JSON body；导入和上传使用 `multipart/form-data`。
- 状态使用 `PUT /{module}/{business}/changeStatus`，排序使用 `PUT /{module}/{business}/updateSort`。

## 2. 统一响应

- 普通响应统一 `R<T>`，序列化结构为 `{ code, msg, data }`。
- 成功使用 `R.ok(data)` 或 `R.ok()`；新增、修改、删除使用 `toAjax(serviceMethod(...))`，由基类把布尔结果转成统一响应。
- 业务失败抛 `ServiceException`，由全局异常处理输出；不要在 Controller 里手工拼 `ResponseEntity` 表达业务错误。
- 分页响应使用 `PageResult<T>`，字段是 `total` 和 `rows`，不是 `records`。Service 返回 `PageResult<Vo>`，Controller 再包 `R`。
- 树表列表通常直接返回 `R<List<Vo>>`，前端读取 `res.data` 数组。
- 文件导出直接写 `HttpServletResponse`，不要包成 `R<byte[]>`。

## 3. 参数和校验

- 查询对象与 `PageQuery` 分开接收：`list(@Validated(QueryGroup.class) XxxBo bo, PageQuery pageQuery)`。
- 新增使用 `@Validated(AddGroup.class)`，修改使用 `@Validated(EditGroup.class)`；主键在编辑分组必填。
- 路径 ID、批量 ID 使用 `@NotNull` / `@NotEmpty`，空集合在 Service 先返回空结果。
- 日期范围字段使用项目现有查询参数约定（如 `params` 中的 begin/end），不要在 Controller 自造另一套日期格式。
- 分页只允许数据库分页；Controller 不拉全量再截取。

## 4. 权限、数据范围与幂等

- 每个接口使用 `@SaCheckPermission("{module}:{business}:{action}")`；权限字符必须与 `sys_menu.perms` 和前端 `v-hasPermi`/`checkPermi` 一致。
- 功能权限不等于数据权限；列表、详情、导出、批量操作和关联选择都要遵守 `@DataPermission` / `DataScopeType`。
- 新增/修改默认加 `@Log`；有重复提交风险的 POST/PUT 按需加 `@RepeatSubmit`。
- 状态切换、排序、批量删除等写操作要校验目标数据范围和业务状态，不能只看按钮权限。

## 5. 加密条件

传输加密不是全站默认行为。前端请求层只有在以下条件同时满足时才加密请求体：

```text
VITE_APP_ENCRYPT === 'true'
且请求头 isEncrypt === 'true'
且 HTTP 方法为 POST 或 PUT
```

后端 `api-decrypt.enabled=true` 只表示启用解密过滤器；接口是否强制加密还取决于加密头和实际注解。`@ApiEncrypt` 的响应加密按注解配置生效。不要写成“所有接口默认 RSA+AES”，也不要用脚本绕过前端请求链直接测试加密接口。

## 6. 前端请求契约

- API 统一从 `@/utils/request` 导入 `request`，返回类型使用 `AxiosPromise<T>`。
- 分页返回 `PageResult<T>`；页面读取 `res.data.rows` 和 `res.data.total`。
- 查询参数使用 `params`，请求体使用 `data`，下载复用 `download` 或现有下载方法。
- API 函数只负责 URL、method、参数和返回类型；业务编排留在页面或 hook。
- `VO`、`Form`、`Query` 分开；主键和外部关联 ID 使用 `string | number`，避免雪花 ID 在前端被 number 精度截断。
- 不使用 `any` 掩盖字段不一致；前后端字段名、日期格式、字典值和可空性逐项对齐。

## 7. 契约变更检查

- [ ] URL、method、权限字符与现有 Controller、菜单 `perms`、前端 API 一致。
- [ ] `R<T>` / `PageResult<T>` 的泛型和字段没有混用。
- [ ] 新增/修改的 BO 分组和前端表单校验一致。
- [ ] 删除、导出、批量操作遵守同一数据范围。
- [ ] 加密接口满足前端环境、请求头和方法条件。
- [ ] 前端读取 `res.data.rows/total`，树表读取数组。
- [ ] 接口契约改动已同步类型、页面调用和验收标准。

## 8. 工程内参考实现

| 场景 | 后端入口 | 前端入口 |
|---|---|---|
| 普通分页 CRUD | `TestDemoController` + `ITestDemoService` + `TestDemoServiceImpl` | `api/demo/demo/` + `views/demo/demo/index.vue` |
| 树表列表 CRUD | `TestTreeController` + `ITestTreeService` + `TestTreeServiceImpl` | `api/demo/tree/` + `views/demo/tree/index.vue` |
| 系统管理 | `ruoyi-modules/ruoyi-system` | `views/system/` |

新增接口沿用所属模块已有的结构、命名、权限字符和字段约定。
