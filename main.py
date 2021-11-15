from package_ops import *

class PackageRegistry():
    def __init__(self):
        self.packages = [] # list of package objects

    def add_package(self, package):
        self.packages.append(package)

    
class Package():
    def __init__(self, name, version, url):
        self.name = name
        self.version = version
        self.url = url


def main():
    registry = PackageRegistry()

    pass

if __name__ == '__main__':
    main()
