# app/services/s3_service.py
import boto3
from flask import current_app

def upload_file_to_s3(file_obj, filename):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
        region_name=current_app.config['AWS_REGION']
    )
    
    try:
        s3_client.upload_fileobj(
            file_obj,
            current_app.config['AWS_BUCKET_NAME'],
            filename
        )
        return f"s3://{current_app.config['AWS_BUCKET_NAME']}/{filename}"
    except Exception as e:
        raise Exception(f"Failed to upload file to S3: {str(e)}")