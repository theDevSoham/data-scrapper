from typing import List, Dict, Any

# ---------- Parser ----------
class Parser:
    def parse_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        print("[Parser] Parsing raw data...")
        return raw_data