import boto3
import json

from ..utils import generate_object_key

class S3Bucket:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def put_object(self, bucket_name, data) -> None:
        json_data = json.dumps(data)

        self.s3_client.put_object(
            Bucket=bucket_name, 
            Key=generate_object_key(data["query"]), 
            Body=json_data,
            ContentType="application/json"
        )