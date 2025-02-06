# utils/management/commands/upload_to_s3.py
from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
import os


class Command(BaseCommand):  # Must inherit from BaseCommand
    help = 'Uploads static and media files to S3' # Description

    def handle(self, *args, **options):  # The main execution function
        if 'USE_AWS' in os.environ: # Check if USE_AWS is true.
            print("USE_AWS is set to True. Uploading files to S3...")  # Debug print
            try:

                s3 = boto3.client('s3')

                def upload_files(root_path, s3_location): # helper function
                    if os.path.exists(root_path):
                        for root, _, files in os.walk(root_path):
                            if files: # Only upload if files exist
                                for file in files: # Recursively uploads files in root_path, which is either static or media on the server.
                                    local_path = os.path.join(root, file)
                                    relative_path = os.path.relpath(local_path, root_path)
                                    s3_path = os.path.join(s3_location, relative_path)
                                    print(f"Uploading: {local_path} to s3://{settings.AWS_STORAGE_BUCKET_NAME}/{s3_path}") # debug print.

                                    with open(local_path, 'rb') as f:
                                        s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, s3_path)

                # Upload static files
                print("Uploading static files...")
                upload_files(settings.STATIC_ROOT, settings.STATICFILES_LOCATION)

                # Upload media files
                print("Uploading media files...")
                upload_files(settings.MEDIA_ROOT, settings.MEDIAFILES_LOCATION) # Upload media files.

                print("Static and media files uploaded to S3 successfully!")

            except Exception as e:
                print(f"S3 Upload Error: {e}") # Catch any other exceptions and handle/print here.

        else:
            print("USE_AWS is not set, skipping upload.")


