# Excel 导入导出参考

只在任务涉及 Excel 导入、导出、模板下载、字典/枚举转换或大批量文件处理时加载。普通 CRUD 不加载。

## 6.0.0 源码事实

- Excel 统一能力在 `ruoyi-common/ruoyi-common-excel`，基于 Fesod；业务 Controller 通常通过 `org.dromara.common.excel.utils.ExcelBuilder` 调用，不直接依赖底层写表 API。
- 典型入口：`ExcelBuilder.of(list, ExportVo.class).sheetName(...).toResponse(response)`、`ExcelBuilder.read(inputStream, ImportVo.class)`、`ExcelBuilder.of(new ArrayList<>(), ImportVo.class)` 生成模板。
- 现有系统模块可参照 `SysUserController` 的 `/export`、`/importData`、`/importTemplate`，以及 `SysUserImportListener` 的导入结果处理。
- 字典、枚举、大数值、合并、下拉和分页导出的实现都在 common-excel 及业务相邻实现中；先读目标版本真实代码，不按文档站 3.5.x 示例直接复制。

## 实现边界

1. **导入导出专用 VO**：不要把 Entity、BO 或页面 Form 直接当 Excel 模型；导出字段、导入字段和展示字段可以不同。
2. **列表与导出同源**：导出查询条件、数据权限和列表一致；不能因为导出绕开权限或分页边界。
3. **字典和枚举对齐**：使用现有 `ExcelDictConvert` / `ExcelEnumConvert` 或项目约定的注解；写回数据库的仍是 `dict_value`，不是中文标签。
4. **大数值保精度**：雪花 ID 等大整数在 Excel 和前端都可能丢精度；按现有 `ExcelBigNumberConvert` 或字符串导出策略处理。
5. **导入要有结果**：复用 `ExcelResult`/`DefaultExcelListener` 的失败行、错误信息和更新策略；不要让部分成功静默变成全成功。
6. **大批量不硬扛内存**：优先分页导出、多 Sheet、ZIP 或现有异步方案；导出上限、超时和失败提示要明确。
7. **文件流安全**：文件名编码、Content-Type、下载响应头和临时文件清理沿用现有实现；不把上传文件落成可公开访问的路径。

## 页面验收

- 先看导出按钮是否按权限显示，再实际下载并用表格软件打开；核对表头、字典值、日期、数字精度和行数。
- 导入至少覆盖成功行、校验失败行和模板下载；确认失败提示可理解，测试数据能清理。
- 大批量/异步导出若本次改动涉及，至少验证任务状态、完成通知和下载文件；不在无人值守阶段打开浏览器。

官方参考：[Excel 操作最佳实践](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/excel-operations.md)。文档版本可能落后于 6.0.0，API 以源码为准。
