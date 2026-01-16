from typing import Any
from abc import ABC, abstractmethod
from src.model.entity import Resource

class CloudScanner(ABC):
    @abstractmethod
    @staticmethod
    def get_resources(cloud_id: int, credential: dict[str,Any]) -> list[Resource]:
        pass
