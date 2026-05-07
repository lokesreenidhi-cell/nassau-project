import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("clustered_data.csv")

# Clean dates
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df = df.dropna(subset=["Order Date", "Ship Date"])

# Lead Time
df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df = df[df["Lead Time"] >= 0]

# Encoders
product_encoder = LabelEncoder()
region_encoder = LabelEncoder()
ship_encoder = LabelEncoder()

df["Product Enc"] = product_encoder.fit_transform(df["Product Name"])
df["Region Enc"] = region_encoder.fit_transform(df["Region"])
df["Ship Enc"] = ship_encoder.fit_transform(df["Ship Mode"])

# Features
X = df[["Product Enc", "Region Enc", "Ship Enc", "Sales", "Units"]]
y = df["Lead Time"]

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# Save files
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(product_encoder, open("product_encoder.pkl", "wb"))
pickle.dump(region_encoder, open("region_encoder.pkl", "wb"))
pickle.dump(ship_encoder, open("ship_encoder.pkl", "wb"))

print("✅ Model trained successfully!")
