admin_user = env['res.users'].browse(2)
group_admin = env.ref('obidss_operational_bi.group_obidss_admin', raise_if_not_found=False)

if group_admin:
    group_admin.write({'users': [(4, admin_user.id)]})
    env.cr.commit()
    print("Added Admin (ID 2) to OBIDSS Administrator group!")
else:
    print("Group obidss_operational_bi.group_obidss_admin not found!")
