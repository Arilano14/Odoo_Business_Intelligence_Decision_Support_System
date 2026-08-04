@echo off
rem Batch script to update odoo.conf and sync custom_addons directory

set CONF="C:\Program Files\Odoo 18.0.20241229\server\odoo.conf"
set TARGET="C:\Program Files\Odoo 18.0.20241229\server\odoo\addons\obidss_operational_bi"
set SRC="c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\custom_addons\obidss_operational_bi"

rem 1. Sync custom_addons folder to runtime addons path
if not exist %TARGET% mkdir %TARGET%
xcopy /E /Y /I %SRC%\* %TARGET%\

rem 2. Stop and start Odoo service to reload
net stop "odoo-server-18.0"
timeout /t 2 /nobreak
net start "odoo-server-18.0"

echo SYNC COMPLETE > "c:\Users\Arilano\Downloads\Project ARICE\Project Odoo\docs\phase11_2_live\sync_status.txt"
