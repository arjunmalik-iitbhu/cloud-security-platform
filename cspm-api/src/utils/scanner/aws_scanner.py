from typing import Any
from .scanner import CloudScanner
import boto3

class AWSScanner(CloudScanner):
    @staticmethod
    def get_resources(credential: dict[str,Any]) -> dict[str,Any]:
        access_key = credential.get("access_key", None)
        secret_access_key = credential.get("secret_access_key", None)
        if not access_key or not secret_access_key:
            raise Exception("Empty access key or secret access key")
        session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )
        s3_client = session.client("s3")
        response = s3_client.list_buckets()
        buckets = [bucket for bucket in response.get("Buckets", [])]
        ec2_client = session.client("ec2")
        instances = [
            {
                "id": instance["InstanceId"],
                "state": instance["State"]["Name"],
                "type": instance["InstanceType"],
                "instance": instance
            }
            for region in ec2_client.describe_regions()["Regions"]
            for reservation in session.client("ec2", region_name=region["RegionName"]).describe_instances()["Reservations"]
            for instance in reservation["Instances"]
        ]
        return {
            "buckets": buckets,
            "instances": instances
        }
