(function() {
    'use strict';

    function sendVideoId() {
        const url = new URL(window.location.href);
        const videoId = url.searchParams.get("v");

        if (videoId) {
            console.log("Detected Video ID:", videoId);

            // Send the video ID to Flask server
            fetch("http://127.0.0.1:5000/store-video-id", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ videoId: videoId })
            })
            .then(response => response.json())
            .then(data => console.log("Server Response:", data))
            .catch(error => console.error("Error sending video ID:", error));
        }
    }

    // Automatically run the function
    sendVideoId();

    // Detect video ID changes (if navigating within YouTube)
    const observer = new MutationObserver(() => {
        sendVideoId();
    });

    observer.observe(document, { childList: true, subtree: true });
})();