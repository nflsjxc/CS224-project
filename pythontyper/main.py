import static
import shutil
import os
import argparse

def copy_files_to_repo(base_diretory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    #remove all files in ./repo
    shutil.rmtree(destination_directory)

    # move all the file in file_paths to destination_directory
    shutil.copytree(base_diretory, destination_directory)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Static Analysis and File Copy Script")
    parser.add_argument("--repo", "-r", required=True, help="Repo source directory")
    # parser.add_argument("--mode", "-m", default="all", help="Analyze mode")

    args = parser.parse_args()

    # base_dir = "./toBeAnalyzed/api"
    base_dir = args.repo
    copy_files_to_repo(base_dir, "./repo")

    print("===================STATIC ANALYZE====================")
    static.static_analyze()

    print("===================CLEAR FILE====================")
    shutil.rmtree("./repo")
    os.mkdir("./repo")