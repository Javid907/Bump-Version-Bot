import os
import shutil
import stat
import time
import re
from git import Repo


def remove_temp_folder(project_folder):
    try:
        shutil.rmtree(project_folder, ignore_errors=True)
    except:
        pass


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_new_version(master_version, version_type):
    if master_version == "None":
        return None
    version_type = version_type.lower()
    if version_type == 'ft' or "minor" in version_type:
        temp_1 = master_version.split('.')
        temp_2 = int(temp_1[1]) + 1
        temp_1[1] = str(temp_2)
        temp_1[2] = '0'
        str_1 = '.'.join(temp_1)
        return str_1
    elif version_type == 'fix' or "patch" in version_type:
        temp_1 = master_version.split('.')
        temp_2 = int(temp_1[2]) + 1
        temp_1[2] = str(temp_2)
        str_1 = '.'.join(temp_1)
        return str_1
    elif version_type == 'major' or "major" in version_type:
        temp_1 = master_version.split('.')
        temp_2 = int(temp_1[0]) + 1
        temp_1[0] = str(temp_2)
        temp_1[1] = '0'
        temp_1[2] = '0'
        str_1 = '.'.join(temp_1)
        return str_1
    else:
        return False


def get_version(file_name, syntax):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if syntax in line:
                    return re.findall(r'[\d.]+', line)[0]
    except:
        return "None"


def get_master_version_dict(url, setting_dict):
    project_folder = "get_master_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
    try:
        Repo.clone_from(url, project_folder)
        dict_value = {}
        os.chdir(project_folder)
        for key, value in setting_dict.items():
            version = get_version(setting_dict[key]['name'], setting_dict[key]['syntax'])
            dict_value[key] = version
        os.chdir('../')
        remove_temp_folder(project_folder)
        return dict_value
    except:
        return False


def get_old_version_dict(url, setting_dict, branch):
    project_folder = "get_old_version_temp_" + time.strftime("%Y%m%d-%H%M%S")
    try:
        Repo.clone_from(url, project_folder, branch=branch)
        dict_value = {}
        os.chdir(project_folder)
        for key, value in setting_dict.items():
            version = get_version(setting_dict[key]['name'], setting_dict[key]['syntax'])
            dict_value[key] = version
        os.chdir('../')
        remove_temp_folder(project_folder)
        return dict_value
    except:
        return False


def get_new_version_dict(master_version_dict, version_type):
    try:
        dict_value = {}
        for key, value in master_version_dict.items():
            if value == "None" or value == "." or value is None:
                version = "None"
            else:
                version = get_new_version(master_version_dict[key], version_type)
            dict_value[key] = version
        return dict_value
    except:
        return False
