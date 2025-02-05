from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    def _save(self, name, content):
        print(f"Saving static file: {name}") # Debug print
        print(f'Bucket Name: {self.bucket_name}') # Debug print
        print(f'Region: {self.region_name}') # Debug print
        return super()._save(name, content)


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def _save(self, name, content):
        print(f"Saving media file: {name}")  # Debug print
        print(f'Bucket Name: {self.bucket_name}') # Debug print
        print(f'Region: {self.region_name}') # Debug print
        return super()._save(name, content)
