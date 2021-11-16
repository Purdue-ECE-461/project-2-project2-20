from django.http.response import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from packages.models import Package
from packages.serializers import PackageSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def package_list(request):
    if request.method == 'GET':
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['GET'])
def package_by_id(request, pk):
    try:
        package = Package.objects.get(pk=pk)
    except Package.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PackageSerializer(package)
        return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['DELETE'])
def reset_registry(request):
    if request.method == 'DELETE':
        Package.objects.all().delete()
        return JsonResponse(status=status.HTTP_200_OK)