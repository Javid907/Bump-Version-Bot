import requests
import json


def get_repo_url(access_token, request_data):
    response = request_data['repository']['clone_url']
    replace = f'https://{access_token}:x-oauth-basic@'
    final = response.replace("https://", replace)
    return final


def check_pull_request(request_data, username):
    try:
        if request_data['pull_request']['assignee']['login'] == username:
            return True
    except:
        if username in request_data['comment']['body']:
            return True
        else:
            return False


def get_state(request_data):
    if request_data['pull_request']['state'] == 'open':
        return True
    elif request_data['issue']['state'] == 'open':
        return True
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
    query_url = "https://api.github.com/repos/{}/pulls/{}/reviews".format(github_repo, pull_request_id)
    headers = {'Authorization': "token {}".format(access_token)}
    r = requests.get(query_url, headers=headers)
    data = r.json()
    for i in range(50):
        if data[i]['state'] == 'APPROVED':
            return True
    else:
        return False


def re_assigne_owner(access_token, github_repo, pull_request_id, username, owner):
    try:
        query_url = "https://api.github.com/repos/{}/issues/{}/assignees".format(github_repo, pull_request_id)
        headers = {'Authorization': "token {}".format(access_token)}
        data = {"assignees": [username]}
        requests.delete(query_url, data=json.dumps(data), headers=headers)
        data = {"assignees": [owner]}
        requests.post(query_url, data=json.dumps(data), headers=headers)
        return True
    except Exception as error:
        return error


def merge_pull_request(access_token, github_repo, pull_request_id):
    query_url = "https://api.github.com/repos/{}/pulls/{}/merge".format(github_repo, pull_request_id)
    headers = {'Authorization': "token {}".format(access_token)}
    data = {"merge_method": "rebase"}
    r = requests.put(query_url, data=json.dumps(data), headers=headers)
    data = r.json()
    if data['merged']:
        return True
    else:
        return False


def get_branch_name(access_token, github_repo, pull_request_id):
    try:
        query_url = "https://api.github.com/repos/{}/pulls/{}".format(github_repo, pull_request_id)
        headers = {'Authorization': "token {}".format(access_token)}
        r = requests.get(query_url, headers=headers)
        data = r.json()
        return data['head']['ref']
    except Exception as error:
        return error


def send_answer(access_token, github_repo, pull_request_id, body):
    try:
        query_url = "https://api.github.com/repos/{}/issues/{}/comments".format(github_repo, pull_request_id)
        headers = {'Authorization': "token {}".format(access_token)}
        data = {"body": body}
        requests.post(query_url, data=json.dumps(data), headers=headers)
        return True
    except Exception as error:
        return error
