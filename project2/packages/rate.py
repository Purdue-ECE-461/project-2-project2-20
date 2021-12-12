import requests
from bs4 import BeautifulSoup
import os
import datetime as dt
import dateutil.relativedelta as du
from github import Github

def get_rating(package_url):
    #order to return:
    # Bus Factor
    # Correctness
    # RampUp
    # ResponsiveMaintainer
    # License
    # GoodPinningPractice

    
    backup_url = package_url
    # print(url)
    metadata_dict = metadata_collect(package_url)
    # print(metadata_dict)
    returnedurl,net_score,ramp_up_score,correctness_score,bus_factor_score,responsive_maintainer_score,license_score = scoring(backup_url, metadata_dict)
    ratings = [net_score, ramp_up_score,correctness_score,bus_factor_score,responsive_maintainer_score,license_score]

    # ratings = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    return ratings

def check_trust(rating):
    low_ratings = [x for x in rating if x < 0.5]
    return (len(low_ratings) == 0)

def metadata_collect(url):
    npm_flag = "https://www.npmjs.com"
    if npm_flag in url:
        headers = {'Accept-Encoding': 'identity'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        all_links = soup.find_all('a', attrs={'aria-labelledby':'repository'})
        url = all_links[0].get('href')

    url = url.replace("https://github.com/", "")

    token = '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'

    g = Github(token)
    reps = g.get_repo(url)

    content_list = reps.get_contents("")
    p_list = []

    for elem in content_list:
        p_list.append(elem.path)
    mit = "MIT"
    gnu = "GNU"
    apache = "Apache"
    affero = "Affero"
    bsd = "BSD"
    mit_l = mit.lower()
    gnu_l = gnu.lower()
    apache_l = apache.lower()
    affero_l = affero.lower()
    bsd_l = bsd.lower()

    git_name = 'LICENSE'
    if git_name in p_list:
        li = reps.get_license().decoded_content
        li = li.title().decode()
        if mit_l in li.lower() or gnu_l in li.lower() or apache_l in li.lower() or affero_l in li.lower() \
                or bsd_l in li.lower():
            lic = 1
        else:
            lic = 0
    else:
        lic = 0

    git_name = 'README.md'
    if git_name in p_list:
        li = reps.get_readme().decoded_content
        li = li.title().decode()
        if lic != 1:
            if mit_l in li.lower() or gnu_l in li.lower() or apache_l in li.lower() or affero_l in li.lower() \
                    or bsd_l in li.lower():
                lic = 1
            else:
                lic = 0
        rm = 1
    else:
        rm = 0

    if reps.has_wiki:
        wiki = 1
    else:
        wiki = 0

    git_name = 'CONTRIBUTING.md'
    if (git_name or 'ISSUE_TEMPLATE') in p_list:
        contri = 1
    else:
        contri = 0

    today = dt.datetime.now()
    date_lm = today + du.relativedelta(months=-1)

    # trying to get issues from the last month
    issues_total1 = reps.get_issues(since=date_lm, state='all').totalCount
    issues_closed1 = reps.get_issues(since=date_lm, state='closed').totalCount
    if issues_total1:
        per_close_1 = (issues_closed1 / issues_total1) * 100
    else:
        per_close_1 = 0
    date_llm = date_lm + du.relativedelta(months=-1)
    issues_total2 = reps.get_issues(since=date_llm, state='all').totalCount - issues_total1
    issues_closed2 = reps.get_issues(since=date_llm, state='closed').totalCount - issues_closed1
    if issues_total2:
        per_close_2 = (issues_closed2 / issues_total2) * 100
    else:
        per_close_2 = 0

    date_lllm = date_llm + du.relativedelta(months=-1)
    issues_total3 = reps.get_issues(since=date_lllm, state='all').totalCount - issues_total1 - issues_total2
    issues_closed3 = reps.get_issues(since=date_lllm, state='closed').totalCount - issues_closed1 - issues_closed2
    if issues_total3:
        per_close_3 = (issues_closed3 / issues_total3) * 100
    else:
        per_close_3 = 0

    avg_per_close = (per_close_1 + per_close_2 + per_close_3) / 3
    # print(avg_per_close)

    cont = reps.get_contributors(anon='True').totalCount  # number of contributors for the repo
    issues_close_time = reps.get_issues(since=date_lm, state='closed')
    cr_time = []
    end_time = []
    # print((cr_time))
    iss_check = reps.get_issues(since=date_lm, state='closed').totalCount
    if iss_check > 0:
        for issues in issues_close_time:
            cr_time.append(issues.created_at.day)
            end_time.append(issues.closed_at.day)
        time_taken = [m - n for m, n in zip(end_time, cr_time)]
        avg_response_time = sum(time_taken) / len(time_taken)
        # print(avg_response_time)
    else:
        avg_response_time = 10000

    metadata_dict = {
        "readme": rm,  # Ramp-up score
        "contributing": contri,  # Ramp-up score
        "documentation": wiki,  # Ramp-up score
        "average %issues closed": avg_per_close,  # Correctness score
        "number_contributors": cont,  # Bus-factor score
        "average time": avg_response_time,  # Responsive Maintainer Score
        "license": lic  # License score
    }
    return metadata_dict



def scoring(url, arg):
    active = None
    # weights for each score
    weight_ramp = 0.1
    weight_correct = 0.2
    weight_busfactor = 0.35
    weight_active = 0.2
    weight_license = 0.15

    # ramp up score checks if the repository has a readme, a contributing/issue template, and documentation to reduce
    # ramp-up time
    key = 'readme'
    key1 = 'contributing'
    key2 = 'documentation'
    unw_ramp = (arg.get(key) + arg.get(key1) + arg.get(key2)) / 3

    # correctness uses the average percentage of issues closed per month over the last three months (implemented)
    avg_iss_clsd = arg.get('average %issues closed')  # number of average issues closed
    if avg_iss_clsd == 0:
        correctness_sc = 0
    elif avg_iss_clsd <= 50:
        if avg_iss_clsd > 0:
            correctness_sc = 0.5
        else:
            correctness_sc = 0
    else:
        correctness_sc = 1

    # the number of contributors
    num_contributors = (arg.get('number_contributors'))
    if num_contributors >= 40:
        bus_score = 1
    elif 40 > num_contributors >= 20:
        bus_score = 0.5
    elif 20 > num_contributors >= 10:
        bus_score = 0.2
    elif num_contributors < 10:
        bus_score = 0
    else:
        bus_score = 0

    # active uses the average time taken to close or respond to an open issue over last month.
    time_taken = (arg.get('average time'))
    if time_taken:
        if time_taken <= 3:  # was chosen based on a an Audit by David Eaves for Mozilla Community Metrics. The
            # presentation is the first link for the search input: "Mozilla Community Metrics - Community Builders"
            active = 1
        elif 3 < time_taken <= 7:  # The same audit found that contributors who waited over 7 days for a code review had
            # virtually zero likelihood of returning, thus giving us the metric for active maintainers
            active = 0.4
        elif 7 < time_taken <= 50:
            active = 0.2
        elif time_taken > 50:
            active = 0
    else:
        active = 0
    # license checks if license is compatible with GNU LPGLv2.1
    license_boo = (arg.get('license'))  # gets value of key from dictionary input
    if license_boo == 0:  # All the pre-processing done in get-metadata.py. 1 if License is compatible with GNU
        # LGPLv2.1, 0 if it isn't.
        license_unw = 0
    else:
        license_unw = 1

    # assigning scores for clarity
    ramp_up_score = unw_ramp
    correctness_score = correctness_sc
    bus_factor_score = bus_score
    responsive_maintainer_score = active
    license_score = license_unw

    # Calculating weighted sum. Weights were assigned in a way that the sum is always between 0 and 1, with 0 for the
    # worst repositories and 1 for repositories that satisfy all requirements.
    net_score = (weight_ramp * ramp_up_score) + (weight_correct * correctness_score) + (
            weight_busfactor * bus_factor_score) + (weight_active * responsive_maintainer_score) + (
                        weight_license * license_score)
    net_score = round(net_score, 1)
    ramp_up_score = round(ramp_up_score, 1)
    correctness_score = round(correctness_score, 1)
    bus_factor_score = round(bus_factor_score, 1)
    responsive_maintainer_score = round(responsive_maintainer_score, 1)
    license_score = round(license_score, 1)

#     print(f"{url} {net_score} {ramp_up_score} {correctness_score} {bus_factor_score} {responsive_maintainer_score}\
#  {license_score}")
    return url,net_score,ramp_up_score,correctness_score,bus_factor_score,responsive_maintainer_score,license_score
