from transformers import pipeline
import pandas as pd
import os
from tqdm import tqdm

def classify_user_content():
    csv_path = os.path.join("data", "parsed_watch_history.csv")
    df = pd.read_csv(csv_path).dropna(subset=["Video Title"])

    print("🚀 Loading zero-shot classification model...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    candidate_labels = [
        "Music Videos", "Movie Trailers & Clips", "TV Show Clips", "Gaming", "Comedy & Roasting",
        "Vlogs", "Educational Content", "Tech Reviews & Unboxings", "Food & Cooking", "Fitness & Health",
        "Motivational Talks", "Spiritual & Devotional", "News & Current Affairs", "DIY & Crafts",
        "Beauty & Makeup Tutorials", "Fashion & Styling", "Automobile Reviews", "Travel & Exploration",
        "Product Reviews", "Finance & Investment", "Short Films & Web Series", "Dance Performances",
        "Prank Videos", "ASMR", "Language Learning", "Parenting & Childcare", "Book Reviews & Summaries",
        "Science & Technology", "History & Mythology", "Art & Painting Tutorials", "Pet Care & Training",
        "Home Organization & Cleaning", "Productivity & Time Management", "Mental Health & Well-being",
        "Language & Accent Training", "Career Guidance & Job Prep", "Photography & Videography",
        "Music Covers & Remixes", "Stand-up Comedy", "Magic & Illusion", "Horoscope & Astrology",
        "Language Translation & Subtitling", "Environmental & Nature", "Unboxing & First Impressions",
        "Virtual Reality & 360° Videos", "Live Streams & Q&A Sessions", "Behind-the-Scenes & Bloopers",
        "Language & Accent Mimicry", "Social Experiments & Challenges",
        "Documentaries & Investigative Reports"
    ]

    predicted = []
    scores = []

    print("📊 Classifying video titles...")
    for title in tqdm(df["Video Title"]):
        try:
            result = classifier(title, candidate_labels)
            predicted.append(result["labels"][0])
            scores.append(result["scores"][0])
        except Exception:
            predicted.append("Unknown")
            scores.append(0.0)

    df["Predicted Category"] = predicted
    df["Confidence Score"] = scores
    df.to_csv("data/categorized_watch_history.csv", index=False)

    summary = df["Predicted Category"].value_counts(normalize=True) * 100
    summary = summary.round(1).astype(str) + "%"
    return "User watched: " + ", ".join([f"{cat} ({pct})" for cat, pct in summary.items()])
