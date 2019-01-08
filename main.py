from github import Github
import json
import io
import os
import shutil
from time import gmtime, strftime
from git import Repo
from git import Actor

github_access_token = os.environ['GITHUB_ACCESS_TOKEN']

config = json.load(open("./config.json"))
ansible_repo_path = config["ansible_repo_path"]
azure_repo_path = config["azure_repo_path"]
sha_file_path = config["sha_file_path"]
repo_mapping_file_path = config["repo_mapping_file_path"]

local_azure_repo = None
new_branch_name = None


def get_latest_commit_sha(repo, branch, path):
    commits = repo.get_commits(sha=branch, path=path)
    page = commits.get_page(0)
    if len(page) > 0:
        return page[0].sha
    else:
        return None


def clone_azure_repo():
    print "Clone Azure repo to " + azure_repo_path
    create_clean_dir(azure_repo_path)
    global local_azure_repo
    azure_repo = Repo()
    local_azure_repo = azure_repo.clone_from("https://ansibleazurebot:" + github_access_token + "@github.com/Azure/azure_preview_modules.git", azure_repo_path)


def has_new_content(repo, branch_name, log_file):
    clone_azure_repo()
    commit_history = json.load(open(log_file))
    for path, sha in commit_history.iteritems():
        new_sha = get_latest_commit_sha(repo, branch_name, path)
        if sha != new_sha:
            return True
    return False


def ansible_repo_has_new_content():
    g = Github(github_access_token)
    ansible_org = g.get_organization("ansible")
    remote_ansible_repo = ansible_org.get_repo("ansible")
    return has_new_content(remote_ansible_repo, config["ansible_default_branch"], sha_file_path)


def save_back_to_json(data, file_name):
    print "Save data to " + file_name
    with io.open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False))


def create_clean_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def clone_ansible_repo():
    print "Clone Ansible repo to " + ansible_repo_path
    create_clean_dir(ansible_repo_path)
    ansible_repo = Repo()
    ansible_repo.clone_from("https://github.com/ansible/ansible.git", ansible_repo_path)


def copy(path):
    full_path = os.path.join(ansible_repo_path, path)
    if os.path.isdir(full_path):
        copy_folder(path)
    else:
        copy_file(path)


def get_joined_path(ansible_path):
    repo_map = json.load(open(repo_mapping_file_path))
    azure_path = repo_map[ansible_path]

    src = os.path.join(ansible_repo_path, ansible_path)
    dest = os.path.join(azure_repo_path, azure_path)

    return src, dest


def copy_file(path):
    print "Copy file " + path
    src, dest = get_joined_path(path)
    shutil.copy(src, dest)


def copy_folder(path):
    print "Copy folder " + path
    if config["special_src_folder_path"] in path:
        copy_folder_specially(path)
    elif config["not_overwrite_copy"] in path:
        copy_folder_non_overwrite(path)
    else:
        copy_folder_normally(path)


def copy_folder_normally(path):
    src, dest = get_joined_path(path)
    shutil.rmtree(dest)
    shutil.copytree(src, dest)


def copy_folder_non_overwrite(path):
    src, dest = get_joined_path(path)
    for name in os.listdir(src):
        src_file_name = os.path.join(src, name)
        dest_file_name = os.path.join(dest, name)
        if os.path.isfile(dest_file_name):
            shutil.copy(src_file_name, dest_file_name)
        if not os.path.exists(dest_file_name):
            shutil.copy(src_file_name, dest_file_name)

def copy_folder_specially(path):
    src, dest = get_joined_path(path)
    for dir_name in os.listdir(src):
        src_dir_path = os.path.join(src, dir_name)
        dest_dir_path = os.path.join(dest, dir_name)
        if os.path.isdir(src_dir_path) and config["test_case_folder_prefix"] in dir_name:
            if os.path.isdir(dest_dir_path):
                shutil.rmtree(dest_dir_path)
                shutil.copytree(src_dir_path, dest_dir_path)
            if not os.path.exists(dest_dir_path):
                shutil.copytree(src_dir_path, dest_dir_path)


def check_out_new_branch():
    global new_branch_name
    new_branch_name = "integration-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    print "Create new branch " + new_branch_name
    local_azure_repo.git.checkout('HEAD', b=new_branch_name)


def copy_changed_files():
    print "Copy changes"
    g = Github(github_access_token)
    ansible_org = g.get_organization("ansible")
    remote_ansible_repo = ansible_org.get_repo("ansible")
    commit_history = json.load(open(sha_file_path))

    changed = False
    for path, sha in commit_history.iteritems():
        new_sha = get_latest_commit_sha(remote_ansible_repo, "devel", path)
        if sha != new_sha:
            copy(path)
            changed = True
            commit_history[path]=new_sha

    if changed:
        save_back_to_json(commit_history, sha_file_path)


def push_changes_to_remote():
    print "Commit and push changes to remote"
    local_azure_repo.git.add(A=True)
    author = Actor(config["author"], config["mail"])
    committer = Actor(config["author"], config["mail"])
    local_azure_repo.index.commit("Merged changes of Azure modules from Ansible repo", author=author, committer=committer)
    refspec = new_branch_name+":"+new_branch_name
    local_azure_repo.remotes.origin.push(refspec=refspec)


def send_pull_request():
    print "Send pull request"
    g = Github(github_access_token)
    azure_org = g.get_organization("Azure")
    remote_azure_repo = azure_org.get_repo("azure_preview_modules")
    pr = remote_azure_repo.create_pull("[Automated Integration]Merge Azure module changes from Ansible repo",
                                       config["alias"], config["azure_default_branch"], new_branch_name)
    print "Created PR: " + pr.url


def migrate_contents():
    clone_ansible_repo()
    check_out_new_branch()
    copy_changed_files()
    push_changes_to_remote()
    send_pull_request()


def main():
    print "Starting..."

    if not ansible_repo_has_new_content():
        print "No new content. Exiting..."
        return
    else:
        print "Migrate content from Ansible repo to Azure modules repo"

    migrate_contents()


if __name__ == "__main__":
    main()
