import os
import git
import shutil
from log import logger
import util as ruyibuild_util
from docker_proxy import DockerProxy
from git_proxy import GitProxy


class Update:

    def run(self):
        config_dir = f'{os.getcwd()}/.ruyibuild/config.yaml'
        config_data = ruyibuild_util.read_yaml(config_dir)
        #print ('config_data', config_data)
        
        #### pull docker image
        try:
            docker_image = config_data['docker']['repo_url'] + ':' + config_data['docker']['tag']
            # print ('docker_image', docker_image)
            docker_image_obj = self.pull_dockerimage(docker_image)
            logger.info(f'docker pull {docker_image} successful')
        except Exception as e:
            logger.error('Cannot find docker image, please confirm docker info in config file')
            raise e
        
        #### download sourcecode
        try:
            src_local_dir = f'{os.getcwd()}/src'
            self.download_sourcecode(src_local_dir, config_data['basic_repo']['repo_url'], config_data['basic_repo']['branch'])
            logger.info('clone {} successful'.format(config_data['basic_repo']['repo_url']))
        except Exception as e:
            logger.error('clone {} failed'.format(config_data['basic_repo']['repo_url']))
            raise e

        #### download build script
        try:
            build_local_dir = f'{os.getcwd()}/script'
            self.download_sourcecode(build_local_dir, config_data['build_script']['repo_url'], config_data['build_script']['branch'])
            logger.info('clone {} successful'.format(config_data['build_script']['repo_url']))
        except Exception as e:
            logger.info('clone {} failed'.format(config_data['build_script']['repo_url']))
            raise e
        
        prompt_msg = f'''
    please execute the follow commands next in the current directory:\n
    ruyibuild generate [<name>]
        '''        
        print (prompt_msg)

    def pull_dockerimage(self, image):
        client = DockerProxy()
        print (f'docker pull {image} ......')
        imageobj = client.pull_docker_image(image)
        return imageobj
    
    def download_sourcecode(self, local_dir, repo_url, repo_branch):
        if os.listdir(local_dir):
            try:
                shutil.rmtree(local_dir)
                os.mkdir(local_dir)
            except Exception as e:
                logger.error('{} directory is not empty'.format(os.path.split(local_dir)[1]))
                raise e
        repo_git = GitProxy()
        repo_git.clone_git_repo(local_dir, repo_url, repo_branch)
