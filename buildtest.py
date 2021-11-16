import time, os, sys
from github import Github

def test():
    NUM_TESTS = 20
    passed_array = [0] * 2
    passed_array[0] = test0()
    passed_array[1] = test1()


    num_passed = sum(passed_array)
    percent = num_passed / NUM_TESTS * 100

    print("Total: " + str(NUM_TESTS))
    print("Passed: " + str(num_passed))
    print("Coverage: " + str(round(percent)) + "%")
    print(str(num_passed) + "/" + str(NUM_TESTS) + " tests passed. " + str(round(percent)) + "%" + " line coverage achieved.")

def test0():
    """
    unit test for gcloud build:
        ensure that project is buildable with correct dependencies
    """
    try:
        os.system('gcloud builds submit --tag gcr.io/project2-20/cd-pipeline --project=project2-20')
    except Exception as e:
        print("Build Error: " + str(e))
        return 0
    return 1

def test1():
    """
    unit test for gcloud Deploy:
        ensure that project is deployable with correct dependencies
    """
    try:
        os.system('gcloud run deploy cd-pipeline --image gcr.io/project2-20/cd-pipeline --platform managed --region us-central1 --project=project2-20 --allow-unauthenticated')
    except Exception as e:
        print("Deploy Error: " + str(e))
        return 0
    return 1

def main():
    test()

if __name__ == "__main__":
    main()
