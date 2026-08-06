# Target Menu Access Control & Role Matrix — Phase 11.2

**Date:** August 4, 2026  
**Status:** **DESIGN APPROVED FOR STAGE 2**  
**Project:** OBIDSS — PT Prima Alat Nusantara (FY 2026)

---

## 1. Security Groups Definition

| Group XML ID | Group Technical Name | Category | Scope / Responsibilities |
|---|---|---|---|
| `group_obidss_user` | `OBIDSS / Operational User` | OBIDSS Operational BI | View Executive, Sales, Purchase & Inventory Dashboards |
| `group_obidss_sales` | `OBIDSS / Sales User` | OBIDSS Operational BI | View Sales Orders, Customer Master, & Sales Analytics |
| `group_obidss_purchase` | `OBIDSS / Purchase User` | OBIDSS Operational BI | View Purchase Orders, Vendor Master, & Procurement Analytics |
| `group_obidss_inventory` | `OBIDSS / Inventory User` | OBIDSS Operational BI | View Stock Quantities, Inventory Movements, & Transfers |
| `group_obidss_finance` | `OBIDSS / Finance User` | OBIDSS Operational BI | View Invoices, Bills, Payment Status, & Financial BI |
| `group_obidss_reviewer` | `OBIDSS / BI Reviewer` | OBIDSS Operational BI | Access Data Quality & Reconciliation Bridge |
| `group_obidss_admin` | `OBIDSS / Administrator` | OBIDSS Operational BI | Full System Configuration, Menu Restructuring, & Settings |

---

## 2. App Launcher Visibility Matrix

| Launcher Application | Operational User | Sales User | Purchase User | Inventory User | Finance User | BI Reviewer | Administrator | Technical Implementation Method |
|---|---|---|---|---|---|---|---|---|
| **Dashboards** | 🟢 Visible | 🟢 Visible | 🟢 Visible | 🟢 Visible | 🟢 Visible | 🟢 Visible | 🟢 Visible | Core Menu (`spreadsheet_dashboard`) |
| **Sales** | 🔴 Hidden | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | 🟢 Visible | Group Access Rule (`sales_team.group_sale_salesman`) |
| **Purchase** | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | 🟢 Visible | Group Access Rule (`purchase.group_purchase_user`) |
| **Inventory** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | 🔴 Hidden | 🟢 Visible | 🟢 Visible | Group Access Rule (`stock.group_stock_user`) |
| **Invoicing** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | 🟢 Visible | 🟢 Visible | Group Access Rule (`account.group_account_invoice`) |
| **Contacts** | 🔴 Hidden | 🟢 Visible | 🟢 Visible | 🔴 Hidden | 🟢 Visible | 🟢 Visible | 🟢 Visible | Group Access Rule (`base.group_partner_manager`) |
| **Discuss** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | Menu Restriction (`groups_id`) |
| **Email Marketing** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | Menu Restriction (`groups_id`) |
| **Surveys** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | Menu Restriction (`groups_id`) |
| **Employees** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | Menu Restriction (`groups_id`) |
| **Apps** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | Core Restriction (`base.group_system`) |
| **Settings** | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🔴 Hidden | 🟢 Visible | Core Restriction (`base.group_system`) |
