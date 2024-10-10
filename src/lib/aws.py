"""Module for interacting with AWS S3."""

import logging
import os
from pathlib import Path

import boto3
import boto3.exceptions
import boto3.session
import dotenv
from mypy_boto3_s3 import S3Client

dotenv.load_dotenv()

DEFAULT_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "my-bucket")


def initialize_s3_client() -> S3Client:
    """Initialize and return an S3 client using environment variables for AWS credentials."""
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        error_message = "AWS credentials are not set in environment variables"
        raise OSError(error_message)

    logging.debug("Initializing S3 client with region: %s", region)

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region,
    )


def upload_file_to_s3(file_path: Path, bucket_name: str = DEFAULT_BUCKET_NAME, target_dir: str = "") -> None:
    """Upload a file to an S3 bucket at the specified target directory.

    Args:
        file_path (Path): The path to the file to upload.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to DEFAULT_BUCKET_NAME.
        target_dir (str, optional): The target directory within the bucket. Defaults to "".

    """
    if not file_path.exists() or not file_path.is_file():
        error_message = f"File {file_path} does not exist or is not a valid file"
        raise FileNotFoundError(error_message)

    logging.debug(
        "Preparing to upload file: %s to bucket: %s, target directory: %s",
        file_path,
        bucket_name,
        target_dir,
    )

    s3_client = initialize_s3_client()
    target_path = f"{target_dir}/{file_path.name}" if target_dir else file_path.name

    s3_client.upload_file(str(file_path), bucket_name, target_path)
    logging.debug("File %s uploaded successfully to %s in bucket %s", file_path.name, target_path, bucket_name)
