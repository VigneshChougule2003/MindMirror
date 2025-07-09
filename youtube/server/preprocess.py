import pandas as pd

# Load the existing cleaned CSV file (or create a new one if missing)
try:
    cleaned_df = pd.read_csv("cleaned_video_data.csv", encoding="utf-8", on_bad_lines="skip")
except FileNotFoundError:
    cleaned_df = pd.DataFrame()  # Create an empty dataframe if no file exists

# Load the new raw video data from `video_data.csv`
raw_df = pd.read_csv("video_data.csv", encoding="utf-8", on_bad_lines="skip")

# Handle missing values
raw_df.fillna("Unknown", inplace=True)
raw_df.dropna(subset=["Video ID"], inplace=True)

# Remove duplicates (including existing ones in `cleaned_video_data.csv`)
if not cleaned_df.empty:
    combined_df = pd.concat([cleaned_df, raw_df], ignore_index=True)
    combined_df.drop_duplicates(subset=["Video ID"], keep="first", inplace=True)
else:
    combined_df = raw_df.drop_duplicates(subset=["Video ID"], keep="first")

# Ensure text columns exist before cleaning
text_columns = ["Title", "Description", "Tags", "Channel"]
for column in text_columns:
    if column in combined_df.columns:
        combined_df.loc[:, column] = combined_df[column].astype(str).str.replace("\n", " ").str.replace(",", " ")

# Convert numeric columns safely
numeric_columns = ["View Count", "Like Count", "Comment Count"]
for column in numeric_columns:
    if column in combined_df.columns:
        combined_df.loc[:, column] = pd.to_numeric(combined_df[column], errors="coerce").fillna(0).astype(int)

# Save the updated cleaned dataset
combined_df.to_csv("cleaned_video_data.csv", index=False, encoding="utf-8")

print("✅ Cleaned and updated CSV file saved successfully.")