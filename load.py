import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))

DIM_CUSTOMERS = "dim_customers"
DIM_PRODUCTS = "dim_products"
DIM_DATE = "dim_date"
FACT_SALES = "fact_sales"

def load_dim_customers(df, engine):
    try:
        existing_customers = pd.read_sql(f"SELECT customer_id FROM {DIM_CUSTOMERS}", engine)["customer_id"].tolist()
    except Exception:
        existing_customers = []

    new_customers = df[~df["customer_id"].isin(existing_customers)]

    if len(new_customers) > 0:
        new_customers.to_sql(
            name="dim_customers",
            con=engine,
            if_exists="append",
            index=False
            )
    
    print(f"Loaded dim_customers — {len(new_customers)} new rows.")

def load_dim_products(df, engine):
    try:
        existing_products = pd.read_sql(f"SELECT stock_code FROM {DIM_PRODUCTS}", engine)["stock_code"].tolist()
    except Exception:
        existing_products = []

    new_products = df[~df["stock_code"].isin(existing_products)]

    if len(new_products) > 0:
        new_products.to_sql(
            name="dim_products",
            con=engine,
            if_exists="append",
            index=False
            )
    print(f"Loaded dim_products — {len(new_products)} new rows.")

def load_dim_date(dim_date, engine):
    try:
        existing_dates = pd.read_sql(f"SELECT full_date FROM {DIM_DATE}", engine)["full_date"].tolist()
        existing_dates = [str(d)[:10] for d in existing_dates]
    except Exception:
        existing_dates = []

    dim_date = dim_date.copy()
    dim_date["full_date"] = dim_date["full_date"].astype(str).str[:10]

    new_dates = dim_date[~dim_date["full_date"].isin(existing_dates)]

    if len(new_dates) > 0:
        new_dates.to_sql(
            name="dim_date",
            con=engine,
            if_exists="append",
            index=False
        )
    print(f"Loaded dim_date — {len(new_dates)} new rows.")

def load_fact_table(df, engine):

    # ON CONFLICT DO NOTHING approach. 

    def _skip_on_conflict(table, conn, keys, data_iter):
        rows = [dict(zip(keys, row)) for row in data_iter]
        stmt = pg_insert(table.table).values(rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=["invoice_no", "stock_code"])
        conn.execute(stmt)

    if len(df) > 0:
        df.to_sql(
            name="fact_sales",
            con=engine,
            if_exists="append",
            index=False,
            method=_skip_on_conflict 
            )

    print(f"Loaded fact_sales — {len(df)} rows attempted (duplicates skipped).")


def query_preview():
    preview_df = pd.read_sql("""
        SELECT 
            f.invoice_no,
            c.country,
            f.total_amount,
            d.month_name,
            d.year
        FROM fact_sales f
        JOIN dim_customers c ON f.customer_id = c.customer_id
        JOIN dim_date d ON f.full_date = d.full_date
        LIMIT 5
    """, engine)
    print("\nPreview of latest sales:")
    print(preview_df.to_string(index=False))