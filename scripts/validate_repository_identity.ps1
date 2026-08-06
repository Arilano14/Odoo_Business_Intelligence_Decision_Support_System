# PowerShell Repository Identity and Attribution Validator
# Canonical URL: https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git
# Maintainer: @Arilano14

$CanonicalUrl = "https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git"
$Owner = "@Arilano14"

Write-Host "=========================================================================="
Write-Host "VALIDATING REPOSITORY IDENTITY AND ATTRIBUTION"
Write-Host "=========================================================================="

# 1. Verify Git Repository
if (-not (Test-Path ".git")) {
    Write-Error "[FAIL] Current directory is not a valid Git repository!"
    exit 1
}

# 2. Check Canonical URL in README.md
if (Test-Path "README.md") {
    $ReadmeText = Get-Content "README.md" -Raw
    if ($ReadmeText -match [regex]::Escape($CanonicalUrl)) {
        Write-Host "  [PASS] Canonical URL present in README.md"
    } else {
        Write-Error "[FAIL] Canonical URL missing from README.md"
        exit 1
    }
}

# 3. Check Canonical URL in NOTICE
if (Test-Path "NOTICE") {
    $NoticeText = Get-Content "NOTICE" -Raw
    if ($NoticeText -match [regex]::Escape($Owner)) {
        Write-Host "  [PASS] Owner @Arilano14 present in NOTICE"
    } else {
        Write-Error "[FAIL] Owner missing from NOTICE"
        exit 1
    }
}

# 4. Check CODEOWNERS
if (Test-Path ".github/CODEOWNERS") {
    $CodeownersText = Get-Content ".github/CODEOWNERS" -Raw
    if ($CodeownersText -match [regex]::Escape($Owner)) {
        Write-Host "  [PASS] Owner @Arilano14 present in .github/CODEOWNERS"
    } else {
        Write-Error "[FAIL] Owner missing from .github/CODEOWNERS"
        exit 1
    }
}

# 5. Display Remotes
Write-Host "`nCurrent Git Remotes:"
git remote -v

Write-Host "=========================================================================="
Write-Host "[SUCCESS] REPOSITORY IDENTITY VALIDATION PASSED!"
Write-Host "=========================================================================="
