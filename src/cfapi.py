import requests

CF_CONTESTS_API = "https://codeforces.com/api/contest.list?gym=false"
CF_SET_API = "https://codeforces.com/api/problemset.problems"
CF_SUBMISSION_API = "https://codeforces.com/api/user.status?handle={handle}"

def get_cf_contest_ids():
    response = requests.get(CF_CONTESTS_API, timeout=300)
    data = response.json()
    return set(contest["id"] for contest in data["result"]) if data["status"] == "OK" else None

def get_user_submissions(handle: str):
    response = requests.get(CF_SUBMISSION_API.format(handle=handle), timeout=300)
    data = response.json()
    return [sub for sub in data["result"] if "contestId" in sub] if data["status"] == "OK" else None