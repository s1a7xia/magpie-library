[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot,

    [Parameter(Mandatory = $true)]
    [string]$Title,

    [Parameter(Mandatory = $true)]
    [string]$ContentFile,

    [ValidateSet('requirement', 'research')]
    [string]$Kind = 'requirement',

    [string[]]$Attachment = @(),

    [switch]$DryRun,

    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Fail([string]$Message) {
    throw "INBOX_PUBLISH_FAILED: $Message"
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [switch]$AllowFailure
    )

    $quoted = @($Arguments | ForEach-Object {
        if ($_ -match '^[A-Za-z0-9_./:@{}~^=+-]+$') {
            $_
        } else {
            '"' + ($_ -replace '"', '\"') + '"'
        }
    })
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = 'git'
    $startInfo.Arguments = '-c core.quotepath=false -C "' + ($script:ResolvedRepo -replace '"', '\"') + '" ' + ($quoted -join ' ')
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    try {
        $startInfo.StandardOutputEncoding = New-Object System.Text.UTF8Encoding($false)
        $startInfo.StandardErrorEncoding = New-Object System.Text.UTF8Encoding($false)
    } catch {
        # Windows PowerShell 5.1 exposes these properties but may reject setting them.
    }
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    [void]$process.Start()
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    $code = $process.ExitCode
    $process.Dispose()
    $lines = @()
    if ($stdout) {
        $lines += @($stdout -split "`r?`n" | Where-Object { $_ -ne '' })
    }
    if ($stderr) {
        $lines += @($stderr -split "`r?`n" | Where-Object { $_ -ne '' })
    }
    if ($code -ne 0 -and -not $AllowFailure) {
        Fail ("git {0} failed: {1}" -f ($Arguments -join ' '), (($lines -join "`n").Trim()))
    }
    return [pscustomobject]@{
        Code = $code
        Lines = $lines
        Text = ($lines -join "`n").Trim()
    }
}

function Convert-ToRepoRelative([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path)
    $root = [System.IO.Path]::GetFullPath($script:ResolvedRepo).TrimEnd('\', '/')
    $comparison = [System.StringComparison]::OrdinalIgnoreCase
    if (-not $full.StartsWith($root + [System.IO.Path]::DirectorySeparatorChar, $comparison)) {
        Fail "path is outside the repository: $Path"
    }
    return $full.Substring($root.Length + 1).Replace('\', '/')
}

function Test-SensitiveName([string]$Name) {
    $sensitiveNames = @(
        '.env', '.env.local', '.env.production',
        'id_rsa', 'id_ed25519', 'credentials', 'secrets'
    )
    $sensitiveExtensions = @(
        '.pem', '.key', '.pfx', '.p12', '.jks', '.keystore', '.kdbx'
    )
    $extension = [System.IO.Path]::GetExtension($Name).ToLowerInvariant()
    return $sensitiveNames -contains $Name.ToLowerInvariant() -or
        $sensitiveExtensions -contains $extension
}

function ConvertTo-MarkdownText([string]$Value) {
    return $Value.Replace('\', '\\').Replace('[', '\[').Replace(']', '\]')
}

function ConvertTo-MarkdownPath([string]$Value) {
    $segments = $Value -split '/'
    return (@($segments | ForEach-Object { [System.Uri]::EscapeDataString($_) }) -join '/')
}

function Test-SensitiveDiff([string]$RelativePath) {
    $diff = Invoke-Git -Arguments @(
        'diff', '--cached', '--no-ext-diff', '--unified=0', '--', $RelativePath
    )
    $patterns = @(
        @{ Label = 'private key'; Pattern = '-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----' },
        @{ Label = 'GitHub token'; Pattern = '\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{20,}\b' },
        @{ Label = 'GitHub fine-grained token'; Pattern = '\bgithub_pat_[A-Za-z0-9_]{20,}\b' },
        @{ Label = 'GitLab token'; Pattern = '\bglpat-[A-Za-z0-9_-]{20,}\b' },
        @{ Label = 'Slack token'; Pattern = '\bxox(?:b|p|a|r|s)-[A-Za-z0-9-]{20,}\b' },
        @{ Label = 'AWS access key'; Pattern = '\b(?:AKIA|ASIA)[A-Z0-9]{16}\b' },
        @{ Label = 'Telegram bot token'; Pattern = '\b\d{8,12}:[A-Za-z0-9_-]{30,}\b' },
        @{ Label = 'credentialed connection string'; Pattern = '\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^/\s:@]+:[^@\s]+@' }
    )

    $findings = New-Object System.Collections.Generic.List[string]
    foreach ($line in $diff.Lines) {
        $text = [string]$line
        if (-not $text.StartsWith('+') -or $text.StartsWith('+++')) {
            continue
        }
        foreach ($item in $patterns) {
            if ($text -match $item.Pattern) {
                $findings.Add($item.Label)
                break
            }
        }
    }
    if ($findings.Count -gt 0) {
        Fail "possible secret in requirement files ($($findings -join ', ')); commit stopped"
    }
}

if ([string]::IsNullOrWhiteSpace($Title)) {
    Fail 'title is required'
}
if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Fail "repository directory not found: $RepoRoot"
}
if (-not (Test-Path -LiteralPath $ContentFile -PathType Leaf)) {
    Fail "content file not found: $ContentFile"
}

$script:ResolvedRepo = (Resolve-Path -LiteralPath $RepoRoot).Path

if ($Kind -eq 'research') {
    $targetRoot = 'docs/research/inbox'
    $idPrefix = 'RES'
    $bodyFileName = '调研简报.md'
    $commitPrefix = 'research'
    $itemLabel = '调研简报'
} else {
    $targetRoot = 'docs/inbox'
    $idPrefix = 'REQ'
    $bodyFileName = '需求.md'
    $commitPrefix = 'req'
    $itemLabel = '需求'
}

# The wrapper passes attachment paths joined by '|' because powershell -File
# cannot bind an array to a single named parameter without the trailing values
# being treated as extra positional arguments. '|' cannot appear in a Windows
# file name, so splitting here is lossless.
$expandedAttachments = @()
foreach ($path in $Attachment) {
    if ($null -eq $path) {
        continue
    }
    foreach ($part in ([string]$path -split '\|')) {
        if (-not [string]::IsNullOrWhiteSpace($part)) {
            $expandedAttachments += $part
        }
    }
}
$Attachment = $expandedAttachments

$topLevel = Invoke-Git -Arguments @('rev-parse', '--show-toplevel')
$actualRoot = [System.IO.Path]::GetFullPath($topLevel.Text)
if ([System.IO.Path]::GetFullPath($script:ResolvedRepo).TrimEnd('\', '/') -ne $actualRoot.TrimEnd('\', '/')) {
    Fail "RepoRoot must be the Git worktree root: $actualRoot"
}

$branchResult = Invoke-Git -Arguments @('symbolic-ref', '--quiet', '--short', 'HEAD') -AllowFailure
if ($branchResult.Code -ne 0 -or [string]::IsNullOrWhiteSpace($branchResult.Text)) {
    Fail 'detached HEAD is not publishable'
}
$branch = $branchResult.Text.Trim()
$defaultBranchNames = @('main', 'master', 'develop', 'dev', 'production', 'prod')
$remoteResult = Invoke-Git -Arguments @('config', "--get", "branch.$branch.remote")
$mergeResult = Invoke-Git -Arguments @('config', "--get", "branch.$branch.merge")
$remote = $remoteResult.Text.Trim()
$mergeRef = $mergeResult.Text.Trim()
if (-not $remote -or -not $mergeRef) {
    Fail "upstream configuration is incomplete: $branch"
}
$remoteHead = Invoke-Git -Arguments @(
    'symbolic-ref', '--quiet', '--short', "refs/remotes/$remote/HEAD"
) -AllowFailure
if ($remoteHead.Code -eq 0 -and $remoteHead.Text.Trim()) {
    $remoteDefault = $remoteHead.Text.Trim() -replace "^$([regex]::Escape($remote))/", ''
    $defaultBranchNames += $remoteDefault
}
if ($branch -in $defaultBranchNames -or $branch -match '^release/') {
    Fail "protected/default branch is not publishable: $branch"
}

$upstreamResult = Invoke-Git -Arguments @('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}') -AllowFailure
if ($upstreamResult.Code -ne 0 -or [string]::IsNullOrWhiteSpace($upstreamResult.Text)) {
    Fail "current branch has no configured upstream: $branch"
}
$upstream = $upstreamResult.Text.Trim()

# Publishing must never drag unrelated local commits to the remote. Unpushed
# commits that only touch the same publishing root are earlier publishes whose
# push failed; allowing them makes a retry possible without weakening the
# guarantee for business changes.
$aheadLog = Invoke-Git -Arguments @(
    'log', '--format=@%H', '--name-only', '@{u}..HEAD'
)
$aheadCommits = 0
$foreignPaths = New-Object System.Collections.Generic.List[string]
foreach ($line in $aheadLog.Lines) {
    $text = [string]$line
    if ($text.StartsWith('@')) {
        $aheadCommits++
        continue
    }
    foreach ($path in ($text -split "`t")) {
        $normalized = $path.Replace('\', '/').Trim()
        if ($normalized -and -not $normalized.StartsWith("$targetRoot/", [System.StringComparison]::OrdinalIgnoreCase)) {
            if (-not $foreignPaths.Contains($normalized)) {
                $foreignPaths.Add($normalized)
            }
        }
    }
}
if ($foreignPaths.Count -gt 0) {
    Fail ("$branch 有 {0} 个未推送提交包含{1}目录外的改动（首个：{2}）；请先推送或处理这些提交再发布" -f $aheadCommits, $itemLabel, $foreignPaths[0])
}

# A behind branch cannot fast-forward push. Reject before writing so a retry
# does not pile up local requirement commits that can never be published.
$behindResult = Invoke-Git -Arguments @('rev-list', '--count', 'HEAD..@{u}')
$behind = 0
if (-not [int]::TryParse($behindResult.Text.Trim(), [ref]$behind)) {
    Fail "could not read how far $branch is behind $upstream"
}
if ($behind -ne 0) {
    Fail "$branch is $behind commit(s) behind $upstream; update the branch before publishing a requirement"
}

$dateTag = Get-Date -Format 'yyyyMMdd'
$inboxRoot = Join-Path $script:ResolvedRepo ($targetRoot -replace '/', '\')
$existingNumbers = @()
if (Test-Path -LiteralPath $inboxRoot -PathType Container) {
    $existingNumbers = Get-ChildItem -LiteralPath $inboxRoot -Force |
        Where-Object { $_.Name -match "^$idPrefix-$dateTag-(\d{3})(?:$|[.-])" } |
        ForEach-Object {
            if ($_.Name -match "^$idPrefix-$dateTag-(\d{3})") {
                [int]$Matches[1]
            }
        }
}
$nextNumber = 1
if ($existingNumbers.Count -gt 0) {
    # Measure-Object returns a Double, and the "D3" numeric format specifier is
    # integral-only, so the maximum must be cast back to Int32 before formatting.
    $maxExisting = [int](($existingNumbers | Measure-Object -Maximum).Maximum)
    $nextNumber = $maxExisting + 1
}
$itemId = "$idPrefix-$dateTag-{0:D3}" -f $nextNumber
$itemRelative = "$targetRoot/$itemId"
$itemDirectory = Join-Path $script:ResolvedRepo (($targetRoot -replace '/', '\') + '\' + $itemId)
$itemFile = Join-Path $itemDirectory $bodyFileName

if (Test-Path -LiteralPath $itemDirectory) {
    Fail "$itemLabel directory already exists: $itemDirectory"
}

$attachmentFiles = @()
$attachmentBytes = 0L
foreach ($path in $Attachment) {
    if ([string]::IsNullOrWhiteSpace($path)) {
        continue
    }
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Fail "attachment not found: $path"
    }
    $item = Get-Item -LiteralPath $path -Force
    if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        Fail "attachment is a link and is not accepted: $path"
    }
    if (Test-SensitiveName $item.Name) {
        Fail "sensitive attachment filename is not accepted: $($item.Name)"
    }
    if ($attachmentFiles.Name -contains $item.Name) {
        Fail "duplicate attachment filename: $($item.Name)"
    }
    $attachmentBytes += $item.Length
    if ($item.Length -gt 50MB) {
        Fail "attachment exceeds the 50 MB per-file limit: $($item.Name)"
    }
    $attachmentFiles += $item
}
if ($attachmentBytes -gt 100MB) {
    Fail "attachments exceed the 100 MB total limit"
}

$body = Get-Content -LiteralPath $ContentFile -Raw -Encoding utf8
if ([string]::IsNullOrWhiteSpace($body)) {
    Fail 'content file is empty'
}
if ($body -match '(?im)^\s*(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*\S+') {
    Fail 'content file contains a credential-like assignment; replace it with a placeholder'
}

$attachmentSection = ''
if ($attachmentFiles.Count -gt 0) {
    $links = $attachmentFiles | ForEach-Object {
        $label = ConvertTo-MarkdownText $_.Name
        $target = ConvertTo-MarkdownPath "assets/$($_.Name)"
        "- [$label]($target)"
    }
    $attachmentSection = "`n`n## 附件`n`n" + ($links -join "`n") + "`n"
}

if ($DryRun) {
    $dryRunResult = [ordered]@{
        Status = 'DRY_RUN'
        RepoRoot = $script:ResolvedRepo
        Branch = $branch
        Upstream = $upstream
        Kind = $Kind
        ItemId = $itemId
        ItemPath = $itemRelative
        BodyFile = $bodyFileName
        Attachments = @($attachmentFiles | ForEach-Object { $_.Name })
    }
    if ($Kind -eq 'research') {
        $dryRunResult.ResearchId = $itemId
        $dryRunResult.ResearchPath = $itemRelative
    } else {
        $dryRunResult.RequirementId = $itemId
        $dryRunResult.RequirementPath = $itemRelative
    }
    [pscustomobject]$dryRunResult | ConvertTo-Json -Depth 4
    exit 0
}

New-Item -ItemType Directory -Path $itemDirectory -Force | Out-Null
$committed = $false
try {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($itemFile, ($body.TrimEnd() + $attachmentSection), $utf8NoBom)

    if ($attachmentFiles.Count -gt 0) {
        $assetsDirectory = Join-Path $itemDirectory 'assets'
        New-Item -ItemType Directory -Path $assetsDirectory -Force | Out-Null
        foreach ($file in $attachmentFiles) {
            Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $assetsDirectory $file.Name)
        }
    }

    Invoke-Git -Arguments @('add', '--', $itemRelative) | Out-Null
    $staged = Invoke-Git -Arguments @('diff', '--cached', '--name-only', '--', $itemRelative)
    if ($staged.Lines.Count -eq 0) {
        Fail "no $itemLabel files were staged"
    }
    foreach ($path in $staged.Lines) {
        if (-not $path.Replace('\', '/').StartsWith($itemRelative + '/', [System.StringComparison]::OrdinalIgnoreCase)) {
            Fail "staged path escaped the $itemLabel directory: $path"
        }
    }

    Test-SensitiveDiff $itemRelative

    $commit = Invoke-Git -Arguments @(
        'commit', '--only', '-m', "$commitPrefix`: $Title", '--', $itemRelative
    )
    $head = (Invoke-Git -Arguments @('rev-parse', 'HEAD')).Text.Trim()
    $committed = $true
    $commitFiles = Invoke-Git -Arguments @('show', '--pretty=format:', '--name-only', 'HEAD')
    foreach ($path in $commitFiles.Lines) {
        if ($path -and -not $path.Replace('\', '/').StartsWith($itemRelative + '/', [System.StringComparison]::OrdinalIgnoreCase)) {
            Fail "commit contains a path outside the $itemLabel directory: $path"
        }
    }

    $pushStatus = 'NOT_PUSHED'
    $pushError = ''
    if (-not $NoPush) {
        $push = Invoke-Git -Arguments @('push') -AllowFailure
        if ($push.Code -ne 0) {
            $pushStatus = 'FAILED'
            $pushError = $push.Text
        } else {
            $tracking = Invoke-Git -Arguments @('rev-parse', '@{u}')
            if ($tracking.Text.Trim() -ne $head) {
                Invoke-Git -Arguments @('fetch', '--no-tags', $remote, $mergeRef) | Out-Null
                $tracking = Invoke-Git -Arguments @('rev-parse', '@{u}')
            }
            if ($tracking.Text.Trim() -ne $head) {
                $pushStatus = 'FAILED'
                $pushError = "push completed but upstream does not match HEAD ($upstream)"
            } else {
                $pushStatus = 'PUSHED'
            }
        }
    }

    $result = [ordered]@{
        Status = 'PUBLISHED'
        Kind = $Kind
        ItemId = $itemId
        ItemPath = $itemRelative
        Attachments = @($attachmentFiles | ForEach-Object { $_.Name })
        Commit = $head
        Branch = $branch
        Upstream = $upstream
        Push = $pushStatus
    }
    if ($Kind -eq 'research') {
        $result.ResearchId = $itemId
        $result.ResearchPath = $itemRelative
    } else {
        $result.RequirementId = $itemId
        $result.RequirementPath = $itemRelative
    }
    if ($pushStatus -eq 'FAILED') {
        $result.Status = 'COMMITTED'
        $result.PushError = $pushError
    }
    [pscustomobject]$result | ConvertTo-Json -Depth 4
}
catch {
    if (-not $committed -and (Test-Path -LiteralPath $itemDirectory)) {
        & git -C $script:ResolvedRepo reset --quiet -- $itemRelative 2>$null
        Remove-Item -LiteralPath $itemDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
    throw
}
