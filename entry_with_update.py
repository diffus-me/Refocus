import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.append(str(root))
os.chdir(root)

bupdated = False
try:
    import pygit2

    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    repo_path = Path(__file__).resolve().parent
    repo = pygit2.Repository(str(repo_path))

    branch_name = repo.head.shorthand

    remote_name = "origin"
    remote = repo.remotes[remote_name]

    remote.fetch()

    local_branch_ref = f"refs/heads/{branch_name}"
    local_branch = repo.lookup_reference(local_branch_ref)

    remote_reference = f"refs/remotes/{remote_name}/{branch_name}"
    remote_commit = repo.revparse_single(remote_reference)

    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("You have the latest version")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Updating Files")
        bupdated = True
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed,  Did you modify any files?")
except Exception as e:
    print("Update failed...")
    print(str(e))


def main():
    if bupdated:
        print("Update succeeded!!")
    import launch
    launch.launch()


if __name__ == '__main__':
    main()
