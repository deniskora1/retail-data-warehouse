import pandas as pd
from datetime import datetime

def transform_retail(data):
    """
    #   Takes the raw data from the Online Retail.csv file and cleans them,
    #   flattens it into a clean pandas Dataframe.

        #   Cleans:
        - bad rows where "Quantity" or "UnitPrice" is <= 0 or returns errors.
        - rows where CustomerID is missing.
        - rows where "InvoiceNo", "StockCode" or "InvoiceDE" is missing

        #   Parses InvoiceDate into a datetime type.
        #   Creates new columns: full_date, year, month, day, month_name
    """
    df = data.copy()

    print("Transforming: shaping raw data into a table")
    # Renaming source columns names to align with warehouse naming convention (snake_case)
    df = df.rename(columns={ 
        "InvoiceNo":"invoice_no", 
        "StockCode":"stock_code",
        "CustomerID":"customer_id",
        "InvoiceDate":"full_date",
        "Quantity":"quantity",
        "UnitPrice":"unit_price",
        "Country":"country",
        "Description":"description"
        })
    
    # convert to numeric first — non-numeric values become NaN
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # drop rows where quantity or unit_price is <= 0
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] > 0]

    # drop rows where customer_id is missing
    df = df.dropna(subset = ["customer_id"])

    # Calculates total amount of sale by multiplying quantity bought and unit price.
    df["total_amount"] = df["quantity"] * df["unit_price"]

    # Generate date dimension attributes from the transaction date.

    df["full_date"] = pd.to_datetime(df["full_date"], format="mixed", errors="coerce")
    df = df.dropna(subset=["full_date"])
    df["full_date"] = df["full_date"].dt.normalize()

    print(df.dtypes)
    df["year"] = df["full_date"].dt.year
    df["month"] = df["full_date"].dt.month
    df["day"] = df["full_date"].dt.day
    df["day_of_week"] = df["full_date"].dt.day_name()
    df["month_name"] = df["full_date"].dt.month_name()

    # Generating date, customers and product dimensions

    dim_date = df[["full_date", "year", "month", "day", "month_name", "day_of_week"]].drop_duplicates(subset = ["full_date"])
    dim_customers = df[["customer_id", "country"]].drop_duplicates(subset = ["customer_id"])
    dim_products = df[["stock_code", "description", "unit_price"]].drop_duplicates(subset = ["stock_code"])

    # Generating fact table "fact_sales"
    fact_sales = df[["invoice_no", "stock_code", "customer_id", "full_date", "quantity", "unit_price", "total_amount"]]

    print(f"Transform complete. {len(fact_sales)} sales rows, {len(dim_customers)} customers, {len(dim_products)} products, {len(dim_date)} dates.")

    return dim_date, dim_customers, dim_products, fact_sales
    
if __name__ == "__main__":
    from extract import extract_online_retail
    df = extract_online_retail()
    dim_date, dim_customers, dim_products, fact_sales = transform_retail(df)
    print(dim_customers.head())
    print(dim_products.head())
    print(dim_date.head())
    print(fact_sales.head())
