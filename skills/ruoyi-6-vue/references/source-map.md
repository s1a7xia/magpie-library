# RuoYi-Vue-Plus 6.0 工程能力地图

本文件只回答一个问题：**要做一件事，先去哪里看实现。** 所有路径相对于工程根目录。路径存在只说明能力或示例在仓库中，不说明业务模块已经启用。

## 1. 工程入口

| 要确认的事 | 先读 |
|---|---|
| 版本、Java、依赖管理 | 根 `pom.xml`、`ruoyi-common/pom.xml` |
| 启动类、端口、profile | `ruoyi-admin/src/main/java/org/dromara/DromaraApplication.java`、`ruoyi-admin/src/main/resources/application*.yml` |
| 模块聚合、运行依赖 | 根 `pom.xml`、`ruoyi-admin/pom.xml`、业务模块 `pom.xml` |
| 跨模块接口和 DTO | `ruoyi-api/src/main/java/org/dromara/` |
| 数据库初始化与增量 | `script/sql/`（初始化）、`docs/sql/`（业务增量） |
| 前端版本、脚本、依赖 | `plus-ui/package.json`、`plus-ui/pnpm-lock.yaml` |
| 前端启动与路由 | `plus-ui/src/main.ts`、`plus-ui/src/permission.ts`、`plus-ui/src/router/` |
| 前端布局与壳层 | `plus-ui/src/layout/components/{AppMain,Navbar}.vue`、`layout/components/Sidebar/`、`layout/components/TagsView/` |
| 前端全局状态 | `plus-ui/src/store/modules/{user,permission,settings,dict}.ts` |
| 前端全局插件 | `plus-ui/src/plugins/{index,modal,cache}.ts` |
| 前端类型与自动声明 | `plus-ui/src/types/`、`plus-ui/vite/plugins/{components,auto-import}.ts` |

标准模块为：

```text
ruoyi-admin
ruoyi-api
ruoyi-common
ruoyi-common/ruoyi-common-core
ruoyi-common/ruoyi-common-mybatis
ruoyi-common/ruoyi-common-ai
ruoyi-common/ruoyi-common-elasticsearch
ruoyi-common/ruoyi-common-mcp
ruoyi-common/ruoyi-common-push
ruoyi-common/ruoyi-common-mail
ruoyi-common/ruoyi-common-sms
ruoyi-modules/ruoyi-ai
ruoyi-modules/ruoyi-demo
ruoyi-modules/ruoyi-gen
ruoyi-modules/ruoyi-job
ruoyi-modules/ruoyi-system
ruoyi-modules/ruoyi-workflow
ruoyi-extend/ruoyi-monitor-admin
ruoyi-extend/ruoyi-snailjob-server
ruoyi-extend/ruoyi-snailai-server
plus-ui
```

## 2. 新增或修改一个业务功能

### 后端

```text
ruoyi-modules/<module>/src/main/java/org/dromara/<domain>/
├─ controller/XxxController.java
├─ domain/Xxx.java
├─ domain/bo/XxxBo.java
├─ domain/vo/XxxVo.java
├─ mapper/XxxMapper.java
└─ service/{IXxxService.java,impl/XxxServiceImpl.java}
```

| 要写的东西 | 最接近的现有样例 |
|---|---|
| 单表 CRUD | `ruoyi-modules/ruoyi-demo/.../TestDemoController.java` 及同目录 Service/Mapper/Entity/BO/VO |
| 树表 CRUD | `ruoyi-modules/ruoyi-demo/.../TestTreeController.java` 及同目录实现 |
| 字典、参数、菜单、用户、角色、部门 | `ruoyi-modules/ruoyi-system/` |
| 导入导出 | `TestDemoController#importData/export`、`SysUserController`、`ruoyi-common-excel` |
| 文件上传下载 | `SysOssController`、`ISysOssService`、`ruoyi-common-oss` |
| 工作流 | `ruoyi-modules/ruoyi-workflow/`、`ruoyi-api/.../workflow/api/` |
| 调度任务 | `ruoyi-modules/ruoyi-job/`、`ruoyi-common-job` |
| AI/MCP | `ruoyi-modules/ruoyi-ai/`、`ruoyi-demo/.../McpDemo*.java`、`ruoyi-common-ai`、`ruoyi-common-mcp` |
| 搜索 | `ruoyi-demo/.../EsCrudController.java`、`esmapper/`、`ruoyi-common-elasticsearch` |

### 前端

```text
plus-ui/src/
├─ api/<module>/<business>/index.ts
├─ api/<module>/<business>/types.ts
└─ views/<module>/<business>/index.vue
```

| 要写的东西 | 最接近的现有样例 |
|---|---|
| 普通 CRUD 页 | `views/demo/demo/index.vue`、`api/demo/demo/` |
| 树表 CRUD 页 | `views/demo/tree/index.vue`、`api/demo/tree/` |
| 系统管理页 | `views/system/{user,role,dept,menu,dict,config,post,oss,client}/` |
| 字典标签 | `components/DictTag/index.vue`、`utils/dict.ts` |
| 分页 | `components/Pagination/index.vue` |
| 工具栏与列显隐 | `components/RightToolbar/index.vue` |
| 用户/角色选择 | `components/UserSelect/index.vue`、`components/RoleSelect/index.vue` |
| 左侧树面板 | `components/TreePanel/index.vue` |
| 文件/图片上传与预览 | `components/FileUpload/index.vue`、`components/ImageUpload/index.vue`、`components/ImagePreview/index.vue` |
| 富文本 | `components/Editor/index.vue`、`utils/ossContent.ts` |
| 图标选择 | `components/IconSelect/index.vue` |
| 请求、错误、下载 | `utils/request.ts`、`plugins/download.ts` |
| 权限指令 | `directive/permission/index.ts`、`utils/permission.ts` |
| 页面壳和主题 | `assets/styles/tokens/`、`assets/styles/components/` |

## 3. 公共能力入口

| 能力 | 模块 | 入口 |
|---|---|---|
| 响应、分页、异常、校验、XSS、工具 | `ruoyi-common-core` | `R`、`PageResult`、`ServiceException`、`AddGroup`、`EditGroup`、`QueryGroup`、`Xss`、`MapstructUtils`、`StringUtils`、`StreamUtils`、`TreeBuildUtils`、`ValidatorUtils` |
| Web、全局异常、验证码 | `ruoyi-common-web` | `BaseController`、`GlobalExceptionHandler`、`ResponseEnhancementAdvice` |
| MyBatis-Plus、分页、数据权限 | `ruoyi-common-mybatis` | `BaseEntity`、`BaseMapperPlus`、`PageQuery`、`QueryBuilder`、`@DataPermission`、`DataPermissionHelper` |
| 登录态与权限 | `ruoyi-common-satoken`、`ruoyi-common-security` | `LoginHelper`、`SaTokenConfig`、`SecurityConfig` |
| 缓存、锁、限流、幂等 | `ruoyi-common-redis` | `CacheUtils`、`RedisUtils`、`@RepeatSubmit`、`@RateLimiter`、`@Lock4j` |
| 操作日志 | `ruoyi-common-log` | `@Log`、`BusinessType` |
| Excel | `ruoyi-common-excel` | `ExcelBuilder`、`ExcelResult`、Fesod 注解、转换器 |
| 文件存储 | `ruoyi-common-oss` | `OssClient`、`OssFactory`、`sys_oss`、`SysOssController` |
| 翻译与脱敏 | `ruoyi-common-translation`、`ruoyi-common-sensitive` | `@Translation`、`@Sensitive` |
| 加解密 | `ruoyi-common-encrypt` | `@ApiEncrypt`、`@EncryptField`、`CryptoFilter`、`EncryptUtils` |
| 消息推送 | `ruoyi-common-push` | `PushHelper`、`PushDTO`、SSE/WebSocket 会话管理 |
| 邮件/短信 | `ruoyi-common-mail`、`ruoyi-common-sms` | `MailBuilder`、SMS4J 配置与工厂 |

## 4. CRUD 结构模板

模板只用于查漏补缺，不是生成步骤。项目没有“页面生成器 → 下载 zip → 导入工程”的操作流程；CRUD 由 AI 读取真实邻近实现后直接写目标文件。

```text
ruoyi-modules/ruoyi-gen/src/main/resources/fm/
├─ java/{domain,bo,vo,mapper,service,serviceImpl,controller}.java.ftl
├─ vue/{api.ts,types.ts,index.vue,index-tree.vue}.ftl
├─ xml/mapper.xml.ftl
└─ sql/{mysql,postgres,oracle,sqlserver}.sql.ftl
```

用途：

| 模板 | 只用来检查 |
|---|---|
| `java/domain.java.ftl` | Entity 继承、主键、逻辑删除、乐观锁、字段映射 |
| `java/bo.java.ftl` | 查询/新增/编辑字段、分组校验、日期范围参数 |
| `java/vo.java.ftl` | Excel、翻译、展示字段 |
| `java/controller.java.ftl` | URL、权限、分组、普通表/树表列表签名、导出 |
| `java/serviceImpl.java.ftl` | `buildQueryWrapper`、唯一性、状态、排序、树维护、删除 |
| `vue/api.ts.ftl`、`vue/types.ts.ftl` | 请求函数、`AxiosPromise`、`PageResult`、VO/Form/Query |
| `vue/index.vue.ftl` | 搜索、工具栏、表格、分页、弹窗、权限、字典 |
| `vue/index-tree.vue.ftl` | `row-key`、`tree-props`、父级选择、展开折叠 |
| `sql/*.sql.ftl` | 菜单和按钮权限 SQL 的字段清单 |

读取顺序：先生成本次字段契约，再读对应模板，再读一份最接近的现有实现；三者冲突时以现有实现为准。

## 5. 数据库

```text
script/sql/
├─ ry_vue.sql、ry_job.sql、ry_workflow.sql、ry_ai.sql
├─ postgres/
├─ oracle/
└─ sqlserver/
docs/sql/                       # 业务增量脚本
```

数据库方言以项目实际配置和现有脚本为准。新增表或字段时同步更新对应初始化或增量脚本，不默认 MySQL，也不自行发明新的脚本目录结构。

## 6. 查找顺序

1. 先读本次要改的目标文件和同模块兄弟实现。
2. 再读本地图指向的框架公共入口。
3. 涉及 CRUD 时读一份 demo 和对应模板分支。
4. 涉及数据库时读现有 DDL、增量脚本、字典和菜单 SQL。
5. 涉及前端交互时读现有组件、hooks、工具和两三个兄弟页面。
6. 只有以上仍不能回答时，才查框架官方文档；结论不能覆盖工程现有实现。
