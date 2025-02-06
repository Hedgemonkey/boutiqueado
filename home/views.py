from django.shortcuts import render
import boto3
from django.http import HttpResponse
import os
from django.conf import settings


# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def test_s3_connection(request):  # Create a test view (add to urls.py)

    if 'USE_AWS' in os.environ:

        try:
            s3 = boto3.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )  # Instantiate boto3 client

            response = s3.list_buckets()  # any s3 method goes here. This one\
            # lists buckets in your s3.
            print("S3 Connection Successful. Buckets:", response['Buckets'])  # Debug print: Print the value of the settings vars in Heroku to check they are correct.
            return HttpResponse("S3 Connection Test Successful")  # Success response
        except Exception as e:
            print(f"S3 Connection Error: {e}")  # Catch and print any exceptions
            return HttpResponse(f"S3 Connection Test Failed: {e}", status=500)

    else:
        return HttpResponse("USE_AWS not set", status=200)


def upload_static_to_s3(request):
    if 'USE_AWS' in os.environ:
        print('USE_AWS is True')

        try:
            s3 = boto3.client('s3')

            def upload_files(root_path, s3_location): # helper function for both static and media files
                if os.path.exists(root_path): # check directory exists
                    for root, _, files in os.walk(root_path): # upload subdirectories too
                        for file in files:
                            local_path = os.path.join(root, file)
                            relative_path = os.path.relpath(local_path, root_path)
                            s3_path = os.path.join(s3_location, relative_path) # gets correct path to file for s3

                            print(f"Uploading: {local_path} to s3://{settings.AWS_STORAGE_BUCKET_NAME}/{s3_path}") # debug print


                            with open(local_path, 'rb') as f:
                                s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, s3_path)  # Simpler upload

            # Static files
            print("Uploading static files...")
            upload_files(settings.STATIC_ROOT, settings.STATICFILES_LOCATION) # uses helper function.

            # Media files
            print("Uploading media files...")
            upload_files(settings.MEDIA_ROOT, settings.MEDIAFILES_LOCATION)  # Call for media files
            print('Media files uploaded') # check if method was called for uploading media files

            return HttpResponse("Static and Media Files Uploaded to S3")

        except Exception as e:
            print(f"S3 Upload Error: {e}")
            return HttpResponse(f"S3 Upload Failed: {e}", status=500)
    else:
        print('USE_AWS is not True')
        return HttpResponse("USE_AWS not set", status=200)
