from typing import List, Dict, Any

# ---------- Storage Gateway ----------
class StorageGateway:
    def store(self, normalized_data: List[Dict[str, Any]]) -> None:
        print(f"[StorageGateway] Storing data: {normalized_data}")