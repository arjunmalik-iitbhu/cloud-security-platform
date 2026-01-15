from abc import ABC, abstractmethod

class CloudScanner(ABC):
    @abstractmethod
    def get_resources(credential):
        pass
