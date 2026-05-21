from extract import extract_online_retail
from transform import transform_retail
from load import load_dim_customers, load_dim_products, load_dim_date, load_fact_table, query_preview, engine

def run_pipeline():
    print("=" * 50)
    print("Starting Remotive ETL Pipeline")
    print("=" * 50)

    raw_data = extract_online_retail()

    dim_date, dim_customers, dim_products, fact_sales = transform_retail(raw_data)
    print(dim_date["full_date"].dtype)
    print(dim_date["full_date"].head())

    load_dim_customers(dim_customers, engine)
    load_dim_products(dim_products, engine)
    load_dim_date(dim_date, engine)

    load_fact_table(fact_sales, engine)

    query_preview()

    print("=" * 50)
    print("Finished Remotive ETL Pipeline succ  essfully")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()