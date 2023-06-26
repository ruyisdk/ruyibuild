import git

class GitProxy:
    def clone_git_repo(self, local_repo_dir, repo_url, repo_branch):
        repo = git.Repo.clone_from(url=repo_url, to_path=local_repo_dir, branch=repo_branch, multi_options=['--depth=1'], progress=Progress())
        if len(repo.submodules) > 0:
            output = repo.git.submodule('update', '--init')
        

class Progress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)