from abc import ABC, abstractmethod
from typing import Dict, Any, List

# ----- Scrapper Abstraction -----
class Scrapper(ABC):
    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]: ...
    
    @abstractmethod
    def parse_data(self, posts: List) -> None: ...