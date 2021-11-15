from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from packages.models import Package
from packages.serializers import PackageSerializer

# Create your views here.

@csrf_exempt
def package_list(request):
    if request.method == 'GET':
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def package_by_id(request, pk):
    try:
        package = Package.objects.get(pk=pk)
    except Package.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PackageSerializer(package)
        return JsonResponse(serializer.data)