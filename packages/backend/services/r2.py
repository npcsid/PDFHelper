import boto3
from botocore.config import Config
from backend.config import (
    CF_ACCOUNT_ID,
    R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY,
    R2_BUCKET_NAME,
    R2_PUBLIC_URL
)
import uuid
from datetime import datetime

def get_r2_client():
    """
    Create and return a boto3 S3 client configured for Cloudflare R2.
    """
    return boto3.client(
        's3',
        endpoint_url=f'https://{CF_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        config=Config(
            signature_version='s3v4',
            retries={'max_attempts': 3}
        )
    )

def upload_to_r2(file_bytes: bytes, original_filename: str, content_type: str = "application/pdf") -> dict:
    """
    Upload a file to R2 and return the file info.
    
    Args:
        file_bytes: The file content as bytes
        original_filename: Original name of the file
        content_type: MIME type of the file
        
    Returns:
        dict with r2_key, r2_url, and file_size
    """
    client = get_r2_client()
    
    timestamp = datetime.utcnow().strftime('%Y/%m/%d')
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = original_filename.replace(' ', '_')
    r2_key = f"uploads/{timestamp}/{unique_id}_{safe_filename}"
    
    # Upload to R2
    client.put_object(
        Bucket=R2_BUCKET_NAME,
        Key=r2_key,
        Body=file_bytes,
        ContentType=content_type
    )
    
    # Generate URL
    if R2_PUBLIC_URL:
        r2_url = f"{R2_PUBLIC_URL.rstrip('/')}/{r2_key}"
    else:
        # Generate a presigned URL valid for 7 days
        r2_url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': R2_BUCKET_NAME, 'Key': r2_key},
            ExpiresIn=604800  # 7 days
        )
    
    return {
        "r2_key": r2_key,
        "r2_url": r2_url,
        "file_size": len(file_bytes)
    }

def get_r2_url(r2_key: str, expires_in: int = 3600) -> str:
    """
    Generate a presigned URL for accessing a file in R2.
    
    Args:
        r2_key: The key/path of the file in R2
        expires_in: URL expiration time in seconds (default 1 hour)
        
    Returns:
        Presigned URL string
    """
    if R2_PUBLIC_URL:
        return f"{R2_PUBLIC_URL.rstrip('/')}/{r2_key}"
    
    client = get_r2_client()
    return client.generate_presigned_url(
        'get_object',
        Params={'Bucket': R2_BUCKET_NAME, 'Key': r2_key},
        ExpiresIn=expires_in
    )

def download_from_r2(r2_key: str) -> bytes:
    """
    Download a file from R2.
    
    Args:
        r2_key: The key/path of the file in R2
        
    Returns:
        File content as bytes
    """
    client = get_r2_client()
    response = client.get_object(Bucket=R2_BUCKET_NAME, Key=r2_key)
    return response['Body'].read()

def delete_from_r2(r2_key: str) -> bool:
    """
    Delete a file from R2.
    
    Args:
        r2_key: The key/path of the file in R2
        
    Returns:
        True if successful
    """
    client = get_r2_client()
    client.delete_object(Bucket=R2_BUCKET_NAME, Key=r2_key)
    return True
