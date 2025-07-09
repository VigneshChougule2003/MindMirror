from googleapiclient.discovery import build

# Replace with your API key
api_key = "AIzaSyCE-xqa5DXJSU8UhUXj05aqqOeYED9QyHw"
youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_runtime(video_id):
    request = youtube.videos().list(part="contentDetails", id=video_id)
    response = request.execute()
    runtime = response['items'][0]['contentDetails']['duration']
    return runtime

# Example: Fetch and print runtime for multiple video IDs
video_ids = ['VIDEO_ID1', 'VIDEO_ID2']
for video_id in video_ids:
    runtime = get_video_runtime(video_id)
    print(f"Video ID: {video_id}, Runtime: {runtime}")