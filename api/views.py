from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelList(APIView):
    def get(self, request):
        data = MyModel.objects.all()
        serializer = MyModelSerializer(data, many=True)
        return Response(serializer.data)


