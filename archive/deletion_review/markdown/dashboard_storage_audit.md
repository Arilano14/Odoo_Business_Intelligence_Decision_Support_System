# Dashboard Storage Audit Report — Phase 11.0

**Date:** August 3, 2026  
**Project:** Odoo Business Intelligence Decision Support System (OBIDSS)

---

## 1. Storage Matrix

| Dashboard ID | Field Storage Mechanism | Linked Attachment ID | DB Column Value (`spreadsheet_dashboard`) | Filestore Attachment Exists | Attachment Size | Checksum (SHA1) | Storage Status |
|---|---|---:|---|---|---:|---|---|
| **1 (Invoicing)** | `ir.attachment` (`spreadsheet_binary_data`) | 798 | Computed via ORM | Yes | 45,546 B | `0222e9f8b0db42170340e28d059b3c883d525e50` | `ATTACHMENT_LINKED` |
| **2 (Warehouse Metrics)** | `ir.attachment` (`spreadsheet_binary_data`) | 810 | Computed via ORM | Yes | 71,550 B | `906efb5ba563ef9670ba10938b7c3eebf3613652` | `ATTACHMENT_LINKED` |
| **3 (Sales)** | `ir.attachment` (`spreadsheet_binary_data`) | 811 | Computed via ORM | Yes | 78,097 B | `bf5f679a62bcf1ee2bd83d3d245d6aafbf9cb18f` | `ATTACHMENT_LINKED` |
| **4 (Product)** | `ir.attachment` (`spreadsheet_binary_data`) | 812 | Computed via ORM | Yes | 21,269 B | `03098f10a3e6b6b3d595cc00e0d34ad23aaecd13` | `ATTACHMENT_LINKED` |

---

## 2. Forensic Metadata & Root Key Structure

- **Storage Type**: Binary data stored in `ir.attachment` (`res_model = 'spreadsheet.dashboard'`, `res_field = 'spreadsheet_binary_data'`).
- **Expected Root JSON Keys**: `version`, `sheets`, `styles`, `formats`, `pivots`, `list_views`.
- **Observation**: Attachment files are present in `ir_attachment` and filestore. The evaluation error occurs when computed ORM methods `get_readonly_dashboard()` fail to resolve relational data model filters in QWeb rendering.
