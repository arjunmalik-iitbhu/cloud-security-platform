from .scanner import AWSScanner
from src.constants import AWS_NAME

def fetch_resources(cloud, credential):
    if cloud != AWS_NAME:
        raise Exception(f'Cloud {cloud} is not supported')
    scanner = AWSScanner(credential)
    return scanner.get_resources()
