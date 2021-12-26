import os
import shutil
import stat
import time
import subprocess
import logging
from typing import List, Tuple, Union
from pathlib import Path
from git import Repo

EXE = shutil.which("github-linguist")
GIT = shutil.which("git")


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def linguist(path: Path, rtype: bool = False) -> Union[str, List[Tuple[str, str]]]:
    if not EXE:
        raise ImportError("GitHub Linguist not found, did you install it per README?")
    path = Path(path).expanduser()
    if not checkrepo(path):
        return None
    ret = subprocess.check_output([EXE, str(path)], universal_newlines=True).split("\n")
    return ret


def checkrepo(path: Path) -> bool:
    if not GIT:
        raise ImportError("Git not found")
    path = Path(path).expanduser()
    if not (path / ".git").is_dir():
        logging.error(f'{path} Linguist only works on files after "git commit"')
        return False
    ret = subprocess.check_output([GIT, "status", "--porcelain"], cwd=path, universal_newlines=True)
    add = {"A", "?"}
    mod = "M"
    for line in ret.split("\n"):
        L = line.split()
        if not L:
            continue
        if add.intersection(L[0]) or (mod in L[0] and L[1] == ".gitattributes"):
            logging.warning(f'{path} Linguist only works on files after "git commit"')
            return False
    return True


def get_microservice_lang(url):
    try:
        project_folder = "get_microservice_type_temp_" + time.strftime("%Y%m%d-%H%M%S")
        Repo.clone_from(url, project_folder)
        lang = linguist(project_folder)[0].split()[2]
        shutil.rmtree(project_folder, ignore_errors=True)
        return lang
    except:
        return False
