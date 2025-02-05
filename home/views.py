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