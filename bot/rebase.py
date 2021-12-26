import os
import shutil
import time
import difflib
from git import Repo
from pathlib import Path
from datetime import date
from . import bump
from . import version


def add_changelog_rebase(url, new_version, old_changelog):
    try:
        try:
            project_folder = "temp_" + time.strftime("%Y%m%d-%H%M%S")
            Repo.clone_from(url, project_folder)
            shutil.copy(project_folder + "/CHANGELOG.md", ".")
            bump.delete_folder(project_folder)
        except:
            pass

        today = date.today()
        current_today = today.strftime("%Y-%m-%d")
        version = '## [{}] - {}'.format(new_version, current_today)
        new_changelog = """
{}
{}
""".format(version, old_changelog)
        with open("CHANGELOG.md", "r") as in_file:
            buf = in_file.readlines()

        with open("CHANGELOG.md", "w") as out_file:
            for line in buf:
                if line == "## [Unreleased]":
                    line = line + new_changelog
                elif line == "## [Unreleased]\n":
                    line = line + new_changelog
                out_file.write(line)
        return "success"
    except Exception as error:
        return str(error)


def get_changelog_rebase(url):
    try:
        project_folder = "temp_" + time.strftime("%Y%m%d-%H%M%S")
        Repo.clone_from(url, project_folder)
        master_changelog = project_folder + "/CHANGELOG.md"
        current_changelog = "CHANGELOG.md"

        data = []
        with open(master_changelog) as file_1:
            file_1_text = file_1.readlines()

        with open(current_changelog) as file_2:
            file_2_text = file_2.readlines()

        # Find and print the diff:
        for line in difflib.unified_diff(
                file_1_text, file_2_text, fromfile=master_changelog,
                tofile=current_changelog, lineterm=''):
            if not line.startswith("-"):
                data.append(line.split('+')[-1])

        new_data = data[7::]
        last_data = new_data[:-3]
        bump.delete_folder(project_folder)
        return '\n'.join(last_data).replace('\n\n', '\n')
    except:
        return False


def git_conflicts_list(setting_dict):
    try:
        conflicts_list = []
        repo = Repo('.')
        status_git = repo.git.status(porcelain=True).split()
        for l, k in enumerate(status_git):
            if "UU" == k:
                conflicts_list.append(status_git[l + 1])

        default_files_list = []

        for key, value in setting_dict.items():
            file = setting_dict[key]['name']
            default_files_list.append(file)

        non_default = []
        for i in conflicts_list:
            if i not in default_files_list:
                non_default.append(i)

        if not non_default:
            return "success"
        elif len(non_default) == 1 and non_default[0] == "CHANGELOG.md":
            return "success_with_changelog"
        else:
            return non_default
    except Exception as error:
        return str(error)


def run_rebase(branch, rebase_branch, setting_dict, username, email):
    try:
        repo = Repo('.')
        repo.config_writer().set_value("user", "name", username).release()
        repo.config_writer().set_value("user", "email", email).release()
        for b in repo.remote().fetch():
            repo.git.checkout('-B', b.name.split('origin/')[1], b.name)
        os.system('git checkout ' + branch)
        os.system('git rebase ' + rebase_branch)

        git_conflicts_list_response = git_conflicts_list(setting_dict)
        if git_conflicts_list_response == "success":
            for key, value in setting_dict.items():
                file = setting_dict[key]['name']
                path_to_file = file
                path = Path(path_to_file)
                if path.is_file():
                    os.system('git checkout --ours ' + file)
            repo.git.add(all=True)
            os.system('git rebase --continue')
            return "success"
        elif git_conflicts_list_response == "success_with_changelog":
            for key, value in setting_dict.items():
                file = setting_dict[key]['name']
                path_to_file = file
                path = Path(path_to_file)
                if path.is_file():
                    os.system('git checkout --ours ' + file)
            os.system('git checkout --ours CHANGELOG.md')
            repo.git.add(all=True)
            os.system('git rebase --continue')
            return "success"
        else:
            return str(git_conflicts_list_response)
    except Exception as error:
        return str(error)


def git_force_push(bump_message, username, email, project_folder):
    repo = Repo('.')
    repo.config_writer().set_value("user", "name", username).release()
    repo.config_writer().set_value("user", "email", email).release()
    repo.git.add(all=True)
    repo.index.commit(bump_message)
    origin = repo.remote('origin')
    origin.push(force=True)
    os.chdir('../')
    bump.delete_folder(project_folder)


def bump_version_rebase(url, branch, setting_dict, new_version_dict, username, email, bot_command_2):
    try:
        bot_answer = "My friend, Adding a new commit was success with rebase, please check"
        project_folder = "rebase_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
        Repo.clone_from(url, project_folder, branch=branch)
        os.chdir(project_folder)

        get_changelog_rebase_response = get_changelog_rebase(url)
        if not get_changelog_rebase_response:
            return str(get_changelog_rebase_response)

        run_rebase_response = run_rebase(branch, bot_command_2, setting_dict, username, email)
        if run_rebase_response == "success":
            pass
        else:
            return "Error while trying rebase" + str(run_rebase_response)

        bump_message = "rebase by bot"
        git_force_push(bump_message, username, email, project_folder)

        project_folder = "bump_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
        Repo.clone_from(url, project_folder, branch=branch)
        os.chdir(project_folder)

        old_version_dict = {}
        for key, value in setting_dict.items():
            old_version = version.get_version(setting_dict[key]['name'], setting_dict[key]['syntax'])
            old_version_dict[key] = old_version

        for key, value in setting_dict.items():
            file = setting_dict[key]['name']
            my_key = setting_dict[key]['syntax']
            old_version = old_version_dict[key]
            new_version = new_version_dict[key]
            if old_version != new_version or new_version is not None or new_version != "None":
                try:
                    bump.replace_version(file, old_version, new_version, my_key)
                except:
                    pass

        app_version = bump.get_app_version(new_version_dict)
        add_changelog_rebase_response = add_changelog_rebase(url, app_version, get_changelog_rebase_response)
        if add_changelog_rebase_response == "success":
            pass
        else:
            return str(add_changelog_rebase_response)

        bump_message = "Bump to {}".format(app_version)
        git_force_push(bump_message, username, email, project_folder)

        return bot_answer
    except Exception as error:
        return str(error)
