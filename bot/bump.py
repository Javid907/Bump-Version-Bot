import fileinput
import os
import shutil
import stat
import time

from git import Repo


def remove_temp_folder(project_folder):
    try:
        shutil.rmtree(project_folder, ignore_errors=True)
    except:
        pass


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_version(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if 'version' in line:
                try:
                    version_split = line.split(":", 1)
                    version = version_split[1].split('"')
                    return version[1]
                except:
                    version_split = line.split(" ", 1)
                    version = version_split[1].split('"')
                    return version[1]


def get_old_version(url, microservice_type, branch):
    project_folder = "get_old_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
    Repo.clone_from(url, project_folder, branch=branch)
    os.chdir(project_folder)
    if microservice_type == "elixir":
        version = get_version('mix.exs')
        os.chdir('../')
        remove_temp_folder(project_folder)
        return version
    elif microservice_type == "javascript":
        version = get_version("package.json")
        os.chdir('../')
        remove_temp_folder(project_folder)
        return version
    else:
        os.chdir('../')
        remove_temp_folder(project_folder)
        return "failed get_old_version"


def get_master_version(url, microservice_type):
    project_folder = "get_master_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
    Repo.clone_from(url, project_folder, branch="master")
    os.chdir(project_folder)
    if microservice_type == "elixir":
        version = get_version('mix.exs')
        os.chdir('../')
        remove_temp_folder(project_folder)
        return version
    elif microservice_type == "javascript":
        version = get_version("package.json")
        os.chdir('../')
        remove_temp_folder(project_folder)
        return version
    else:
        os.chdir('../')
        remove_temp_folder(project_folder)
        return "failed get_master_version"


def get_new_version(branch, old_version):
    branch_type = branch.split('/')[0]
    branch_type = branch_type.lower()
    if branch_type == 'ft':
        temp_1 = old_version.split('.')
        temp_2 = int(temp_1[1]) + 1
        temp_1[1] = str(temp_2)
        temp_1[2] = '0'
        str_1 = '.'.join(temp_1)
        return str_1
    elif branch_type == 'fix':
        temp_1 = old_version.split('.')
        temp_2 = int(temp_1[2]) + 1
        temp_1[2] = str(temp_2)
        str_1 = '.'.join(temp_1)
        return str_1
    else:
        return False


def git_push(new_version):
    repo = Repo('.')
    bump_message = "Bump to {}".format(new_version)
    repo.git.add(all=True)
    repo.index.commit(bump_message)
    origin = repo.remote('origin')
    origin.push()


def bump_version(url, branch, old_version, new_version, microservice_type):
    project_folder = "bump_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
    Repo.clone_from(url, project_folder, branch=branch)
    os.chdir(project_folder)
    if microservice_type == "elixir":
        with fileinput.FileInput("mix.exs", inplace=True) as file:
            for line in file:
                print(line.replace(old_version, new_version), end='')
    elif microservice_type == "javascript":
        with fileinput.FileInput("package.json", inplace=True) as file:
            for line in file:
                print(line.replace(old_version, new_version), end='')
    else:
        os.chdir('../')
        remove_temp_folder(project_folder)
        return "failed"

    try:
        os.chdir('chart')
        with fileinput.FileInput("Chart.yaml", inplace=True) as file:
            for line in file:
                print(line.replace(old_version, new_version), end='')
        with fileinput.FileInput("values.yaml", inplace=True) as file:
            for line in file:
                print(line.replace(old_version, new_version), end='')
        os.chdir('../')
    except:
        pass

    git_push(new_version)
    os.chdir('../')
    remove_temp_folder(project_folder)
    return "success"
