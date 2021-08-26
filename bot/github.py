import requests
import json
from collections import Counter


def get_repo_url(access_token, github_repo):
    query_url = f"https://api.github.com/repos/{github_repo}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    response = data['clone_url']
    replace = f'https://{access_token}:x-oauth-basic@'
    final = response.replace("https://", replace)
    return final


def get_repo_ssh_url(access_token, github_repo):
    query_url = f"https://api.github.com/repos/{github_repo}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    return data['ssh_url']


def get_count_pull_request(access_token, github_repo):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    try:
        return data[0]['number']
    except:
        return False


def get_assigner_pull_request(access_token, github_repo, bot_username):
    count = get_count_pull_request(access_token, github_repo)
    for i in range(1, count + 1):
        query_url = f"https://api.github.com/repos/{github_repo}/pulls/{i}"
        headers = {'Authorization': f'token {access_token}'}
        r = requests.get(query_url, headers=headers)
        data = r.json()
        try:
            user = data['assignee']['login']
            if user == bot_username:
                return i
                break
        except:
            pass


def get_branch_name(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    branch = data['head']['ref']
    return branch


def get_owner(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    owner = data['user']['login']
    return owner


def get_state(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    state = data['state']
    if state == 'open':
        return True
    else:
        return False


def get_review(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}/reviews"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    try:
        for i in range(len(data) + 1):
            if data[i]['state'] == 'APPROVED':
                return True
        else:
            return False
    except:
        return False


def get_draft(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    draft = data['mergeable_state']
    if draft == 'draft':
        return False
    else:
        return True


def get_action_state(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    action_state = data['mergeable_state']
    if action_state == 'unstable':
        return False
    else:
        return True


def get_rebaseable(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    return data['rebaseable']


def get_mergeable(access_token, github_repo, pull_request_id):
    query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}"
    headers = {'Authorization': f'token {access_token}'}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    return data['mergeable']


def get_rebase_status(access_token, github_repo, pull_request_id):
    mergeable = get_mergeable(access_token, github_repo, pull_request_id)
    rebaseable = get_rebaseable(access_token, github_repo, pull_request_id)
    if rebaseable == True and mergeable == True:
        return True
    elif rebaseable == True and mergeable == False:
        return False
    elif rebaseable == False and mergeable == False:
        return False
    elif rebaseable == False and mergeable == False:
        return False
    else:
        return False


def merge_pull_request(access_token, github_repo, pull_request_id):
    try:
        query_url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_id}/merge"
        headers = {'Authorization': f'token {access_token}'}
        data = {"merge_method": "rebase"}
        r = requests.put(query_url, data=json.dumps(data), headers=headers)
        data = r.json()
        if data['merged']:
            return True
        else:
            return False
    except:
        return False


def re_assigne_owner(access_token, github_repo, pull_request_id, bot_username):
    owner = get_owner(access_token, github_repo, pull_request_id)
    try:
        query_url = f"https://api.github.com/repos/{github_repo}/issues/{pull_request_id}/assignees"
        headers = {'Authorization': f'token {access_token}'}
        data = {"assignees": [bot_username]}
        requests.delete(query_url, data=json.dumps(data), headers=headers)
        data = {"assignees": [owner]}
        requests.post(query_url, data=json.dumps(data), headers=headers)
        return True
    except:
        return False