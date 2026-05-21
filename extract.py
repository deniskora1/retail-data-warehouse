import pandas as pd

#Extracting RAW data from the online retail data CSV


def extract_online_retail():
    print("Extracting: reading Online Retail.csv")
    df = None
    try:
        df = pd.read_csv("data/raw/Online Retail.csv", sep=";")
        print(f"Extraction complete. Got {len(df)} rows.")
    except FileNotFoundError:
        print("File not found. Check the path variable and file name.")
    return df

if __name__ == "__main__":
    data = extract_online_retail()
    if data is not None: print(data.head(3).to_string())
    else: print("Data is None.")
