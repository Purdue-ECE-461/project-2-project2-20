
def get_rating(package_url):
    #order to return:
    # Bus Factor
    # Correctness
    # RampUp
    # ResponsiveMaintainer
    # License
    # GoodPinningPractice

    ratings = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    return ratings

def check_trust(rating):
    low_ratings = [x for x in rating if x < 0.5]
    return (len(low_ratings) == 0)