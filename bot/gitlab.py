import requests
import json


def get_ssh_url(gitlab_access_token, project_name, host):
    url = 'https://{}/api/v4/projects?search={}'.format(host, project_name)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    json_format = json.loads(response.text)
    count = 0
    for i in json_format:
        if json_format[count]['path'] == project_name:
            return json_format[count]['ssh_url_to_repo']
            break
        count += 1


def get_ssh_url(gitlab_access_token, project_name, host):
    url = 'https://{}/api/v4/projects?search={}'.format(host, project_name)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    json_format = json.loads(response.text)
    count = 0
    for i in json_format:
        if json_format[count]['path'] == project_name:
            return json_format[count]['ssh_url_to_repo']
            break
        count += 1


def get_project_id(gitlab_access_token, project_name, host):
    url = 'https://{}/api/v4/projects?search={}'.format(host, project_name)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    json_format = json.loads(response.text)
    count = 0
    for i in json_format:
        if json_format[count]['path'] == project_name:
            return json_format[count]['id']
            break
        count += 1


def get_merge_request_url(gitlab_access_token, project_name, host):
    url = 'https://{}/api/v4/projects?search={}'.format(host, project_name)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    json_format = json.loads(response.text)
    count = 0
    for i in json_format:
        if json_format[count]['path'] == project_name:
            return json_format[count]['_links']['merge_requests']
            break
        count += 1


def get_assignee_mr_url(gitlab_access_token, project_name, host):
    default_mr_url = get_merge_request_url(host, project_name, gitlab_access_token)
    url = '{}?state=opened'.format(default_mr_url)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    if response_json_format is not None:
        json_file_count = len(response_json_format)
        for i in range(json_file_count):
            assignee = response_json_format[i]['assignee']
            if assignee is not None:
                username = assignee['username']
                if username == 'scp-gitlab-merge-bot':
                    merge_request_id = response_json_format[i]['iid']
                    full_merge_request_url = '{}/{}'.format(default_mr_url, merge_request_id)
                    return full_merge_request_url


def get_assignee_mr_id(gitlab_access_token, full_mr_url):
    response = requests.get(full_mr_url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    return response_json_format['iid']


def get_branch_of_merge_request(gitlab_access_token, full_mr_url):
    if full_mr_url is not None:
        response = requests.get(full_mr_url, headers={'PRIVATE-TOKEN': gitlab_access_token})
        response_json_format = json.loads(response.text)
        source_branch = response_json_format['source_branch']
        return source_branch


def get_approvals_count(full_mr_url, gitlab_access_token):
    count = 0
    response = requests.get(full_mr_url + "/approvals", headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    approved_by = response_json_format['approved_by']
    for i in approved_by:
        if approved_by[0]['user']:
            count += 1
    return count


def get_status_pipeline(host, project_name, full_mr_url, gitlab_access_token):
    project_id = get_project_id(host, project_name, gitlab_access_token)
    merge_request_id = get_assignee_mr_id(full_mr_url, gitlab_access_token)
    ref_name = 'refs/merge-requests/{}/head'.format(merge_request_id)
    url = 'https://{}/api/v4/projects/{}/pipelines?ref={}'.format(host, project_id, ref_name)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    return response_json_format[0]['status']


def get_username_of_mr_author(full_mr_url, gitlab_access_token):
    response = requests.get(full_mr_url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    return response_json_format['author']['username']


def get_id_of_user(host, full_mr_url, gitlab_access_token):
    username = get_username_of_mr_author(full_mr_url, gitlab_access_token)
    url = 'https://{}/api/v4/users?username={}'.format(host, username)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    return response_json_format[0]['id']


def get_email_of_user(host, full_mr_url, gitlab_access_token):
    user_id = get_id_of_user(host, full_mr_url, gitlab_access_token)
    url = 'https://{}/api/v4/users/{}'.format(host, user_id)
    response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    return response_json_format['public_email']


def assignee_to_user(host, full_mr_url, gitlab_access_token):
    user_id = get_id_of_user(host, full_mr_url, gitlab_access_token)
    headers = {"content-type": "application/json", 'PRIVATE-TOKEN': gitlab_access_token}
    data = {"assignee_ids": [user_id]}
    requests.put(full_mr_url, headers=headers, data=json.dumps(data))


def get_http_mr_url(full_mr_url, gitlab_access_token):
    response = requests.get(full_mr_url, headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    return response_json_format['web_url']


def merge_assigner_mr(full_mr_url, gitlab_access_token):
    try:
        url = "{}/merge".format(full_mr_url)
        headers = {'PRIVATE-TOKEN': gitlab_access_token}
        requests.put(url, headers=headers)
        return "success"
    except:
        return "failed"


def get_list_of_approved_username(full_mr_url, gitlab_access_token):
    count = get_approvals_count(full_mr_url, gitlab_access_token)
    my_list = []
    response = requests.get(full_mr_url + "/approvals", headers={'PRIVATE-TOKEN': gitlab_access_token})
    response_json_format = json.loads(response.text)
    approved_by = response_json_format['approved_by']
    for i in range(count):
        my_list.append(approved_by[i]['user']['username'])
    return my_list


def get_list_of_approved_email(host, full_mr_url, gitlab_access_token):
    username_list = get_list_of_approved_username(full_mr_url, gitlab_access_token)
    email_list = []
    for username in username_list:
        url = 'https://{}/api/v4/users?username={}'.format(host, username)
        response = requests.get(url, headers={'PRIVATE-TOKEN': gitlab_access_token})
        response_json_format = json.loads(response.text)
        username_id = response_json_format[0]['id']

        new_url = 'https://{}/api/v4/users/{}'.format(host, username_id)
        new_response = requests.get(new_url, headers={'PRIVATE-TOKEN': gitlab_access_token})
        new_response_json_format = json.loads(new_response.text)
        email_list.append(new_response_json_format['public_email'])
    return email_list


def check_who_approved(full_mr_url, gitlab_access_token):
    username_list = get_list_of_approved_username(full_mr_url, gitlab_access_token)
    username = get_username_of_mr_author(full_mr_url, gitlab_access_token)
    for i in username_list:
        if i == username:
            return "failed"
        else:
            return "success"


def get_thread_status(full_mr_url, gitlab_access_token):
    try:
        response = requests.get(full_mr_url, headers={'PRIVATE-TOKEN': gitlab_access_token})
        response_json_format = json.loads(response.text)
        response_status=response_json_format['blocking_discussions_resolved']
        if response_status:
            return "success"
        else:
            return "failed"
    except:
        return "failed"
