# Power BI Dashboard Specification & Visual Layout Guide
**Project:** Frogeindrip DTC Ecommerce Analytics & BI  
**Target Resolution:** 16:9 Canvas (1920 x 1080 px)  
**Theme Palette:** Slate Dark (#0F172A), Emerald (#10B981), Cyan (#38BDF8), Indigo (#6366F1), Light Text (#F8FAFC)  

---

## 1. Executive Overview Page (Wireframe Specification)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│  FROGEINDRIP EXECUTIVE BI OVERVIEW                  [Date Slicer: 2025-09-01 to 2026-07-31] │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬──────────────┤
│  TOTAL NET SALES  │  COMPLETED ORDERS │  AVG ORDER VALUE  │  GROSS MARGIN %   │ REPEAT GMV % │
│   $66,099.10      │       577         │     $114.56       │      64.2%        │    35.4%     │
│  [▲ 32.4% vs Tgt] │  [95% Settle Rate]│  [+$14.20 vs Ind] │  [High Fleece Mix]│ [VIP Cohorts]│
├───────────────────┴───────────────────┴───────────────────┴───────────────────┴──────────────┤
│  MONTHLY NET SALES & MARGIN TRAJECTORY (Combo Clustered Column + Secondary Line Chart)      │
│   - Primary Y-Axis (Bars): Total Net Revenue by Month ($) in Emerald                         │
│   - Secondary Y-Axis (Line): Realized Gross Margin % by Month in Cyan                        │
│   - Tooltip: Orders, Discounts, AOV, MoM Growth %                                            │
├───────────────────────────────────────────────┬──────────────────────────────────────────────┤
│  SALES CHANNEL BREAKDOWN                      │  ORDER STATUS & REFUND DISTRIBUTION          │
│   - Donut Chart: Online Store vs Pop-up POS   │   - Horizontal Clustered Bar                 │
│   - Legend: Net Revenue & Order Volume        │   - Completed, Refunded, Cancelled           │
└───────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 2. Customer Cohort & RFM Page (Wireframe Specification)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│  CUSTOMER INTELLIGENCE & RETENTION                  [Segment Slicer: All / Champions / Core] │
├───────────────────────────────────────────────┬──────────────────────────────────────────────┤
│  RFM SEGMENT VALUE TREEMAP                    │  REPEAT BUYER GMV SHARE COMPARISON           │
│   - Box Area: Total GMV per Segment ($)       │   - Gauge / KPI Card: 35.4% Point-in-Time    │
│   - Color Gradient: Average Customer Spend    │   - Stacked Bar: Repeat vs New Revenue       │
├───────────────────────────────────────────────┴──────────────────────────────────────────────┤
│  CUSTOMER COHORT RETENTION MATRIX (Matrix Visual with Conditional Formatting)                │
│   - Rows: Acquisition Month (Cohort Year-Month)                                              │
│   - Columns: Elapsed Months (Month 0, Month 1, Month 2, Month 3, Month 4)                    │
│   - Values: Active Customers & Retention Rate %                                              │
│   - Background Color Scale: Teal Heatmap (High = #10B981, Low = #1E293B)                     │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Product Profitability Page (Wireframe Specification)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│  PRODUCT PERFORMANCE & MARGIN AUDIT                [Category Filter: Hoodies / Tees / Bottoms]│
├───────────────────────────────────────────────┬──────────────────────────────────────────────┤
│  TOP REVENUE SKUs (Horizontal Bar Chart)      │  PRICE VS MARGIN MATRIX (Scatter Chart)      │
│   - Froge Heavyweight Hoodie (Forest)         │   - X-Axis: MSRP Retail Price ($)            │
│   - Froge Tactical Cargo Pants (Olive)        │   - Y-Axis: Realized Gross Margin (%)        │
│   - Froge Oversized Acid Wash Tee (Mineral)   │   - Bubble Size: Units Sold                  │
├───────────────────────────────────────────────┴──────────────────────────────────────────────┤
│  DETAILED PRODUCT CONTRIBUTION TABLE                                                         │
│   - Product Name, Category, Retail Price, Cost Price, Units, Net Sales, Profit, Realized %   │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```
