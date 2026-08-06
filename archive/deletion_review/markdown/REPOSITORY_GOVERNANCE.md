# REPOSITORY GOVERNANCE & SECURITY GUIDELINES

## Canonical Repository
- **URL**: `https://github.com/Arilano14/Odoo_Business_Intelligence_Decision_Support_System.git`
- **Owner**: `@Arilano14`

## GitHub Security Protections
The repository enforces the following security standards:
- Protected `main` branch with mandatory pull requests.
- Code Owner review required from `@Arilano14`.
- Blocked force pushes and branch deletions.
- Automated secret scanning and push protection enabled.
- Dependabot dependency reviews enabled.

## Branching and Migration Rules
1. All changes must pass automated verification checks before merging.
2. Direct SQL mutations on Odoo core tables are prohibited.
3. Database records and Power BI `.pbix` assets must be preserved without data loss.
