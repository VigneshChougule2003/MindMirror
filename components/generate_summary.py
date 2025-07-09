import pandas as pd

def generate_user_summary(csv_path="data/categorized_watch_history.csv"):
    try:
        df = pd.read_csv(csv_path)

        if "Predicted Category" not in df.columns:
            return "❌ Error: 'Predicted Category' column not found in CSV."

        percentages = df['Predicted Category'].value_counts(normalize=True) * 100
        summary_parts = [f"{cat} ({pct:.1f}%)" for cat, pct in percentages.items()]
        summary = "User watched: " + ", ".join(summary_parts)

        return summary

    except FileNotFoundError:
        return f"❌ Error: File not found at {csv_path}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"
