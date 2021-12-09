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
        Package.objects.create(name='lodash', version='4.0.0', url='https://github.com/lodash/lodash')
        Package.objects.create(name='jQuery', version='3.6.0', url='https://github.com/jquery/jquery')

    def test_num_packages(self):
        packages = list(Package.objects.all())
        self.assertEqual(len(packages), 2)

    def test_package_id(self):
        lodash_package = Package.objects.get(id=1)
        self.assertEqual(lodash_package.name, 'lodash')

class RESTTestCase(APITestCase):
    def checkReset(self):
        response = self.client.delete('/api/reset/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def checkCreate(self):
        data = {'name': 'sample', 'version': '1.0.0', 'url': 'https://github.com/sample/sample/'}
        self.client.post('/api/package/', data)
        all_packages_data = self.client.get('/api/packages/')
        self.assertEqual(len(all_packages_data), 1)

    def checkUpdate(self):
        data = {'name': 'sample', 'version': '1.0.0', 'url': 'https://github.com/sample/sample/'}
        self.client.post('/api/package/', data)
        new_data = {'name': 'sample', 'version': '2.0.0', 'url': 'https://github.com/sample/sample/'}
        response = self.client.put('/api/package/', new_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def checkDelete(self):
        data = {'name': 'sample', 'version': '1.0.0', 'url': 'https://github.com/sample/sample/'}
        self.client.post('/api/package/', data)
        response = self.client.delete('/api/package')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def checkRate(self):
        data = {'name': 'sample', 'version': '1.0.0', 'url': 'https://github.com/sample/sample/'}
        self.client.post('/api/package/', data)
        response = self.client.get('/api/package/1/rate')
        self.assertEqual(response.status_code, HTTP_200_OK)

