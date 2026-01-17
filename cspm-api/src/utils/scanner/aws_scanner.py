from typing import Any
from .scanner import CloudScanner
import boto3
import json
from src.model.entity import Resource
from src.constants import RESOURCE_TYPE_S3, RESOURCE_TYPE_EC2


def get_value_or_default(func, default, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return default


class AWSScanner(CloudScanner):
    @staticmethod
    def get_resources(cloud_id: int, credential: dict[str, Any]) -> list[Resource]:
        access_key = credential.get("access_key", None)
        secret_access_key = credential.get("secret_access_key", None)
        region = credential.get("region", "us-east-1")
        if not access_key or not secret_access_key:
            raise Exception("Empty access key or secret access key")
        session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region,
        )
        s3_client = session.client(RESOURCE_TYPE_S3)
        response = s3_client.list_buckets()
        buckets = [
            Resource(
                type=RESOURCE_TYPE_S3,
                details=json.dumps(
                    {
                        **bucket,
                        **get_value_or_default(
                            s3_client.get_bucket_encryption, {}, Bucket=bucket["Name"]
                        ),
                        **get_value_or_default(
                            s3_client.get_bucket_policy_status,
                            {},
                            Bucket=bucket["Name"],
                        ),
                        **get_value_or_default(
                            s3_client.get_bucket_logging, {}, Bucket=bucket["Name"]
                        ),
                        **{
                            "Versioning": get_value_or_default(
                                s3_client.get_bucket_versioning,
                                {},
                                Bucket=bucket["Name"],
                            )
                        },
                    },
                    default=str,
                ),
                cloud_id=cloud_id,
                external_resource_id=bucket["BucketArn"],
            )
            for bucket in response.get("Buckets", [])
        ]
        ec2_client = session.client(RESOURCE_TYPE_EC2)
        instances = [
            Resource(
                type=RESOURCE_TYPE_EC2,
                details=json.dumps(instance, default=str),
                cloud_id=cloud_id,
                external_resource_id=instance["InstanceId"],
            )
            for region in ec2_client.describe_regions()["Regions"]
            for reservation in session.client(
                RESOURCE_TYPE_EC2, region_name=region["RegionName"]
            ).describe_instances()["Reservations"]
            for instance in reservation["Instances"]
        ]
        return [*buckets[:], *instances[:]]
