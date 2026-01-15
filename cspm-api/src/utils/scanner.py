from abc import ABC, abstractmethod
import boto3

class CloudScanner(ABC):
    @abstractmethod
    def get_resources(credential):
        pass

class AWSScanner(CloudScanner):
    def get_resources(credential):
	pass
