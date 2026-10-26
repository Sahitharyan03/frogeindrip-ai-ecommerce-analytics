# Power BI Star Schema Data Model Specification
**Project:** Frogeindrip DTC Ecommerce Analytics & BI  
**Target Engine:** Power BI Desktop / Analysis Services Tabular / DuckDB DirectQuery  

---

## 1. Dimensional Architecture Overview

The analytical model follows a classic Kimbalesque **Star Schema**, optimized for fast aggregation, high cardinality customer slicing, and DAX time-intelligence operations.

```
       ┌────────────────────────┐         ┌────────────────────────┐
       │     dim_customers      │         │      dim_products      │
       ├────────────────────────┤         ├────────────────────────┤
       │ PK: customer_id        │         │ PK: product_id         │
       │     first_name         │         │     product_name       │
       │     last_name          │         │     category           │
       │     email              │         │     cost_price         │
       │     registered_at      │         │     retail_price       │
       │     acquisition_channel│         │     margin_pct         │
       │     state, country     │         │     is_active          │
       │     is_repeat_buyer    │         └───────────┬────────────┘
       └───────────┬────────────┘                     │
                   │ (1)                              │ (1)
                   │                                  │
                   │ (*)                              │ (*)
              ┌────┴──────────────────────────────────┴────┐
              │                 fct_sales                  │
              ├────────────────────────────────────────────┤
              │ PK: order_item_id                          │
              │ FK: order_id                               │
              │ FK: customer_id                            │
              │ FK: product_id                             │
              │ FK: date_id                                │
              │     order_timestamp                        │
              │     order_status                           │
              │     channel                                │
              │     payment_method                         │
              │     quantity                               │
              │     unit_price                             │
              │     item_gross_sales                       │
              │     item_allocated_discount                │
              │     item_net_sales                         │
              │     item_cogs                              │
              │     item_gross_profit                      │
              └────────────────────┬───────────────────────┘
                                   │ (*)
                                   │
                                   │ (1)
                      ┌────────────┴───────────┐
                      │       dim_dates        │
                      ├────────────────────────┤
                      │ PK: date_id (Date)     │
                      │     year               │
                      │     month              │
                      │     month_name         │
                      │     year_month         │
                      │     day_of_week        │
                      │     day_name           │
                      │     is_weekend         │
                      │     quarter            │
                      └────────────────────────┘
```

---

## 2. Table Cardinalities & Cross-Filter Relationships

| From Table (Dimension) | Primary Key | To Table (Fact) | Foreign Key | Cardinality | Cross-Filter Direction | Security |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_customers` | `customer_id` | `fct_sales` | `customer_id` | One-to-Many (`1:*`) | Single (`dim -> fct`) | Active |
| `dim_products` | `product_id` | `fct_sales` | `product_id` | One-to-Many (`1:*`) | Single (`dim -> fct`) | Active |
| `dim_dates` | `date_id` | `fct_sales` | `date_id` | One-to-Many (`1:*`) | Single (`dim -> fct`) | Active |

---

## 3. Storage Mode & Performance Tuning

1. **Storage Mode:** Import Mode recommended for models under 10M rows (provides ultra-low latency sub-second DAX querying via VertiPaq).
2. **Column Encoding:**
   - Integer date foreign keys (`date_id`) use Value Encoding.
   - Text IDs (`customer_id`, `product_id`) use Dictionary/Hash Encoding.
3. **Surrogate Keys:** Primary keys are strictly indexed to ensure deterministic one-to-many relationship validation in Tabular Model.
