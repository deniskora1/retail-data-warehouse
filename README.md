# Online Retail Data Warehouse
 
End-to-end data warehouse project featuring star schema design, dimensional modeling, and a Python ETL pipeline.

## Table of Contents
 
- [Summary](#background)
- [Install](#install)
- [Usage](#usage)


# Summary 

Transforms the [UCI Online Retail dataset](https://archive.ics.uci.edu/ml/datasets/online+retail) into a structured data warehouse. 
Covers the full pipeline from raw CSV ingestion to a star schema.

## Install
 
**1. Clone the repo**
```bash
git clone https://github.com/yourusername/online-retail-dwh.git
cd online-retail-dwh
```
 
**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
**4. Set up environment variables**
```bash
cp .env.example .env
```
Open `.env` and fill in your database connection string:
```
DB_URL=postgresql://user:password@localhost:5432/your_db
```
 
**5. Download the dataset**
 
Download `Online Retail.csv` from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail) and place it in the project root.
 
**To uninstall:**
```bash
deactivate
cd ..
rm -rf online-retail-dwh
```
 
To drop the warehouse tables from your database:
```sql
DROP TABLE IF EXISTS fact_sales, dim_customers, dim_products, dim_date;
```

## Usage
 
Run the full ETL pipeline:
 
```bash
python pipeline.py
```


