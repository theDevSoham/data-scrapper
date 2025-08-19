from Scrapper import Scrapper
from utils import Parser, Normalizer, StorageGateway
from typing import List

# ---------- Orchestrator ----------
class Orchestrator:
    def __init__(self, scrappers: List[Scrapper], parser: Parser, normalizer: Normalizer, storage_gateway: StorageGateway):
        self.scrappers = scrappers
        self.parser = parser
        self.normalizer = normalizer
        self.storage_gateway = storage_gateway

    def run(self):
        print("[Orchestrator] Starting scraping workflow...")
        for scrapper in self.scrappers:
            print(f"[Orchestrator] Using {scrapper.__class__.__name__}...")
            raw_data = scrapper.fetch_data()
            parsed = self.parser.parse_data(raw_data)
            normalized = self.normalizer.normalize(parsed)
            self.storage_gateway.store(normalized)
        print("[Orchestrator] Workflow complete!")