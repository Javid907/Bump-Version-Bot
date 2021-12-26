import requests
import json


def get_repo_url(access_token, request_data):
    response = request_data['project']['http_url']
    replace = f'https://oauth2:{access_token}@'
    final = response.replace("https://", replace)
    return final


def object_kind(request_data):
    if request_data['object_kind'] == "merge_request":
        return "merge_request"
    elif request_data['object_kind'] == "note":
        return "note"
    else:
        return False


def get_assigne_mr_id(request_data, username):
    try:
        if request_data['assignees'][0]['username'] == username:
            return request_data['object_attributes']['iid']
        else:
            return False
    except:
        return False


def get_note_mr_id(request_data, username):
    try:
        if username in request_data['object_attributes']['note']:
            return request_data['merge_request']['iid']
        else:
            return False
    except:
        return False


def get_merge_status(request_data, object_kind):
    if object_kind == "note":
        if request_data['merge_request']['merge_status'] == "can_be_merged":
            return True
        else:
            return False
    elif object_kind == "merge_request":
        if request_data['object_attributes']['merge_status'] == "can_be_merged":
            return True
        else:
            return False


def re_assigne_owner(full_mr_url, gitlab_access_token, request_data):
    user_id = request_data['user']['id']
    headers = {"content-type": "application/json", 'PRIVATE-TOKEN': gitlab_access_token}
    data = {"assignee_ids": [user_id]}
    requests.put(full_mr_url, headers=headers, data=json.dumps(data))


def get_thread_status(full_mr_url, gitlab_access_token):
    response = requests.get(full_mr_url + "/discussions", headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    for i in response_json_format:
        if i["notes"][0]["resolvable"]:
            if i["notes"][0]["resolved"]:
                return True
            else:
                return False


def get_status_pipeline(full_mr_url, gitlab_access_token):
    response = requests.get(full_mr_url + "/pipelines", headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    if response_json_format[-1]['status'] == "success":
        return True
    else:
        return False


def get_approvals_count(full_mr_url, gitlab_access_token):
    count = 0
    response = requests.get(full_mr_url + "/approvals", headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    approved_by = response_json_format['approved_by']
    for i in approved_by:
        if approved_by[0]['user']:
            count += 1
    return count


def get_list_of_approved_username(full_mr_url, gitlab_access_token):
    count = get_approvals_count(full_mr_url, gitlab_access_token)
    my_list = []
    response = requests.get(full_mr_url + "/approvals", headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    approved_by = response_json_format['approved_by']
    for i in range(count):
        my_list.append(approved_by[i]['user']['username'])
    return my_list


def check_who_approved(full_mr_url, gitlab_access_token, request_data):
    list_of_approved_username = get_list_of_approved_username(full_mr_url, gitlab_access_token)
    owner = request_data['user']['username']
    for i in list_of_approved_username:
        if i == owner:
            return False
        else:
            return True


def send_answer(full_mr_url, gitlab_access_token, message):
    headers = {"content-type": "application/json", 'PRIVATE-TOKEN': gitlab_access_token}
    data = {"body": message}
    requests.post(full_mr_url + "/notes", headers=headers, data=json.dumps(data))


def merge_request(full_mr_url, gitlab_access_token):
    try:
        url = "{}/merge".format(full_mr_url)
        headers = {'PRIVATE-TOKEN': gitlab_access_token}
        requests.put(url, headers=headers)
        return "success"
    except:
        return "failed"
