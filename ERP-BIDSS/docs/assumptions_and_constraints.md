# Assumptions & Constraints

## Assumptions
1. Implementasi ERP Odoo 18 telah berhasil dilakukan dan data transaksi tersedia.
2. Data simulasi merepresentasikan pola transaksi perusahaan distributor alat berat selama 12 bulan operasional.
3. Power BI menggunakan Import Mode (bukan DirectQuery) untuk performa optimal.
4. User dashboard bersifat Read-Only.
5. Moving Average 3 Periode cukup memadai untuk forecasting operasional pada skala MVP.

## Constraints

### In Scope
- [x] Odoo 18 Community Edition
- [x] PostgreSQL
- [x] Python (Pandas, SQLAlchemy, NumPy)
- [x] Power BI (Import Mode)

### Out of Scope
- [ ] Real-time streaming
- [ ] Big Data (Hadoop, Spark, Kafka)
- [ ] Deep Learning
- [ ] Multi-company ERP
- [ ] Distributed Database
- [ ] Custom Odoo Module Development
- [ ] Cloud deployment
