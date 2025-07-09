# components/history_parser.py

import os
import pandas as pd
from bs4 import BeautifulSoup

class WatchHistoryParser:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        with open(self.input_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        titles = [a.text for a in soup.find_all("a") if "watch" in a.get("href", "")]
        df = pd.DataFrame({"Video Title": titles})
        df.to_csv(self.output_path, index=False)
        print(f"✅ Watch history parsed and saved to {self.output_path}")
