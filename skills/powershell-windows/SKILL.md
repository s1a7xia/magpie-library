---
name: powershell-windows
description: "编写或修改复杂 Windows PowerShell 7 脚本，或排查 PowerShell 的引号、管道、编码、路径与错误处理问题时使用。普通命令执行、读取文件或仅选择 shell 不必加载。"
---

# PowerShell 7 脚本与排错

## 适用范围

- 用于多步骤脚本、跨进程参数传递，以及 PowerShell 特有的解析或运行错误；简单的一行命令直接执行即可。
- 默认面向 PowerShell 7；只有目标明确要求 Windows PowerShell 5.1 时才考虑旧版兼容性。
- shell 的选择遵循全局执行约束。本技能不设置默认 shell；解释器不匹配先修正调用入口，不为错误解释器改写业务脚本。

## 引号、表达式与参数

- 组合 cmdlet 调用结果时，用括号界定调用，避免将逻辑运算符误解析为参数：

  ```powershell
  if ((Test-Path -LiteralPath $a) -or (Test-Path -LiteralPath $b)) { ... }
  ```

- 单引号字符串不展开变量，双引号字符串会展开。属性或复杂表达式使用 `$()`，例如 `"Value: $($obj.prop.sub)"`，这是合法语法；仅在有助阅读时拆成变量。
- 调用外部程序使用调用运算符和分开的参数，例如 `& $exe @arguments`；不要拼接命令字符串再用 `Invoke-Expression`。
- 多层 shell 引号容易提前展开 `$变量`。脚本较长或跨解释器调用时，优先保存为 `.ps1` 后使用 `pwsh -NoLogo -NoProfile -File <path>`，不要堆叠转义。

## 编码与路径

- PowerShell 7 支持 Unicode；中文和 emoji 并不是语法错误。文件通常使用 UTF-8；只有实际终端、旧版解析器或外部程序有限制时才调整编码或输出字符。
- `Unexpected token` 应按具体位置检查引号、括号和语法，不能直接归因于 Unicode。
- 文件名可能含 `[]` 等通配字符时，支持该参数的 cmdlet 使用 `-LiteralPath`；组合路径用 `Join-Path`，脚本目录用 `$PSScriptRoot`。
- 删除或移动文件使用同一 shell 的原生命令；递归操作前确认最终绝对目标在已授权范围内，不跨 shell 拼接破坏性命令。

## 错误处理

- `try/catch` 捕获终止错误。需要失败即停的 cmdlet 使用 `-ErrorAction Stop`；整个脚本确实需要此行为时再设置 `$ErrorActionPreference = 'Stop'`。
- 原生程序的失败不能仅依赖 `try/catch` 或 `$ErrorActionPreference`。调用后立即检查 `$LASTEXITCODE`，并按该程序定义判断哪些退出码是错误，不把所有非零码一概视为失败。
- `SilentlyContinue` 只用于已预期且有明确后续处理的错误，不用它掩盖未知失败。生产脚本也不应一律使用 `Continue`。
- `return` 可以出现在 `try` 中；资源清理放在 `finally`。只在脚本或进程边界需要时使用 `exit`，不要让复用函数终止调用者。

## 数据形状与 JSON

- 区分 `$null`、空集合、`0` 和 `$false`；不要用真假判断替代业务上的存在性判断。判断空值通常用 `$null -eq $value`。
- 需要稳定集合形状时使用 `@(...)`。JSON 或管道结果可能只有零项或一项，访问属性前按实际结构判断，不盲目追加 `.ToString()` 消除类型错误。
- JSON 使用 `Get-Content -LiteralPath $path -Raw | ConvertFrom-Json` 读取。序列化嵌套对象时按实际结构指定足够的 `ConvertTo-Json -Depth`，避免默认深度截断；写文件时明确 UTF-8。

## 排错收口

先确认实际解释器与版本，再定位失败语句、参数和退出码；只复查受影响路径。区分命令成功、脚本完成与业务验证，不把失败或截断输出当作结论。
