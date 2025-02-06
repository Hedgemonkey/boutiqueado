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
            s3 = boto3.client('s3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            ) # Instantiate boto3 client

            response = s3.list_buckets() # any s3 method goes here. This one lists buckets in your s3.
            print("S3 Connection Successful. Buckets:", response['Buckets']) # Debug print: Print the value of the settings vars in Heroku to check they are correct.
            return HttpResponse("S3 Connection Test Successful") # Success response
        except Exception as e:
            print(f"S3 Connection Error: {e}")  # Catch and print any exceptions
            return HttpResponse(f"S3 Connection Test Failed: {e}", status=500)

    else:
        return HttpResponse("USE_AWS not set", status=200)


def upload_static_to_s3():
    if 'USE_AWS' in os.environ:  # Only try if USE_AWS is True
        print("USE_AWS set to True. Uploading static files to S3...")  # Debug print
        try:

            s3 = boto3.client('s3')  # No credentials needed if configured in config vars.

            # Iterate through the 'staticfiles' directory
            static_root = settings.STATIC_ROOT
            for root, _, files in os.walk(static_root):  # Use os.walk() for subdirectories
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, static_root) # gets relative path from STATIC_ROOT
                    s3_path = os.path.join(settings.STATICFILES_LOCATION, relative_path) # create full s3 path.
                    print(f"Uploading: {local_path} to s3://{settings.AWS_STORAGE_BUCKET_NAME}/{s3_path}")

                    # Upload with appropriate content type
                    # (Important for CSS, JS, images to be served correctly)
                    content_type = None # add handling for different file types here.
                    if s3_path.endswith(('.css')):
                        content_type = 'text/css'
                    elif s3_path.endswith(('.js')):
                        content_type = 'text/javascript'
                    elif s3_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')): # Images
                        content_type = 'image/' + s3_path.split('.')[-1] # Set image mimetype.

                    with open(local_path, 'rb') as f: # Read in binary mode.
                        s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, s3_path, ExtraArgs={'ContentType': content_type or 'binary/octet-stream'})

            print("Static files uploaded to S3 successfully.")
            return HttpResponse("Static Files Uploaded to S3")  # Success response.

        except Exception as e:
            print(f"S3 Upload Error: {e}")  # Print any exceptions.
            return HttpResponse(f"S3 Upload Failed: {e}", status=500)

    else:
        print("USE_AWS is not set. Skipping S3 upload.")
        return HttpResponse("USE_AWS not set", status=200)