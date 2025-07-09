import subprocess  # Allows running the preprocessing script
from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import pandas as pd
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# Load API key securely from an environment variable
api_key = ("AIzaSyCE-xqa5DXJSU8UhUXj05aqqOeYED9QyHw")
if not api_key:
    raise ValueError("ERROR: API key not found! Set YOUTUBE_API_KEY as an environment variable.")

youtube = build("youtube", "v3", developerKey=api_key)

@app.route('/store-video-id', methods=['POST'])
def store_video_id():
    try:
        video_id = request.json.get("videoId")
        if not video_id:
            return jsonify({"error": "Missing video ID"}), 400

        print(f"Received Video ID: {video_id}")

        # Check for duplicate video ID in CSV
        try:
            df = pd.read_csv("video_data.csv", encoding="utf-8", on_bad_lines="skip")
            if video_id in df["Video ID"].values:
                print(f"Video ID {video_id} already stored. Skipping entry.")
                return jsonify({"message": "Duplicate entry. Video already stored."}), 200
        except (FileNotFoundError, pd.errors.ParserError):
            print("No existing CSV file or format issue detected. Creating a new one.")

        # Fetch metadata from YouTube API
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails,status",
            id=video_id
        ).execute()

        if not response.get("items"):
            print(f"No video found for Video ID: {video_id}")
            return jsonify({"error": "Invalid video ID or no data found"}), 400

        # Extract video details
        video_info = response["items"][0]["snippet"]
        video_statistics = response["items"][0]["statistics"]
        video_content = response["items"][0]["contentDetails"]
        video_status = response["items"][0]["status"]

        video_details = {
            "Video ID": video_id,
            "Title": video_info["title"],
            "Description": video_info["description"],
            "Published At": video_info["publishedAt"],
            "Channel": video_info["channelTitle"],
            "View Count": video_statistics.get("viewCount", "N/A"),
            "Like Count": video_statistics.get("likeCount", "N/A"),
            "Comment Count": video_statistics.get("commentCount", "N/A"),
            "Duration": video_content.get("duration", "N/A"),
            "Category ID": video_info.get("categoryId", "N/A"),
            "Tags": ", ".join(video_info.get("tags", [])) if "tags" in video_info else "N/A",
            "Thumbnail URL": video_info["thumbnails"]["default"]["url"],
            "License": video_status.get("license", "N/A"),
            "Embeddable": video_status.get("embeddable", "N/A"),
            "Privacy Status": video_status.get("privacyStatus", "N/A")
        }

        # Ensure clean CSV writing
        with open("video_data.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=video_details.keys())
            if file.tell() == 0:
                writer.writeheader()

            # Remove unwanted characters (newlines, commas) before writing
            for key in video_details:
                if isinstance(video_details[key], str):
                    video_details[key] = video_details[key].replace("\n", " ").replace(",", " ")

            writer.writerow(video_details)

        print(f"Stored Video Details: {video_details}")

        # **Automatically run preprocessing script**
        print("Running preprocessing...")
        subprocess.run(["python", "preprocess.py"])

        return jsonify({"message": "Video ID stored successfully", "videoDetails": video_details})

    except Exception as e:
        print(f"Error fetching video metadata: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)