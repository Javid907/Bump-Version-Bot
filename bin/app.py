from flask import Flask, request
from bot import config, github, env, gitlab, bump
from waitress import serve

app = Flask(__name__)
bot_username = config.get_config('bot_username')
token = config.get_config('token')
hosting = config.get_config('hosting')
if hosting == "gitlab":
    host = config.get_config('host')


@app.route('/bot_bump_version', methods=['POST'])
def bot_bump_version():
    try:
        repo = request.args.get('repo_name')

        if hosting == "github":
            pull_request_id = github.get_assigner_pull_request(token, repo, bot_username)
            url = github.get_repo_url(token, repo)
            branch = github.get_branch_name(token, repo, pull_request_id)
            pull_request_url = f"https://github.com/{repo}/pull/{pull_request_id}"

            if not github.get_state(token, repo, pull_request_id):
                github.re_assigne_owner(token, repo, pull_request_id, bot_username)
                return str("This Pull Request is close " + pull_request_url), 405

            if not github.get_rebase_status(token, repo, pull_request_id):
                github.re_assigne_owner(token, repo, pull_request_id, bot_username)
                return str("Rebase need " + pull_request_url), 405

            if not github.get_draft(token, repo, pull_request_id):
                github.re_assigne_owner(token, repo, pull_request_id, bot_username)
                return str("This is a draft Pull Request " + pull_request_url), 405

            if not github.get_review(token, repo, pull_request_id):
                github.re_assigne_owner(token, repo, pull_request_id, bot_username)
                return str("This Pull Request was not approved " + pull_request_url), 405

            if not github.get_action_state(token, repo, pull_request_id):
                github.re_assigne_owner(token, repo, pull_request_id, bot_username)
                return str("Action is red " + pull_request_url), 405

        elif hosting == "gitlab":
            url = gitlab.get_repo_url(token, repo, host)
            assignee_mr_url = gitlab.get_assignee_mr_url(token, repo, host)
            branch = gitlab.get_branch_of_merge_request(token, assignee_mr_url)
            pull_request_url = gitlab.get_http_mr_url(assignee_mr_url, token)

            if gitlab.get_thread_status(assignee_mr_url, token):
                gitlab.assignee_to_user(url, assignee_mr_url, token)
                return str("There are open discussions  " + pull_request_url), 405

            if gitlab.get_rebase_status(assignee_mr_url, token):
                gitlab.assignee_to_user(url, assignee_mr_url, token)
                return str("Rebase need " + pull_request_url), 405

            if gitlab.check_who_approved(assignee_mr_url, token):
                gitlab.assignee_to_user(url, assignee_mr_url, token)
                return str("MR should be approved from other person " + pull_request_url), 405

            approve_count = gitlab.get_approvals_count(assignee_mr_url, token)
            if int(approve_count) < 1:
                gitlab.assignee_to_user(url, assignee_mr_url, token)
                return str("This Pull Request was not approved " + pull_request_url), 405

            if gitlab.get_status_pipeline(url, project_name, assignee_mr_url, token):
                gitlab.assignee_to_user(url, assignee_mr_url, token)
                return str("Pipeline is red " + assignee_mr_url), 405

        microservice_type = env.get_microservice_type(url)
        old_version = bump.get_old_version(url, microservice_type, branch)
        master_version = bump.get_master_version(url, microservice_type)
        new_version = bump.get_new_version(branch, master_version)
        push = bump.bump_version(url, branch, old_version, new_version, microservice_type)

        if hosting == "github":
            github.re_assigne_owner(token, repo, pull_request_id, bot_username)
        elif hosting == "gitlab":
            gitlab.assignee_to_user(url, assignee_mr_url, token)

        if request.args.get('merge'):
            if not github.merge_pull_request(token, repo, pull_request_id):
                return str("Could not merge " + assignee_mr_url), 405

        return str(push), 200
    except Exception as error:
        return str(error), 405


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
