# 02. DAX Measure Catalog

Dokumen ini berisi seluruh formula DAX (*Data Analysis Expressions*) yang digunakan di dalam Dashboard. Formula ini telah dirancang untuk mencakup perhitungan KPI, Time Intelligence, Forecast, dan Decision Logic.

> **💡 CATATAN PENTING TENTANG NAMA TABEL**: 
> Pastikan nama tabel di dalam rumus (seperti `'fact_sales'`) sama persis dengan nama tabel yang muncul di panel *Data* Power BI Anda. Jika Power BI meng-importnya menjadi `mart fact_sales` atau `fact sales`, ubahlah nama di dalam rumus dan pastikan selalu diapit tanda kutip tunggal `''` (contoh: `SUM('mart fact_sales'[revenue])`).

## A. Basic Measures (Core KPI)

**1. Total Revenue**
```dax
Total Revenue = SUM(fact_sales[revenue])
```

**2. Total Cost**
```dax
Total Cost = SUM(fact_sales[cost])
```

**3. Total Margin**
```dax
Total Margin = SUM(fact_sales[margin])
```

**4. Margin %**
```dax
Margin % = DIVIDE([Total Margin], [Total Revenue], 0)
```

**5. Total Purchase Value**
```dax
Total Purchase Value = SUM(fact_purchase[subtotal])
```

**6. Total Purchase Qty**
```dax
Total Purchase Qty = SUM(fact_purchase[quantity])
```

**7. Total Sales Qty**
```dax
Total Sales Qty = SUM(fact_sales[quantity])
```

**8. Current Inventory Value**
```dax
Inventory Value = 
CALCULATE(
    SUM(fact_inventory[value]),
    fact_inventory[movement_type] = "incoming"
) - 
CALCULATE(
    SUM(fact_inventory[value]),
    fact_inventory[movement_type] = "outgoing"
)
```

**9. Current Inventory Qty**
```dax
Inventory Qty = 
CALCULATE(
    SUM(fact_inventory[quantity]),
    fact_inventory[movement_type] = "incoming"
) - 
CALCULATE(
    SUM(fact_inventory[quantity]),
    fact_inventory[movement_type] = "outgoing"
)
```

---

## B. Time Intelligence

**1. YTD Revenue (Year-to-Date)**
```dax
YTD Revenue = TOTALYTD([Total Revenue], dim_date[full_date])
```

**2. MoM Revenue Growth (Month-over-Month)**
```dax
Previous Month Revenue = CALCULATE([Total Revenue], PREVIOUSMONTH(dim_date[full_date]))
```
```dax
MoM Revenue Growth % = DIVIDE([Total Revenue] - [Previous Month Revenue], [Previous Month Revenue], 0)
```

---

## C. Analytics & Forecast

**1. 3-Month Moving Average Demand**
```dax
3M MA Demand = 
AVERAGEX(
    DATESINPERIOD(dim_date[full_date], MAX(dim_date[full_date]), -3, MONTH),
    [Total Sales Qty]
)
```

**2. Average Lead Time (Days)**
```dax
Avg Lead Time Days = AVERAGE(fact_purchase[lead_time_days])
```

**3. Inventory Turnover Ratio (ITR)**
```dax
ITR = DIVIDE([Total Cost], [Inventory Value], 0)
```

**4. Days Inventory Outstanding (DIO)**
```dax
DIO = DIVIDE(365, [ITR], 0)
```

---

## D. Decision Measures (Prescriptive)

**1. Reorder Point (ROP)**
*Rumus: (Average Daily Sales × Average Lead Time) + Safety Stock*
```dax
Avg Daily Sales = DIVIDE([3M MA Demand], 30, 0)
```
```dax
Safety Stock = [Avg Daily Sales] * 5  // Asumsi buffer 5 hari
```
```dax
ROP = ([Avg Daily Sales] * [Avg Lead Time Days]) + [Safety Stock]
```

**2. Recommended Order Quantity**
```dax
Recommended Order = 
IF(
    [Inventory Qty] <= [ROP],
    MAX([3M MA Demand] - [Inventory Qty], 0),
    0
)
```

**3. Action Status**
```dax
Action Status = 
IF(
    [Inventory Qty] = 0, "🔴 Stockout - Urgent Order",
    IF(
        [Inventory Qty] <= [ROP], "🟡 Reorder Needed",
        IF(
            [DIO] > 90, "🔵 Overstock - Hold Order",
            "🟢 Optimal"
        )
    )
)
```

**4. Supplier Reliability Status**
```dax
Supplier Reliability = 
IF(
    [Avg Lead Time Days] > 7, "Poor (Delay Risk)",
    IF([Avg Lead Time Days] > 5, "Average", "Excellent")
)
```
