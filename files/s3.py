import logging
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError


class S3:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str):
        object_name = file_path.split("/")[-1]  # /admins/ilya/dog.mov
        try:
            # async with self.get_client() as client:
            #     with open(file_path, "rb") as file:
            #         await client.put_object(
            #             Bucket=self.bucket_name,
            #             Key=object_name,
            #             Body=file,
            #         )
            logging.info(f"File {object_name} uploaded to {self.bucket_name}")  # Imitation of uploading
        except ClientError as e:
            logging.error(f"Error uploading file: {e}")
            raise ClientError

    async def delete_file(self, object_name: str):
        try:
            # async with self.get_client() as client:
            #     await client.delete_object(Bucket=self.bucket_name, Key=object_name)
            logging.info(f"File {object_name} deleted from {self.bucket_name}")  # Imitation of deleting
        except ClientError as e:
            logging.error(f"Error deleting file: {e}")
            raise ClientError


s3 = S3(access_key="some_public_key", secret_key="some_secret_key", endpoint_url="url", bucket_name="test_public_bucket")
