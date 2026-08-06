# PowerShell script to configure canonical repository remotes safely
# Canonical Repository: https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git

$CanonicalUrl = "https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git"

Write-Host "=========================================================================="
Write-Host "CANONICAL REPOSITORY REMOTE CONFIGURATION & GOVERNANCE"
Write-Host "=========================================================================="

# 1. Verify Git Repository
if (-not (Test-Path ".git")) {
    Write-Error "Current directory is not a valid Git repository!"
    exit 1
}

# 2. Inspect Existing Remotes
$Remotes = git remote -v

Write-Host "Current Remotes:"
Write-Host $Remotes

$OriginExists = $Remotes -match "origin"
$UpstreamExists = $Remotes -match "upstream"

if (-not $OriginExists) {
    Write-Host "Configuring origin -> $CanonicalUrl"
    git remote add origin $CanonicalUrl
} else {
    Write-Host "Origin exists. Preserving origin and adding canonical repository as upstream if absent..."
    if (-not $UpstreamExists) {
        git remote add upstream $CanonicalUrl
        Write-Host "Added upstream -> $CanonicalUrl"
    } else {
        Write-Host "Upstream remote already configured."
    }
}

Write-Host "`nUpdated Remotes:"
git remote -v
Write-Host "=========================================================================="
