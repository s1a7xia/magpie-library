# Human-in-the-loop reproduction loop for Codex on Windows PowerShell 7.
# Copy this file, edit the steps below, and run it with:
#   pwsh -NoLogo -NoProfile -File .\hitl-loop.template.ps1
#
# The Codex session runs the script; the user follows prompts in the terminal.
# Capture observations only. Leave sign-in and other credential entry to the user.

$ErrorActionPreference = 'Stop'

function Step {
    param([Parameter(Mandatory)][string]$Instruction)
    Write-Host ""
    Write-Host ">>> $Instruction"
    Read-Host "    [Enter when done]" | Out-Null
}

function Capture {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][string]$Question
    )
    Write-Host ""
    Write-Host ">>> $Question"
    return Read-Host "    >"
}

# --- edit below ---------------------------------------------------------

Step "Open the app at http://localhost:3000 and sign in."

$errored = Capture -Name "ERRORED" -Question "Click the 'Export' button. Did it throw an error? (y/n)"
$errorMessage = Capture -Name "ERROR_MSG" -Question "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

Write-Host ""
Write-Host "--- Captured ---"
Write-Host "ERRORED=$errored"
Write-Host "ERROR_MSG=$errorMessage"
