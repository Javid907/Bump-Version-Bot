import requests
import json


def get_repo_url(access_token, request_data):
    response = request_data['repository']['clone_url']
    replace = f'https://{access_token}:x-oauth-basic@'
    final = response.replace("https://", replace)
    return final


def get_assigner_pull_request(request_data, bot_username):
    if request_data['action'] == 'assigned':
        if request_data['pull_request']['assignee']['login'] == bot_username:
            return request_data['number']
        else:
            return False
    else:
        return False


def get_state(request_data):
    state = request_data['pull_request']['state']
    if state == 'open':
        return True
    else:
        return False


def get_rebase_status(request_data):
    mergeable = request_data['pull_request']['mergeable']
    rebaseable = request_data['pull_request']['rebaseable']
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


def get_draft(request_data):
    if request_data['pull_request']['mergeable_state'] == 'draft':
        return False
    else:
        return True


def get_action_state(request_data):
    if request_data['pull_request']['mergeable_state'] == 'unstable':
        return False
    else:
        return True


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


def re_assigne_owner(access_token, github_repo, pull_request_id, bot_username, request_data):
    owner = request_data['pull_request']['user']['login']
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
