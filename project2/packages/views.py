from django.http.response import HttpResponse, JsonResponse
from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import permissions

from packages.models import Package
from packages.serializers import PackageSerializer, UserSerializer

# Create your views here.

class PackageList(generics.ListAPIView):
    # GET package list
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

class PackageByID(generics.RetrieveUpdateDestroyAPIView):
    # GET, PUT, DELETE packages by ID
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

@csrf_exempt
@api_view(['DELETE'])
def reset_registry(request):
    # reset registry to no packages, single admin user
    if request.method == 'DELETE':
        Package.objects.all().delete()
        User.objects.all().delete()
        try:
            User.objects.get(username='ece461defaultadminuser') # should never work since we are deleting all users
        except User.DoesNotExist:
            u = User(username='ece461defaultadminuser')
            u.set_password('correcthorsebatterystaple123(!__+@**(A')
            u.is_superuser = True
            u.is_staff = True
            u.save()
        return Response(status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer