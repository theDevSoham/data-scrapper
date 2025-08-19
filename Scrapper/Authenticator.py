from abc import ABC, abstractmethod

# ----- Scrapper Abstraction -----
class Authenticator(ABC):
    @abstractmethod
    def _authenticate(self) -> None: ...