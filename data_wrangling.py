import pandas as pd
import numpy as np

def clean_airbnb_data(df):
    # --- Drop rows with missing critical values ---
    df = df.dropna(subset=["price", "latitude", "longitude", "room_type", "neighbourhood"])

    # --- Convert date ---
    df["last_review"] = pd.to_datetime(df["last_review"], errors='coerce')

    # --- Clean price ---
    df = df[df["price"] > 0]                     # Remove 0 prices
    df = df[df["price"] < 1000]                  # Cap max price for outlier removal

    # --- Normalize beds, bedrooms, baths ---
    def to_numeric_safe(val):
        try:
            return float(val)
        except:
            return np.nan

    for col in ["bedrooms", "beds", "baths", "rating"]:
        df[col] = df[col].apply(to_numeric_safe)

    # Optional: Fill missing values
    df["bedrooms"].fillna(1, inplace=True)
    df["beds"].fillna(1, inplace=True)
    df["baths"].fillna(1, inplace=True)
    df["rating"].fillna(df["rating"].median(), inplace=True)

    # --- Clean text encoding issues in 'name' ---
    df["name"] = df["name"].str.encode('latin1', errors='ignore').str.decode('utf-8', errors='ignore')

    # --- Drop unnecessary columns ---
    df.drop(columns=["id", "host_id", "license"], inplace=True, errors='ignore')

    return df


def main():
    raw_data = pd.read_csv("data/new_york_listings_2024.csv") 
    clean_data = clean_airbnb_data(raw_data)
    clean_data.to_csv("data/clean_airbnb.csv", index=False)
    print("✅ Cleaned data saved to 'data/clean_airbnb.csv'")


if __name__ == "__main__":
    main()
