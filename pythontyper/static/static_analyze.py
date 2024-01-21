import ast
import os
import shutil
import subprocess

from static.utils import *
from static.fuse import *

def pytype():
    #move into repo directory
    # copy_files_to_repo(base_dir, "./repo")
    try:
        shutil.rmtree("./.pytype")
    except:
        pass
    #call pytype
    subprocess.run(["pytype", "--config=pytype.toml"])


file_mapping_pyi_to_py = {}
file_mapping_py_to_pyi = {}

def pypyimap():
    #map pyi to py file, find the unannotated types in each file
    file_mapping_pyi_to_py = {}
    file_mapping_py_to_pyi = {}
    pyi_root = "./.pytype/pyi/repo"
    py_root = "./repo"
    for root, dirs, files in os.walk("./.pytype/pyi/repo"):
        for file in files:
            if file.endswith(".pyi"):
                pyi_path = os.path.join(root, file)
                rel_path = os.path.relpath(pyi_path, pyi_root)
                py_path = os.path.join(py_root, rel_path)
                filename = os.path.basename(pyi_path)
                py_name = filename.split(".")[0] + ".py"
                py_path = os.path.join(os.path.dirname(py_path), py_name)
                print("mapping: {} To {}".format(pyi_path, py_path))
                file_mapping_pyi_to_py[pyi_path] = py_path
                file_mapping_py_to_pyi[py_path] = pyi_path

    return file_mapping_pyi_to_py, file_mapping_py_to_pyi


def find_unannotated_vars(py_file, pyi_file):
    unannotated_vars = []

    with open(py_file, 'r') as file:
        py_tree = ast.parse(file.read(), filename=py_file)

    with open(pyi_file, 'r') as file:
        pyi_tree = ast.parse(file.read(), filename=pyi_file)

    for node in ast.walk(py_tree):
        if is_variable(node):
            print(node.id)
        
    # pyi_vars = {node.id for node in ast.walk(pyi_tree) if isinstance(node, ast.AnnAssign) and node.annotation is not None}

    # unannotated_vars = py_vars - pyi_vars

    # return unannotated_vars

def hityper():
    try:
        os.remove("./._repo_INFERREDTYPES.json")
    except:
        pass
    subprocess.run(["hityper", "infer", "-p", "./repo"])


def static_analyze():
    
    pytype()

    # file_mapping_pyi_to_py, file_mapping_py_to_pyi = pypyimap()
    # for pyi_file, py_file in file_mapping_pyi_to_py.items():
    #     if not "versioneer" in pyi_file:
    #         continue
    #     unannotated_vars = find_unannotated_vars(py_file, pyi_file)
    #     print(unannotated_vars)
    #     print(pyi_file)
    #     print(py_file)
    #     print()
    #     break

    hityper()
    fuse()
    # markUnannotated()