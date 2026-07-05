# Project Assumptions

1. **Assumption 1:** Implementasi Odoo ERP telah selesai dan data transaksi operasional sudah tersedia di database PostgreSQL.
2. **Assumption 2:** Seluruh data yang digunakan merupakan data simulasi berbasis skenario bisnis yang disusun mengikuti karakteristik perusahaan distributor alat berat.
3. **Assumption 3:** Forecast menggunakan Moving Average 3 Periode berdasarkan data historis transaksi simulasi selama 12 bulan.
4. **Assumption 4:** Power BI menggunakan Import Mode untuk mengakses Analytics Mart.
5. **Assumption 5:** User dashboard bersifat Read-Only (konsumsi informasi, bukan input data).
6. **Assumption 6:** Tidak menggunakan data rahasia perusahaan klien sesuai ketentuan NDA.
