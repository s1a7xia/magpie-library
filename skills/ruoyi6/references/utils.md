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

## 按场景找入口

下表只回答“这类处理该去哪个类找”；具体方法名、重载和返回值以当前 checkout 为准，不要凭清单或旧示例直接调用。

| 场景 | 优先入口 |
|---|---|
| 字符串判空、截取、格式化、拆分、拼接、命名转换 | `org.dromara.common.core.utils.StringUtils`（继承 Commons Lang3） |
| 集合、Stream、Map 转换 | `org.dromara.common.core.utils.StreamUtils` |
| 集合空值和 Map 工具 | Hutool `CollUtil`、`MapUtil` |
| 对象安全取值、默认值 | `org.dromara.common.core.utils.ObjectUtils` |
| BO/Entity/VO 及列表转换 | `org.dromara.common.core.utils.MapstructUtils` |
| JSON 序列化与解析 | `org.dromara.common.json.utils.JsonUtils` |
| 日期时间计算、范围校验、友好展示 | `org.dromara.common.core.utils.DateUtils`（继承 Hutool `DateUtil`） |
| 树结构构建、找叶子、多根节点 | `org.dromara.common.core.utils.TreeBuildUtils` |
| 参数校验、分组校验 | `ValidatorUtils` 与现有分组注解 |
| 国际化消息 | `org.dromara.common.core.utils.MessageUtils` |
| 下载文件名与响应头 | `org.dromara.common.core.utils.file.FileUtils` |
| IP 判断与网段匹配 | `org.dromara.common.core.utils.NetUtils` |
| 正则提取 | `org.dromara.common.core.utils.regex.RegexUtils`、`RegexConstants` |
| SQL 排序与关键字校验 | `org.dromara.common.core.utils.sql.SqlUtil` |

不确定某个能力是否已封装时，先按“选择顺序”找到对应类，再读当前源码中的可用方法，而不是假设存在某个方法名。

## 各领域边界

### 字符串与集合

- 先看 `StringUtils` 是否已经提供等价方法，再考虑 `StrUtil`、Commons Lang3 或手写。
- `StringUtils` 继承 Commons Lang3，因此父类的判空、拼接、拆分、大小写等方法同样可用；不要仅因为方法定义不在当前文件就另写一份。
- `StreamUtils` 的集合转换会跳过 `null` 元素，并保留项目约定的可变 `List` 语义；涉及空集合、去重和顺序时先读实现。
- 普通集合操作优先用 `StreamUtils`；复杂流式组合可以直接使用标准 Stream API，但要保持同样的空值和可变集合行为。

### 对象、DTO 与树

- BO/Entity/VO 和列表转换优先 `MapstructUtils`，不要手写逐字段赋值或平行映射器。
- `ObjectUtils` 只做安全取值和默认值；不要为一次空判断新建 `ObjectHelper`。
- 树结构优先 `TreeBuildUtils`，前端树组件和 `handleTree` 只在页面层使用；父级 ID、根节点和多根节点的约定以后端当前实现为准。

### JSON、日期与校验

- 请求、响应、缓存和 JSON 字段使用 `JsonUtils`，不要另建 `JsonMapper` 或静态 `ObjectMapper`。
- `JsonUtils` 对不同输入（空文本、空数组、解析失败）的行为并不一致；调用前看当前方法签名，不要假设存在某个工具方法。
- 日期计算、时间差、范围校验和友好展示先看 `DateUtils`；实体字段和接口使用项目现有的 `LocalDateTime`、`Date` 约定，不自行拼接 `SimpleDateFormat`。
- 业务方法内部需要校验 DTO 时用 `ValidatorUtils.validate` 和现有分组；Controller 参数优先用 `@Validated` 与分组注解。

### 文件、网络、安全与 SQL

- 文件下载响应头用 `FileUtils`，OSS 文件信息走 `OssService` / `OssClient`，不要把本地路径或二进制塞进通用 JSON 接口。
- IP 判断和网段匹配用 `NetUtils`，IP 归属和区域用 `org.dromara.common.core.utils.ip.AddressUtils` / `RegionUtils`；不要复制 CIDR 解析。
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
| 手写字符串拆分、去空、去重 | `StringUtils`、`StreamUtils` |
| 手写 `for` 循环做集合转 Map、分组、拼接 | `StreamUtils` |
| 手写 BO/VO 逐字段复制 | `MapstructUtils` |
| 新建 `ObjectMapper` 或手写 JSON 字符串 | `JsonUtils` |
| 手写递归建树、找叶子、拼路径 | `TreeBuildUtils` |
| 手写日期差、范围校验 | `DateUtils` |
| 自己写正则、IP 或 SQL 排序校验 | `RegexUtils`、`NetUtils`、`SqlUtil` |
| 为一个业务加通用 `XxxUtils` | 先查现有工具；单业务逻辑留在业务模块 |

## 检查

- [ ] 已搜索 `ruoyi-common-core`、`ruoyi-common-json`、相关公共模块和目标模块。
- [ ] 已读当前 checkout 的方法签名和空值、异常、返回类型语义。
- [ ] 没有复制项目已有工具，也没有搭建第二套 JSON、转换、树或校验实现。
- [ ] 新增私有工具只承载当前业务规则，并说明了不能复用的原因。
