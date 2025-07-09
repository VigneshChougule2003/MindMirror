# rag_module/rag_engine.py
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file and configure Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def analyze_psychology_from_summary(summary_text: str):
    # Reduce summary to top 8 categories
    try:
        percentages = pd.Series({
            item.split(" (")[0]: float(item.split("(")[1].replace("%)", ""))
            for item in summary_text.replace("User watched: ", "").split(", ")
        })
        top8 = percentages.sort_values(ascending=False).head(8)
        formatted_list = "\n".join([f"{i+1}. {k} ({v:.1f}%)" for i, (k, v) in enumerate(top8.items())])
    except:
        formatted_list = summary_text

    # Prompt for Gemini model
    prompt = (
        "You are a psychologist analyzing a user's YouTube viewing behavior.\n"
        f"The user's top 8 content categories are:\n{formatted_list}\n\n"
        "Write a fluent and detailed paragraph interpreting their emotional state, mental health, curiosity, attention span, and behavioral patterns.\n"
        "Avoid listing categories. Respond empathetically with psychological insight."
    )

    # Use Gemini Pro to generate the insight
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()