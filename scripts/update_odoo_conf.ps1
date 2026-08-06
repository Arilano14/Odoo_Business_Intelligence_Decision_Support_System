$confPath = "C:\Program Files\Odoo 18.0.20241229\server\odoo.conf"
$content = Get-Content $confPath -Raw
$old = "addons_path = c:\program files\odoo 18.0.20241229\server\odoo\addons"
$new = "addons_path = c:\program files\odoo 18.0.20241229\server\odoo\addons,c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\custom_addons"
$content = $content.Replace($old, $new)
[System.IO.File]::WriteAllText($confPath, $content)
Write-Output "SUCCESS: odoo.conf updated"

# Also restart the service
Stop-Service "odoo-server-18.0" -Force
Start-Sleep -Seconds 3
Start-Service "odoo-server-18.0"
Write-Output "Odoo service restarted"
