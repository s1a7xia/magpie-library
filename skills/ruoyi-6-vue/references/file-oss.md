# 文件与 OSS 参考

只在任务涉及文件上传、下载、附件、图片/视频、OSS 存储或文件预览时加载。普通 CRUD 不加载。

## 6.0.0 源码事实

- 通用存储在 `ruoyi-common/ruoyi-common-oss`，核心入口是 `OssClient`、`OssFactory` 和 `OssClientConfig`；底层是 S3 兼容对象存储，不能假设所有环境都是本地磁盘。
- 系统侧文件记录和上传接口在 `ruoyi-modules/ruoyi-system` 的 `SysOssController`、`ISysOssService`，常见路径为 `/resource/oss/upload`、`/list`、`/download/{ossId}`、`/delete`。
- 业务表通常保存 `ossId`、URL 或业务附件关联，而不是直接复制二进制；先查 `sys_oss` 和现有附件字段。
- 现有上传响应同时返回 `url`、`fileName`、`ossId`；后续预览/下载/删除要优先使用稳定标识，不能只依赖可能变化的公开 URL。

## 实现边界

1. **先复用系统 OSS**：不要为单个业务模块另建文件表和上传接口；先核对现有 `sys_oss`、`SysOssService` 和前端上传组件。
2. **区分临时与正式文件**：上传成功不等于业务已引用；删除业务记录时明确附件是保留、软删还是清理，避免误删共享文件。
3. **权限和数据范围**：上传、下载、删除分别有权限字符；不要只用前端隐藏按钮。文件记录和对象路径也要按现有数据范围检查。
4. **类型和大小校验**：服务端校验真实类型、扩展名和大小，不能只信任前端 `accept`；下载时设置安全的响应头，避免把用户上传内容当同源 HTML 执行。
5. **访问策略**：公开 URL、预签名 URL 和鉴权下载是不同安全边界；按业务敏感度选择，不在日志或页面暴露长期凭证。
6. **不把本地路径当远程 URL**：本机开发上传可落本地存储，但项目记录和接口契约要能在目标部署环境工作。

## 页面验收

- 上传后能看到文件名/预览，刷新页面后附件仍能回显；下载内容与上传一致。
- 验证大小/类型拒绝、无权限下载和删除后的行为；测试文件要清理。
- 涉及图片裁剪、富文本或视频时，按真实渲染验证，不只看接口返回成功。

官方参考：[文件处理最佳实践](https://github.com/bkywksj/ruoyi-plus-uniapp-docs/blob/master/src/content/docs/practices/features/file-processing.md)。文件 API 和前端组件以目标源码为准。
