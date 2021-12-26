import os
import shutil
import time
import subprocess
from git import Repo
from datetime import date
from pathlib import Path


def delete_folder(folder_name):
    try:
        shutil.rmtree(folder_name, ignore_errors=True)
    except:
        pass


def remove_line_in_file(filename, del_line):
    with open(filename, "r") as text_obj:
        my_list = list(text_obj)
    del my_list[del_line - 1]
    with open(filename, "w") as text_obj:
        for n in my_list:
            text_obj.write(n)


def get_app_version(new_version_dict):
    for key, value in new_version_dict.items():
        for character in value:
            if character.isdigit():
                return value


def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False


def replace_version(file, old_version, new_version, key):
    with open(file, "r") as in_file:
        buf = in_file.readlines()

    with open(file, "w") as out_file:
        for line in buf:
            if key in line:
                line = line.replace(old_version, new_version, 1)
                out_file.write(line)
            else:
                out_file.write(line)


def rebump_without_changelog(url, new_version):
    try:
        if check_if_string_in_file("CHANGELOG.md", new_version):
            return "success"

        output = subprocess.check_output("changelog current",
                                         universal_newlines=True, shell=True)
        version = output.rstrip()

        try:
            project_folder = "temp_" + time.strftime("%Y%m%d-%H%M%S")
            Repo.clone_from(url, project_folder)
            master_changelog = project_folder + "/CHANGELOG.md"
        except:
            pass

        if check_if_string_in_file(master_changelog, str(version)):
            delete_folder(project_folder)
            return "success"
        else:
            with open("CHANGELOG.md", "r") as in_file:
                buf = in_file.readlines()
            with open("CHANGELOG.md", "w") as out_file:
                for line in buf:
                    if "## [" + version + "]" not in line:
                        out_file.write(line)
            delete_folder(project_folder)
            return "success"
    except Exception as error:
        return str(error)


def add_changelog_without_msg(new_version):
    try:
        if check_if_string_in_file("CHANGELOG.md", new_version):
            return "success"

        today = date.today()
        current_today = today.strftime("%Y-%m-%d")
        version = '## [{}] - {}'.format(new_version, current_today)
        with open("CHANGELOG.md", "r") as in_file:
            buf = in_file.readlines()

        with open("CHANGELOG.md", "w") as out_file:
            for line in buf:
                if line == "## [Unreleased]":
                    line = line + "\n\n" + version + "\n"
                elif line == "## [Unreleased]\n":
                    line = line + "\n" + version + "\n"
                out_file.write(line)
        return "success"
    except Exception as error:
        return str(error)


def add_changelog_with_msg(url, new_version, changelog_message, changelog_begin, changelog_end):
    try:
        try:
            project_folder = "temp_" + time.strftime("%Y%m%d-%H%M%S")
            Repo.clone_from(url, project_folder)
            shutil.copy(project_folder + "/CHANGELOG.md", ".")
            delete_folder(project_folder)
        except:
            pass

        today = date.today()
        current_today = today.strftime("%Y-%m-%d")
        version = '## [{}] - {}'.format(new_version, current_today)
        if str(changelog_begin) != "None" or str(changelog_end) != "None":
            changelog = \
            "".join(changelog_message[
                    changelog_message.index(changelog_begin) + 1:changelog_message.index(changelog_end)])
            new_changelog = """
{}
{}
""".format(version, changelog.split("\n", 1)[1])
        else:
            new_changelog = """
{}
{}
""".format(version, changelog_message)
        with open("CHANGELOG.md", "r") as in_file:
            buf = in_file.readlines()

        with open("CHANGELOG.md", "w") as out_file:
            for line in buf:
                if line == "## [Unreleased]":
                    line = line + "\n\n" + new_changelog + "\n"
                elif line == "## [Unreleased]\n":
                    line = line + "\n" + new_changelog + "\n"
                out_file.write(line)
        return "success"
    except Exception as error:
        return str(error)


def git_push(bump_message, username, email):
    repo = Repo('.')
    changed_files = [item.a_path for item in repo.index.diff(None)]
    if not changed_files:
        return "Version bump already performed. Nothing for me to do."
    else:
        repo.config_writer().set_value("user", "name", username).release()
        repo.config_writer().set_value("user", "email", email).release()
        repo.git.add(all=True)
        repo.index.commit(bump_message)
        origin = repo.remote('origin')
        origin.push()
        return "success"


def bump_version(url, branch, setting_dict, old_version_dict,
                 new_version_dict, master_version_dict, username,
                 email, changelog_message, changelog_begin, changelog_end):
    bot_answer = "My friend, Adding a new commit was success, please check"
    project_folder = "bump_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
    try:
        Repo.clone_from(url, project_folder, branch=branch)
        os.chdir(project_folder)
        for key, value in setting_dict.items():
            file = setting_dict[key]['name']
            my_key = setting_dict[key]['syntax']
            old_version = old_version_dict[key]
            new_version = new_version_dict[key]
            if old_version != new_version or new_version is not None or new_version != "None":
                try:
                    replace_version(file, old_version, new_version, my_key)
                except:
                    pass

        master_app_version = get_app_version(master_version_dict)
        app_version = get_app_version(new_version_dict)
        my_file = Path("CHANGELOG.md")

        changelog = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]"""
        if not my_file.is_file():
            with open("CHANGELOG.md", "w") as f:
                f.write(changelog)

        if not check_if_string_in_file("CHANGELOG.md", "## [Unreleased]"):
            bot_answer = "My friend, Adding a new commit was success, but was \
                         skip for changelog file Unreleased line doest \
                         not exit line please check"
        else:
            if str(changelog_begin) != "None" or str(changelog_end) != "None":
                if changelog_begin in str(changelog_message) and changelog_end in str(changelog_message):
                    add_changelog_with_msg_response = add_changelog_with_msg(url, app_version,
                                                                             changelog_message, changelog_begin,
                                                                             changelog_end)
                    if add_changelog_with_msg_response == "success":
                        pass
                    else:
                        return str(add_changelog_with_msg_response)
                else:
                    remove_rebump_response = rebump_without_changelog(url, app_version)
                    if remove_rebump_response != "success":
                        return str(remove_rebump_response)
                    add_changelog_without_msg_response = add_changelog_without_msg(app_version)
                    if add_changelog_without_msg_response == "success":
                        pass
                    else:
                        return str(add_changelog_without_msg_response)
            else:
                if str(changelog_message) is not None or str(changelog_message) != "None":
                    add_changelog_with_msg_response = add_changelog_with_msg(url, app_version,
                                                                             changelog_message, changelog_begin,
                                                                             changelog_end)
                    if add_changelog_with_msg_response == "success":
                        pass
                    else:
                        return str(add_changelog_with_msg_response)
                else:
                    remove_rebump_response = rebump_without_changelog(url, app_version)
                    if remove_rebump_response != "success":
                        return str(remove_rebump_response)
                    add_changelog_without_msg_response = add_changelog_without_msg(app_version)
                    if add_changelog_without_msg_response == "success":
                        pass
                    else:
                        return str(add_changelog_without_msg_response)

        bump_message = "Bump to {}".format(app_version)
        push_commit = git_push(bump_message, username, email)
        if push_commit != "success":
            return str(push_commit)
        os.chdir('../')
        delete_folder(project_folder)
        return bot_answer
    except Exception as error:
        return str(error)
