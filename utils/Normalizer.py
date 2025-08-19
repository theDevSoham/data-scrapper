from typing import List, Dict, Any

# ---------- Normalizer ----------
class Normalizer:
    def normalize(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        print("[Normalizer] Normalizing parsed data...")
        return parsed_data