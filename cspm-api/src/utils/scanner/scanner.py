from typing import Any
from abc import ABC, abstractmethod

class CloudScanner(ABC):
    @abstractmethod
    @staticmethod
    def get_resources(credential: dict[str,Any]) -> dict[str,Any]:
        pass
