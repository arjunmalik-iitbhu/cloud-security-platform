from .scanner import AWSScanner
from src.constants import AWS_NAME
from src.model.entity import Resource

def fetch_resources(cloud_id: int, cloud_name:str, credential: dict[str,Any]) -> list[Resource]:
    if cloud_name != AWS_NAME:
        raise Exception(f'Cloud {cloud_name} is not supported')
    scanner = AWSScanner()
    return scanner.get_resources(cloud_id, credential)
