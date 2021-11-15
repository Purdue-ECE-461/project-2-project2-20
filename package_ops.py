from github import Github

# Fetch listing of packages in registry

def fetch_listing(registry):
    '''
    fetch listing of all packages in registry
    '''
    return registry.packages

# Request update of npm package

def package_update(package):
    '''
    inputs:
    package - package object that will be updated

    if "ingestible", get new version of package in registry
    '''
    scores = rate_package(package)
    can_ingest = True

    for s in scores:
        if s < 0.5:
            can_ingest = False
    
    if can_ingest:
        print("can upload")

    return


# Request security audit of package using npm audit

def security_audit(package):
    pass

def rate_package(package):
    print(package.url)
    return [1, 1, 1, 1, 1] # scores from project 1
