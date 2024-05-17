from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .tasks import my_celery_task

from app.tasks import *

import time


class MyApiView(APIView):
    def get(self, request):
        print(request.data, 'Get method ')  # {} Get method
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data, 'Post method')
        return Response(status=status.HTTP_202_ACCEPTED)
