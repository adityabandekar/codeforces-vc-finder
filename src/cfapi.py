import requests

CF_CONTESTS_API = "https://codeforces.com/api/contest.list?gym=false"
CF_SET_API = "https://codeforces.com/api/problemset.problems"
CF_SUBMISSION_API = "https://codeforces.com/api/user.status?handle={handle}"

def get_cf_contest_ids():
    response = requests.get(CF_CONTESTS_API, timeout=300)
    data = response.json()
    if data["status"] != "OK":
        return None
    contest_ids = set()
    for contest in data["result"]:
        contest_ids.add(contest["id"])
    return contest_ids

def get_user_submissions(handle: str):
    response = requests.get(CF_SUBMISSION_API.format(handle=handle), timeout=300)
    data = response.json()
    if data["status"] != "OK":
        return None
    submission_list = []
    for submission in data["result"]:
        if "contestId" in submission:
            submission_list.append(submission)
    return submission_list