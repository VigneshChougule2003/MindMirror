chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (tab.url && tab.url.includes("youtube.com/watch")) {
      const url = new URL(tab.url);
      const videoId = url.searchParams.get("v");
      console.log("Detected Video ID:", videoId);
  
      // Send the video ID to your server for analysis
      fetch("http://localhost:5000/store-video-id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ videoId: videoId })
      });
    }
  });