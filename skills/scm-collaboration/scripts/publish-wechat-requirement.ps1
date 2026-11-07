[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot,

    [Parameter(Mandatory = $true)]
    [string]$DraftDir,

    [Parameter(Mandatory = $true)]
    [string]$Title,

    [switch]$KeepDraft,

    [switch]$DryRun,

    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'

function Fail([string]$Message) {
    throw "WECHAT_REQUIREMENT_PUBLISH_FAILED: $Message"
}

if (-not (Test-Path -LiteralPath $DraftDir -PathType Container)) {
    Fail "draft directory not found: $DraftDir"
}

$resolvedDraft = (Resolve-Path -LiteralPath $DraftDir).Path
$bodyFile = Join-Path $resolvedDraft '需求.md'
if (-not (Test-Path -LiteralPath $bodyFile -PathType Leaf)) {
    Fail "draft body not found: $bodyFile"
}

$attachmentFiles = @()
$assetsDirectory = Join-Path $resolvedDraft 'assets'
if (Test-Path -LiteralPath $assetsDirectory -PathType Container) {
    $attachmentFiles = @(
        Get-ChildItem -LiteralPath $assetsDirectory -File -Force |
            ForEach-Object { $_.FullName }
    )
}

$publisher = Join-Path $PSScriptRoot 'publish-inbox.ps1'
if (-not (Test-Path -LiteralPath $publisher -PathType Leaf)) {
    Fail "publisher script not found: $publisher"
}

$arguments = @(
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-File', $publisher,
    '-RepoRoot', $RepoRoot,
    '-Title', $Title,
    '-ContentFile', $bodyFile
)
if ($attachmentFiles.Count -gt 0) {
    $arguments += '-Attachment'
    $arguments += ($attachmentFiles -join '|')
}
if ($DryRun) { $arguments += '-DryRun' }
if ($NoPush) { $arguments += '-NoPush' }

# With $ErrorActionPreference = 'Stop', merging a native command's stderr into
# the success stream turns a normal non-zero exit into a terminating error, so
# the JSON/exit-code handling below would never run.
$previousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
try {
    $raw = & powershell @arguments 2>&1
    $exitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $previousErrorActionPreference
}
$text = ($raw | ForEach-Object { $_.ToString() }) -join "`n"
if ($exitCode -ne 0) {
    throw $text.Trim()
}

try {
    $result = $text | ConvertFrom-Json
} catch {
    Fail "publisher returned non-JSON output: $($text.Trim())"
}

if (-not $DryRun -and $result.Status -eq 'PUBLISHED' -and $result.Push -eq 'PUSHED' -and -not $KeepDraft) {
    $bodyFile = Join-Path $resolvedDraft '需求.md'
    if (Test-Path -LiteralPath $bodyFile -PathType Leaf) {
        Remove-Item -LiteralPath $bodyFile -Force
    }
    $assetsDirectory = Join-Path $resolvedDraft 'assets'
    if (Test-Path -LiteralPath $assetsDirectory -PathType Container) {
        Remove-Item -LiteralPath $assetsDirectory -Recurse -Force
    }
    $remaining = @(Get-ChildItem -LiteralPath $resolvedDraft -Force)
    if ($remaining.Count -eq 0) {
        Remove-Item -LiteralPath $resolvedDraft -Force
    }
    $result | Add-Member -NotePropertyName DraftRemoved -NotePropertyValue (-not (Test-Path -LiteralPath $resolvedDraft)) -Force
    if (Test-Path -LiteralPath $resolvedDraft) {
        $result | Add-Member -NotePropertyName DraftRetainedReason -NotePropertyValue 'draft directory contains other files' -Force
    }
} else {
    $result | Add-Member -NotePropertyName DraftRemoved -NotePropertyValue $false -Force
}

$result | ConvertTo-Json -Depth 4
