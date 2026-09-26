# Lab M9 setup check for Windows (PowerShell 5.1 or PowerShell 7).
#
# Proves your tools are ready instead of assuming they are. Each check prints PASS or FAIL, and
# every FAIL prints the exact command that fixes it. Nothing here changes your machine: it only
# looks. Run it again after each fix until it says 4 of 4.
#
#   powershell -ExecutionPolicy Bypass -File .\check-setup.ps1
#
# "-ExecutionPolicy Bypass" lets this one script run without changing your machine's policy.
# Exit status is 0 when everything passes and 1 otherwise.

$passed = 0
$total = 4

function Write-Pass($message) {
    Write-Host "PASS  " -ForegroundColor Green -NoNewline
    Write-Host $message
    $script:passed++
}

function Write-Fail($message, $fix) {
    Write-Host "FAIL  " -ForegroundColor Red -NoNewline
    Write-Host $message
    Write-Host "      fix: $fix"
}

Write-Host "Lab M9 setup check - Windows" -ForegroundColor Cyan
Write-Host ""

# 1. git
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Pass "git is installed: $(git --version)"
} else {
    Write-Fail "git is not installed" "winget install --id Git.Git -e --source winget   then open a NEW terminal window"
}

# 2. gh, the GitHub CLI
$hasGh = [bool](Get-Command gh -ErrorAction SilentlyContinue)
if ($hasGh) {
    $ghVersion = (gh --version | Select-Object -First 1)
    Write-Pass "GitHub CLI is installed: $ghVersion"
} else {
    Write-Fail "GitHub CLI (gh) is not installed" "winget install --id GitHub.cli --source winget   then open a NEW terminal window"
}

# 3. your name and email on commits
$name = ""
$email = ""
if (Get-Command git -ErrorAction SilentlyContinue) {
    $name = (git config --global user.name) 2>$null
    $email = (git config --global user.email) 2>$null
}
if ($name -and $email) {
    Write-Pass "git knows who you are: $name <$email>"
} else {
    Write-Fail "git does not know your name and email yet" 'git config --global user.name "Your Name"   and   git config --global user.email "you@example.com"'
}

# 4. signed in to GitHub
$signedIn = $false
if ($hasGh) {
    gh auth status *> $null
    $signedIn = ($LASTEXITCODE -eq 0)
}
if ($signedIn) {
    $account = (gh api user --jq .login) 2>$null
    if (-not $account) { $account = "your account" }
    Write-Pass "signed in to GitHub as $account"
} else {
    Write-Fail "not signed in to GitHub from the terminal" "gh auth login   (choose GitHub.com, HTTPS, yes to git credentials, log in with a web browser)"
}

Write-Host ""
Write-Host "$passed of $total checks passed." -ForegroundColor Cyan
if ($passed -eq $total) {
    Write-Host "You are ready for Lab M9. Paste this output into your evidence log."
    exit 0
}
Write-Host "Fix the first FAIL above, open a new terminal window, and run this again."
exit 1
