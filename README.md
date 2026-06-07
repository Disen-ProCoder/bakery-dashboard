# Bakery Business Intelligence Dashboard

A complete data pipeline and analytics dashboard for a bakery business — built with PostgreSQL, Python, and Metabase. Tracks revenue, products, customers, sales trends, waste, and profitability with automated hourly data refresh.

## Overview

This project takes raw CSV data (products, customers, orders, order items, inventory), loads it into a PostgreSQL database through a Python ETL pipeline, and visualizes it through 6 interactive dashboards built in Metabase.

## Tech Stack

- **Database:** PostgreSQL
- **ETL:** Python (pandas, psycopg2)
- **Visualization:** Metabase
- **Automation:** Windows Task Scheduler

## Architecture

```
CSV Files  →  Python ETL Script  →  PostgreSQL Database  →  Metabase Dashboards
(bakery_data)   (etl_script.py)        (bakery_db)          (localhost:3000)
```

## Database Schema

Five relational tables:

- **products** — product catalog with cost, pricing, shelf life, and capacity
- **customers** — customer profiles with contact info and signup source
- **orders** — order-level transactions with totals, fees, and status
- **order_items** — line items per order (quantity, unit price, line total)
- **inventory** — daily stock levels, units sold, and waste per product

## ETL Pipeline

`etl_script.py` connects to PostgreSQL, reads each CSV from `bakery_data/`, clears existing records, and bulk-inserts fresh data — keeping the database in sync with the source files.

To run it manually:

```bash
python etl_script.py
```

## Dashboards

Built in Metabase, connected directly to `bakery_db`:

1. **Overview** — total revenue, total orders, revenue trend, orders by status
2. **Product Performance** — revenue by product/category, top sellers, waste by product
3. **Customer Insights** — customers by source/city, total customers, top customers by orders
4. **Sales Trends** — daily revenue trend, orders by day of week/hour, monthly revenue
5. **Waste Management** — waste by product, wasted vs sold, waste over time, total units wasted
6. **Profitability** — total revenue, revenue by customer, total discounts, revenue vs discount trend, total delivery fees

## Automation

A scheduled Windows Task runs `etl_script.py` every hour to refresh the database, and Metabase syncs with the database on its own hourly schedule — keeping all dashboards up to date automatically.

## Setup

1. Create the PostgreSQL database and tables (see SQL schema)
2. Place CSV files in `bakery_data/`
3. Update `CSV_FOLDER`, `DB_PASSWORD` in `etl_script.py` to match your environment
4. Run `python etl_script.py` to load data
5. Connect Metabase to `bakery_db` and build/import the dashboards

## Adding New Data

- Append new rows to the CSV files in `bakery_data/` and re-run `etl_script.py`, or
- Insert records directly into PostgreSQL via SQL `INSERT` statements
