import os
import shutil
import stat
import time
from git import Repo


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_microservice_type(url):
    project_folder = "get_microservice_type_temp_" + time.strftime("%Y%m%d-%H%M%S")
    Repo.clone_from(url, project_folder, branch="master")
    os.chdir(project_folder)
    if os.path.isfile('./mix.exs'):
        os.chdir('../')
        shutil.rmtree(project_folder, ignore_errors=True)
        return "elixir"
    elif os.path.isfile('./package.json'):
        os.chdir('../')
        shutil.rmtree(project_folder, ignore_errors=True)
        return "javascript"
    else:
        os.chdir('../')
        shutil.rmtree(project_folder, ignore_errors=True)
        return False
