from django.http.response import HttpResponse, JsonResponse
from django.http import Http404
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework import permissions
from packages.rate import *

from packages.models import Package
from packages.serializers import PackageSerializer, UserSerializer, RatingSerializer

# Create your views here.

class PackageList(generics.ListAPIView):
    # GET package list
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     return Package.objects.all().filter(owner=user)


class PackageByID(generics.RetrieveUpdateDestroyAPIView):
    # GET, PUT, DELETE packages by ID
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

    def perform_update(self, serializer):
        # PUT only if ingestible package
        if check_trust(get_rating(serializer.validated_data['url'])):
            serializer.save()


class CreatePackage(generics.CreateAPIView):
    # POST package
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PackageSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


@csrf_exempt
@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def rate_package(request, pk):
    # GET rating of package with specified ID
    try:
        p = Package.objects.get(pk=pk)
    except Package.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        package_url = p.url
        ratings = get_rating(package_url)
        serialized_data = RatingSerializer(data={'BusFactor': ratings[0], 'Correctness': ratings[1], 'RampUp': ratings[2], 'ResponsiveMaintainer': ratings[3], 'LicenseScore': ratings[4], 'GoodPinningPractice': ratings[5]})
        serialized_data.is_valid()
        return Response(data=serialized_data.data)


class PackageByName(generics.RetrieveDestroyAPIView):
    # GET, DELETE packages by name
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    lookup_field = 'name'


@csrf_exempt
@api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
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

@api_view(['PUT'])
def authenticate(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

class UserList(generics.ListCreateAPIView):
    # GET list of all users
    # permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # GET detail of a singular user
    # permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer