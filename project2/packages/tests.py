from django.test import TestCase
from packages.models import Package
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

# Create your tests here.

class PackageTestCase(TestCase):
    def setUp(self):
        u = User(username='ece461defaultadminuser')
        u.set_password('correcthorsebatterystaple123(!__+@**(A')
        u.is_superuser = True
        u.is_staff = True
        u.save()
        Package.objects.create(name='lodash', version='4.0.0', url='https://github.com/lodash/lodash', owner=u)
        Package.objects.create(name='jQuery', version='3.6.0', url='https://github.com/jquery/jquery', owner=u)

    def test_num_packages(self):
        packages = list(Package.objects.all())
        self.assertEqual(len(packages), 2)

    def test_package_id(self):
        lodash_package = Package.objects.get(id=1)
        self.assertEqual(lodash_package.name, 'lodash')

    def checkRating(self):
        pass

