import pandas as pd

# Load original dataset
df = pd.read_excel("data/Online Retail.xlsx")

# Select 1,000 random records
sample_df = df.sample(n=5000, random_state=42)

# Save the smaller dataset
sample_df.to_csv("data/online_retail_1000.csv", index=False)

print("Original dataset:", df.shape)
print("Sample dataset:", sample_df.shape)
print("Saved successfully!")