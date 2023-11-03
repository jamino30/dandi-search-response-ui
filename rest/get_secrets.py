import boto3
from botocore.exceptions import ClientError
import json
import os

def get_secrets():

    secret_name = "dandi-search-ui-env-vars"
    region_name = "us-east-1"

    session = boto3.session.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret)

    for key, value in secret_dict.items():
        print(f'{key} env var set...{value}')
        os.environ[key] = value
        try:
            print(f'{os.environ.get(key)}')
        except:
            pass
