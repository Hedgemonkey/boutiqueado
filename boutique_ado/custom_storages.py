from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    region_name = settings.AWS_S3_REGION_NAME # Explicitly set region
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME  # Use this for clarity
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    region_name = settings.AWS_S3_REGION_NAME  # Explicitly set region
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME  # Use this for clarity
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN