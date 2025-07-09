import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.history_parser import WatchHistoryParser
from components.classifier_model import classify_user_content
from rag_module.rag_engine import analyze_psychology_from_summary

def main():
    # Step 1: Parse HTML
    input_html = "data/watch-history.html"
    parsed_csv = "data/parsed_watch_history.csv"
    print("📥 Parsing watch-history.html to structured CSV...")
    parser = WatchHistoryParser(input_path=input_html, output_path=parsed_csv)
    parser.run()

    # Step 2: Classify user content
    print("🧠 Generating user behavior summary...")
    user_summary = classify_user_content()
    print(f"\n📊 Behavior Summary:\n{user_summary}\n")

    # Step 3: RAG Psychological Analysis
    print("🔍 Analyzing mental state using Gemini...")
    rag_result = analyze_psychology_from_summary(user_summary)
    print(f"\n🧾 Final Psychological Analysis:\n{rag_result}\n")

    # Step 4: Save to output
    os.makedirs("output", exist_ok=True)
    with open("output/psych_analysis.txt", "w") as f:
        f.write("Behavior Summary:\n" + user_summary + "\n\n")
        f.write("Psychological Analysis:\n" + rag_result)
    print("✅ Output saved to output/psych_analysis.txt")

if __name__ == "__main__":
    main()
