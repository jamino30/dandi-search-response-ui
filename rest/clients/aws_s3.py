import boto3
import json
import os

from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ParamValidationError
)

from ..utils import generate_object_key

class S3Bucket:
    def __init__(self, bucket_name: str):
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", None)
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
        self.aws_default_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-2")

        self.bucket_name = bucket_name

        try:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_default_region
            )
        except (
            NoCredentialsError,
            PartialCredentialsError,
            ParamValidationError
        ) as e:
            print(e)


    def put_json_object(self, data: dict) -> None:
        json_data = json.dumps(data)

        self.s3_client.put_object(
            Bucket=self.bucket_name, 
            Key=generate_object_key(data["query"]), 
            Body=json_data,
            ContentType="application/json"
        )