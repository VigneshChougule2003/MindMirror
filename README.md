# 🧠 MindMirror: YouTube Watch History Analyzer

MindMirror is a smart tool designed to analyze a user's YouTube watch history and generate insights related to mental health, psychology, and digital behavior patterns. It uses machine learning, psychological models, and Retrieval-Augmented Generation (RAG) techniques to process YouTube data and deliver meaningful analysis.

---

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Usage](#-usage)
- [Tech Stack](#-tech-stack)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features
- ✅ Parse YouTube Watch History (HTML Export)
- ✅ Video Content Classification with ML Models
- ✅ Generate Psychological & Behavioral Summaries
- ✅ Retrieval-Augmented Generation (RAG) Analysis using PDF Documents
- ✅ Clean & Minimal Web Dashboard Interface
- ✅ Optional Browser Extension for Data Collection

---

## 📂 Project Structure
```
MindMirror/
│
├── .env                               # Environment variables (API keys, configs)
├── requirements.txt                   # Python dependencies
│
├── app.py                             # Main backend application
├── api.py                             # API endpoints (part 1)
├── api2.py                            # API endpoints (part 2)
├── main.py                            # App runner
│
├── components/                        # Core components
│   ├── classifier_model.py            # Machine Learning classifier
│   ├── generate_summary.py            # Generates text summaries
│   ├── history_parser.py              # Parses YouTube watch history
│   ├── run_rag.py                     # Runs Retrieval-Augmented Generation
│   └── __init__.py
│
├── rag_module/                        # Retrieval-Augmented Generation module
│   └── rag_engine.py
│
├── data/                              # Sample data & resources
│   ├── The Shallows.pdf               # Reference PDF for RAG
│   └── watch-history.html             # Sample YouTube Watch History export
│
├── frontend/                          # Web Frontend (UI)
│   ├── index.html                     # Main Dashboard Page
│   ├── index2.html                    # Alternative UI (optional)
│   ├── script.js                      # Main JavaScript functionality
│   ├── script2.js                     # Alternative JavaScript (optional)
│   └── style.css                      # Styling (CSS)
│
└── youtube/                           # YouTube Tools
    ├── extension/                     # Chrome Extension
    │   ├── background.js
    │   ├── content.js
    │   └── manifest.json
    │
    └── server/                        # Backend server for YouTube data
        ├── cleaned_video_data.csv
        ├── preprocess.py
        ├── runtime_analysis.py
        ├── server.py
        └── video_data.csv
```

---

## 🛠️ Setup & Installation

### 1. Clone Repository:
```bash
git clone https://github.com/VigneshChougule2003/MindMirror.git
cd MindMirror
```

### 2. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 3. Setup `.env`:
Create `.env` file to store API keys, secrets, or config:
```bash
# Example .env content
API_KEY=your_api_key_here
```

### 4. Run the App:
```bash
python app.py
```

---

## 🚀 Usage
1. Export your YouTube watch history from Google Takeout.
2. Upload the `watch-history.html` file via the web dashboard.
3. The app will:
   - Parse your history.
   - Classify the videos.
   - Summarize your behavior.
   - Run RAG-based analysis (if enabled).
4. View results and download reports (if available).

---

## 🧰 Tech Stack
| Category      | Tech Used                        |
|---------------|---------------------------------|
| Language      | Python 3.x                       |
| Backend       | Flask / FastAPI                  |
| Machine Learning | Custom Classifier Models    |
| Frontend      | HTML, JavaScript, CSS            |
| Data Parsing  | BeautifulSoup, Pandas            |
| RAG / NLP     | Langchain, PDF Parsing Modules   |
| Chrome Ext    | JavaScript, Manifest V3          |

---

## 📄 License
This project is licensed under the **MIT License** — feel free to modify and use it as needed.

---

## 📬 Contact
**Developer:** [Vignesh Chougule](https://github.com/VigneshChougule2003)

For issues or contributions, open an [issue](https://github.com/VigneshChougule2003/MindMirror/issues) or submit a pull request.

---

> ⚠️ **Disclaimer:**  
This project is for research and educational purposes only. It is not intended for clinical or medical use.

---
