from django.shortcuts import render
import boto3
from django.http import HttpResponse
import os
from django.conf import settings


# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

