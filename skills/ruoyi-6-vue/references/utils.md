# 工具类选型

## 目标

写业务时，先确认项目已有工具能否准确表达当前语义；能复用就复用，不原样重写字符串、集合、转换、JSON、日期、树、校验、文件、IP 或 SQL 处理。

这里不是完整 API 手册，也不把外部文档的方法名当成事实。使用前读当前 checkout 的类和方法，确认重载、空值、异常和返回类型。

## 选择顺序

1. **项目自己的工具类**：`ruoyi-common-core`、`ruoyi-common-json` 及所属公共模块。
2. **工具类继承或委托的底层能力**：例如 `StringUtils` 继承 Commons Lang3、`DateUtils` 继承 Hutool `DateUtil`。
3. **标准库或既有依赖**：确实没有被项目封装、且语义清楚时使用。
4. **业务内私有方法**：只服务当前业务、语义与公共工具不一致时使用。

只有稳定、跨模块、无业务归属的能力才考虑提升为公共工具；不要因为“以后可能复用”就新增一层。

## 高频入口

| 场景 | 优先入口 | 典型用途 |
|---|---|---|
| 字符串判空、截取、格式化 | `org.dromara.common.core.utils.StringUtils` | `isBlank`、`isNotBlank`、`trim`、`substring`、`format("{}")` |
| 字符串拆分、拼接、命名转换 | `StringUtils` | `splitList`、`splitTo`、`str2List`、`str2Set`、`joinComma`、`toCamelCase`、`toUnderScoreCase` |
| 集合、Stream、Map | `org.dromara.common.core.utils.StreamUtils` | `filter`、`toList`、`toSet`、`toMap`、`groupByKey`、`sorted`、`join`、`merge` |
| 集合空值和 Map 工具 | Hutool `CollUtil`、`MapUtil` | 空集合判断、空 Map 判断、创建可变集合 |
| 对象安全取值 | `org.dromara.common.core.utils.ObjectUtils` | `notNullGetter`、`notNull` |
| BO/Entity/VO 转换 | `org.dromara.common.core.utils.MapstructUtils` | `convert(source, Target.class)`、列表转换 |
| JSON | `org.dromara.common.json.utils.JsonUtils` | `toJsonString`、`parseObject`、`parseArray`、`parseMap`、`isJson` |
| 日期时间 | `org.dromara.common.core.utils.DateUtils` | 继承 Hutool `DateUtil`；时间差、范围校验和友好时间用本类已有方法 |
| 树结构 | `org.dromara.common.core.utils.TreeBuildUtils` | `build`、`buildMultiRoot`、`getLeafNodes`、`buildTreeNodeMap` |
| 参数校验 | `ValidatorUtils.validate`、分组校验注解 | 新增/编辑/查询分组；业务失败抛 `ServiceException` |
| 国际化 | `org.dromara.common.core.utils.MessageUtils` | `message("code", args...)` |
| 下载文件名 | `org.dromara.common.core.utils.file.FileUtils` | `setAttachmentResponseHeader`、`percentEncode` |
| IP 判断与匹配 | `org.dromara.common.core.utils.NetUtils` | `isIPv4`、`isIPv6`、`isInnerIPv6`、`isMatchIpRule`、`isMatchCidr` |
| 正则提取 | `org.dromara.common.core.utils.regex.RegexUtils` | `extractFromString`；预定义规则用 `RegexConstants` |
| SQL 排序和关键字 | `org.dromara.common.core.utils.sql.SqlUtil` | `escapeOrderBySql`、`isValidOrderBySql`、`filterKeyword` |

## 各领域边界

### 字符串与集合

- 先看 `StringUtils` 是否已经提供等价方法，再考虑 `StrUtil`、Commons Lang3 或手写。
- `StringUtils` 继承 Commons Lang3，因此 `isBlank`、`isNotBlank`、`join`、`split`、`capitalize` 等继承方法也可用；不要仅因为方法定义不在当前文件就另写一份。
- `StreamUtils` 的集合转换会跳过 `null` 元素，并保留项目约定的可变 `List` 语义；涉及空集合、去重和顺序时先读实现。
- 普通集合操作优先用 `StreamUtils`；复杂流式组合可以直接使用标准 Stream API，但要保持同样的空值和可变集合行为。

### 对象、DTO 与树

- BO/Entity/VO 和列表转换优先 `MapstructUtils`，不要手写逐字段赋值或平行映射器。
- `ObjectUtils` 只做安全取值和默认值；不要为一次空判断新建 `ObjectHelper`。
- 树结构优先 `TreeBuildUtils`，前端树组件和 `handleTree` 只在页面层使用；父级 ID、根节点和多根节点的约定以后端当前实现为准。

### JSON、日期与校验

- 请求、响应、缓存和 JSON 字段使用 `JsonUtils`，不要另建 `JsonMapper` 或静态 `ObjectMapper`。
- `JsonUtils` 的空文本、空数组和解析失败行为并不完全一致；调用前看当前方法签名，需要静默解析时不要假设存在 `parseObjectQuietly`。
- 日期计算、时间差、范围校验和友好展示先看 `DateUtils`；实体字段和接口使用项目现有的 `LocalDateTime`、`Date` 约定，不自行拼接 `SimpleDateFormat`。
- 业务方法内部需要校验 DTO 时用 `ValidatorUtils.validate` 和现有分组；Controller 参数优先用 `@Validated` 与分组注解。

### 文件、网络、安全与 SQL

- 文件下载响应头用 `FileUtils`，OSS 文件信息走 `OssService` / `OssClient`，不要把本地路径或二进制塞进通用 JSON 接口。
- IP 判断和网段匹配用 `NetUtils`，IP 归属和区域用 `AddressUtils` / `RegionUtils`；不要复制 CIDR 解析。
- 排序字段和查询关键字使用 `SqlUtil` 的现有校验；SQL 仍通过 Wrapper 或参数绑定，不拼接用户输入。
- 加密、脱敏、缓存、Excel 等有专门公共模块，使用对应模块入口，不在业务 Service 手写同类基础算法。

## 什么时候自己写

只有满足以下至少一条时才写私有工具或内联逻辑：

- 现有工具的空值、异常、精度、默认值或排序语义与业务不一致。
- 规则只属于当前业务，放进公共层会污染通用 API。
- 现有工具需要昂贵的通用化改造，而当前需求只需要一个小范围处理。
- 现有工具确实没有该能力，且标准库或已引入依赖也没有合适实现。

写完后把差异留在业务模块的私有方法中；有第二个稳定调用方、且语义确实一致时，再评估提升为公共工具。

## 常见重复实现

| 不要这样写 | 先检查 |
|---|---|
| 手写逗号拆分、去空、去重 | `StringUtils.str2List`、`StringUtils.splitList`、`StreamUtils` |
| 手写 `for` 循环做集合转 Map、分组、拼接 | `StreamUtils.toMap`、`groupByKey`、`join` |
| 手写 BO/VO 逐字段复制 | `MapstructUtils.convert` |
| 新建 `ObjectMapper` 或手写 JSON 字符串 | `JsonUtils` |
| 手写递归建树、找叶子、拼路径 | `TreeBuildUtils` |
| 手写日期差、范围校验 | `DateUtils` |
| 复制正则、IP 或 SQL 排序校验 | `RegexUtils`、`NetUtils`、`SqlUtil` |
| 为一个业务加通用 `XxxUtils` | 先查现有工具；单业务逻辑留在业务模块 |

## 检查

- [ ] 已搜索 `ruoyi-common-core`、`ruoyi-common-json`、相关公共模块和目标模块。
- [ ] 已读当前 checkout 的方法签名和空值、异常、返回类型语义。
- [ ] 没有复制项目已有工具，也没有搭建第二套 JSON、转换、树或校验实现。
- [ ] 新增私有工具只承载当前业务规则，并说明了不能复用的原因。
