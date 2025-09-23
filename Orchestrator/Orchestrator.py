from Scrapper import Scrapper
from typing import List

# ---------- Orchestrator ----------
class Orchestrator:
    def __init__(self, scrappers: List[Scrapper]):
        self.scrappers = scrappers

    def run(self):
        print("[Orchestrator] Starting scraping workflow...")
        for scrapper in self.scrappers:
            print(f"[Orchestrator] Using {scrapper.__class__.__name__}...")
            raw_data = scrapper.fetch_data()
            print(f"[Orchestrator] Received raw data of length {len(raw_data)}")
            scrapper.parse_data(raw_data)
        print("[Orchestrator] Workflow complete!")