# Power BI Enterprise DAX Measures Reference
**Project:** Frogeindrip DTC Ecommerce Analytics & BI  
**Language:** DAX (Data Analysis Expressions)  

---

## 1. Core Revenue & Volume Measures

### Total Gross Sales
```dax
[Total Gross Sales] := 
CALCULATE(
    SUM(fct_sales[item_gross_sales]),
    fct_sales[order_status] = "completed"
)
```

### Total Discounts
```dax
[Total Discounts] := 
CALCULATE(
    SUM(fct_sales[item_allocated_discount]),
    fct_sales[order_status] = "completed"
)
```

### Total Net Sales
```dax
[Total Net Sales] := 
CALCULATE(
    SUM(fct_sales[item_net_sales]),
    fct_sales[order_status] = "completed"
)
```

### Total Orders
```dax
[Total Orders] := 
CALCULATE(
    DISTINCTCOUNT(fct_sales[order_id]),
    fct_sales[order_status] = "completed"
)
```

### Average Order Value (AOV)
```dax
[Average Order Value] := 
DIVIDE(
    [Total Net Sales],
    [Total Orders],
    0.0
)
```

### Total Cost of Goods Sold (COGS)
```dax
[Total COGS] := 
CALCULATE(
    SUM(fct_sales[item_cogs]),
    fct_sales[order_status] = "completed"
)
```

### Realized Gross Profit
```dax
[Gross Profit] := 
[Total Net Sales] - [Total COGS]
```

### Realized Gross Margin %
```dax
[Gross Margin %] := 
DIVIDE(
    [Gross Profit],
    [Total Net Sales],
    0.0
)
```

---

## 2. Customer Intelligence & Repeat Buyer DAX

### Unique Purchasing Customers
```dax
[Unique Customers] := 
CALCULATE(
    DISTINCTCOUNT(fct_sales[customer_id]),
    fct_sales[order_status] = "completed"
)
```

### Repeat Customer Revenue (Lifetime Definition)
```dax
[Repeat Customer Revenue (Lifetime)] := 
CALCULATE(
    [Total Net Sales],
    dim_customers[is_repeat_buyer] = TRUE()
)
```

### Repeat Customer Share % (Lifetime)
```dax
[Repeat Customer Share % (Lifetime)] := 
DIVIDE(
    [Repeat Customer Revenue (Lifetime)],
    [Total Net Sales],
    0.0
)
```

### Point-in-Time Repeat Revenue (Strict Non-Leaking)
```dax
[Repeat Revenue (Point-in-Time)] := 
VAR CustomerOrderRank = 
    ADDCOLUMNS(
        fct_sales,
        "OrderSequence",
        CALCULATE(
            DISTINCTCOUNT(fct_sales[order_id]),
            FILTER(
                ALL(fct_sales),
                fct_sales[customer_id] = EARLIER(fct_sales[customer_id]) &&
                fct_sales[order_timestamp] <= EARLIER(fct_sales[order_timestamp]) &&
                fct_sales[order_status] = "completed"
            )
        )
    )
RETURN
    SUMX(
        FILTER(CustomerOrderRank, [OrderSequence] >= 2),
        fct_sales[item_net_sales]
    )
```

---

## 3. Time Intelligence & Growth Measures

### Prior Month Net Sales
```dax
[Prior Month Net Sales] := 
CALCULATE(
    [Total Net Sales],
    DATEADD(dim_dates[date_id], -1, MONTH)
)
```

### Month-over-Month (MoM) Net Dollar Growth
```dax
[MoM Net Growth ($)] := 
IF(
    ISBLANK([Prior Month Net Sales]),
    BLANK(),
    [Total Net Sales] - [Prior Month Net Sales]
)
```

### Month-over-Month (MoM) Growth %
```dax
[MoM Growth %] := 
DIVIDE(
    [MoM Net Growth ($)],
    [Prior Month Net Sales],
    BLANK()
)
```

### Cumulative Running Brand GMV
```dax
[Cumulative Brand GMV] := 
CALCULATE(
    [Total Net Sales],
    FILTER(
        ALLSELECTED(dim_dates),
        dim_dates[date_id] <= MAX(dim_dates[date_id])
    )
)
```
