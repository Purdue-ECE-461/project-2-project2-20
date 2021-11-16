from django.test import TestCase
from packages.models import Package

# Create your tests here.

class PackageTestCase(TestCase):
    def set_up(self):
        Package.objects.create(name='lodash', version='4.0.0', url='https://github.com/lodash/lodash')
        Package.objects.create(name='jQuery', version='3.6.0', url='https://github.com/jquery/jquery')

    def test_num_packages(self):
        packages = Package.objects.all()
        self.assertEqual(len(packages), 2)

    def test_package_id(self):
        lodash_package = Package.objects.get(id=1)
        self.assertEqual(lodash_package.name, 'lodash')