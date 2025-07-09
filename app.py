# app.py (streamlined from midpoint)
from components.generate_summary import generate_user_summary
from rag_module.rag_engine import analyze_psychology_from_summary
import logging
import os
import json

logging.getLogger("transformers").setLevel(logging.ERROR)

def main():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "summary.json")
    result_path = os.path.join(output_dir, "psych_analysis.txt")

    print("\n📝 Generating user behavior summary from categorized watch history...")
    user_summary = generate_user_summary("data/categorized_watch_history.csv")
    print(f"\n🧠 Behavior Summary:\n{user_summary}\n")

    # Save summary for frontend chart
    summary_dict = {}
    try:
        items = user_summary.replace("User watched: ", "").split(", ")
        for item in items:
            label, percent = item.split(" (")
            summary_dict[label.strip()] = float(percent.replace("%)", ""))
        with open(summary_path, "w") as sf:
            json.dump(summary_dict, sf)
    except Exception as e:
        print("⚠️  Could not save summary.json:", e)

    print("🔍 Running psychological insight analysis using RAG model...")
    rag_result = analyze_psychology_from_summary(user_summary)
    print(f"\n🧾 Final Psychological Analysis:\n{rag_result}")

    # Save analysis output
    with open(result_path, "w", encoding="utf-8") as f:
        f.write("Behavior Summary:\n" + user_summary + "\n\n")
        f.write("Psychological Analysis:\n" + rag_result + "\n")

if __name__ == "__main__":
    main()
