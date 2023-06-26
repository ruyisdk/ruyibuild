import os
import shutil
from log import logger
import util as ruyibuild_util
from git_proxy import GitProxy


class Init:

    def __init__(self):
        self.ruyibuild_dir = None
        self.src_dir = None
        self.build_dir = None
        self.script_dir = None

    def run(self, workspace_dir, yaml_dir=None):
        self.create_workspace_dir(workspace_dir, yaml_dir)

    def create_workspace_dir(self, directory, yaml_directory):
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except Exception as e:
                logger.error(e)
                raise (e)
        try:
            os.mkdir(directory)
            self.create_src_dir(directory)
            self.create_build_dir(directory)
            self.create_script_dir(directory)
            self.create_ruyibuild_dir(directory)
            if yaml_directory:
                self.clone_config_file(self.ruyibuild_dir, yaml_directory)
            else:
                self.copy_config_file(self.ruyibuild_dir)
            os.chdir(directory)
            prompt_msg = f'''
    please execute the follow commands next:\n
    cd {os.getcwd()}\n
    ruyibuild update
    '''       
            logger.info(f'init workspace {directory} successful')
            print (prompt_msg)
        except Exception as e:
            logger.error(f'init workspace {directory} failed')
            raise (e)

    def create_ruyibuild_dir(self, updir):
        self.ruyibuild_dir = os.path.join(updir, '.ruyibuild')
        os.mkdir(self.ruyibuild_dir)
    
    def create_src_dir(self, updir):
        self.src_dir = os.path.join(updir, 'src')
        os.mkdir(self.src_dir)

    def create_build_dir(self, updir):
        self.build_dir = os.path.join(updir, 'build')
        os.mkdir(self.build_dir)
    
    def create_script_dir(self, updir):
        self.script_dir = os.path.join(updir, 'script')
        os.mkdir(self.script_dir)
    
    def copy_config_file(self, updir):
        config_dir = ruyibuild_util.get_config_yaml_dir()
        shutil.copyfile(config_dir, os.path.join(updir, 'config.yaml'))
    
    def clone_config_file(self, updir, file_dir):
        git_dir = os.path.join(updir, 'git')
        os.mkdir(git_dir)
        ruyicfg_data = ruyibuild_util.read_yaml(file_dir)
        repo_git = GitProxy()
        repo_git.clone_git_repo(git_dir, ruyicfg_data['config_file']['repo_url'], ruyicfg_data['config_file']['branch'])
        config_file_dir = os.path.join(git_dir, ruyicfg_data['config_file']['path'])
        shutil.copyfile(config_file_dir, os.path.join(updir, 'config.yaml'))




