# 权限、数据范围与字段脱敏参考

只在任务涉及菜单/按钮权限、接口权限、数据范围、字段脱敏或后台任务身份时加载。普通 CRUD 也至少要遵守 `common.md` 的权限和归属检查；本文件用于更细的判断。

## 6.1.0 源码事实

- 接口权限：Controller 使用 `@SaCheckPermission`，权限字符与 `sys_menu` 和前端 `v-hasPermi`/`checkPermi` 对齐。
- 数据权限：`@DataPermission` 标注在 Mapper/方法上，通过 `DataPermissionHelper` 管理上下文；`DataPermissionHelper.ignore` 只在明确理由和最小范围内使用。
- 数据范围：`DataScopeType`、`SysUserMapper`、`SysRoleMapper`、`SysDeptMapper` 等已有实现可作参照；字段必须和 SQL 别名对齐。
- 字段敏感：沿用 `@Sensitive`、`SensitiveService`/现有脱敏实现，不在页面或导出中自行拼接明文。
- 多租户：`codex/p0-integration` **未启用**。`MybatisPlusConfig` 只装配数据权限、分页、乐观锁，没有 `TenantLineInnerInterceptor`、`TenantLineHandler` 或 `TenantHelper`；`ry_vue.sql`、`ry_ai.sql`、`ry_job.sql` 没有 `tenant_id`。业务表不自行新增租户字段。

## 检查顺序

1. **功能权限和数据权限分开**：能进入页面不代表能看全部数据；列表、详情、导出、批量操作和关联选择都要检查数据范围。
2. **写操作也受范围约束**：新增归属、修改/删除目标、跨部门转移不能只校验按钮权限；后台任务无登录态时显式确定身份和数据范围。
3. **字段权限在出口统一处理**：列表、详情、导出、消息和日志使用同一脱敏策略；不要只在前端隐藏字段。
4. **不引入租户维度**：不新增租户实体、租户表、租户管理页或 `tenant_id`；数据隔离按现有部门、用户和角色数据权限解决。

## 常见缺口

| 现象 | 处理 |
|---|---|
| 菜单有权限但接口 403 | 对齐 `sys_menu.perms`、前端 `v-hasPermi` 和 `@SaCheckPermission` |
| 列表按部门过滤，导出却是全量 | 导出复用同一查询和数据权限，不另写无范围 SQL |
| 后台任务能查到所有部门 | 明确任务身份，使用最小忽略范围并记录理由 |
| 外部文档要求加 `tenant_id` | 本地基线未启用多租户；不因文档示例修改业务表 |
| 前端隐藏了敏感字段，接口仍返回明文 | 在 VO/序列化出口统一脱敏，前端隐藏不算权限 |

## 验证

- 至少用两个角色验证菜单/按钮/接口权限，以及一个有数据范围差异的账号。
- 核对列表、详情、导出和写操作的可见范围一致。
- 记录角色、权限字符、数据范围和实际结果；不记录凭证、完整令牌或个人敏感信息。

官方参考：[权限控制](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/permission-control.md)、[数据权限](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/data-permission.md)、[字段权限](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/field-permission.md)。这些页面只借鉴思路；6.1.0 的类名、配置和权限链路以本地源码为准。
