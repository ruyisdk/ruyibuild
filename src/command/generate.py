import os
import time
import shutil
import tarfile
import subprocess
import sys
from log import logger
import util as ruyibuild_util
from docker_proxy import DockerProxy


class Generate:
    def __init__(self):
       self.config_dir = f'{os.getcwd()}/.ruyibuild/config.yaml'
       self.client = DockerProxy()

    def run(self, output_dir=None):
        if not os.path.exists(f'{os.getcwd()}/build'):
            os.mkdir('build')
        if not os.path.exists(f'{os.getcwd()}/src'):
            logger.error(f'cannot find the directory: {os.getcwd()}/src')
            sys.exit(1)
        if len(os.listdir(f'{os.getcwd()}/src')) == 0:
            logger.error(f'The directory {os.getcwd()}/src is empty')
            sys.exit(1)
        config_data = ruyibuild_util.read_yaml(self.config_dir)
        container_obj = self.run_container(config_data)
        time.sleep(3)
        
        if output_dir:
            container = self.client.get_container(container_obj.id)
            self.create_outputdir(container, output_dir)
            result = self.execute_script(config_data, container, output_dir)
            self.chmod_directory(container)
            if result == 0:
                self.compress_output(output_dir)
                self.delete_directory()
            else:
                logger.error('package build failed')
            self.destory_container(container)
        else:
            command = f'docker exec -it {container_obj.id} /bin/bash'
            os.system(command)
    

    def run_container(self, config_data):
        container_name = self.create_container_name()
        container_volumes = [
            f'{os.getcwd()}/src:/home/src',
            f'{os.getcwd()}/build:/home/build',
            f'{os.getcwd()}/script:/home/script'
        ]
        try:
            docker_image = config_data['docker']['repo_url'] + ':' + config_data['docker']['tag']
            container = self.client.run_docker_container(docker_image, container_name, container_volumes)
            logger.info(f'docker run {docker_image} successful')
            return container
        except Exception as e:
            logger.error(f'docker run {docker_image} failed')
            raise e
   
    
    def create_container_name(self):
        container_name = 'ruyibuild-{}'.format(os.path.split(os.getcwd())[1])
        return container_name

    
    def create_outputdir(self, container, directory):
        output_dir = f'{os.getcwd()}/build/{directory}'
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
            except Exception as e:
                self.destory_container(container)
                logger.error(e)
                raise e
        os.mkdir(output_dir)


    def execute_script(self, config_data, container, directory):
        if os.path.split(config_data['build_script']['path'])[0] == '.':
           script_dir = '/home/script/{}'.format(os.path.split(config_data['build_script']['path'])[1])
        else:
            script_dir = '/home/script/{}'.format(config_data['build_script']['path'])
        script_command = f'sh {script_dir} {directory}'
        command = f'docker exec -it {container.id} bash -c "{script_command}"'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline().decode()
            print(line)

        return p.returncode

    
    def destory_container(self, container):
        print (f'container {container.name} is stopping ......')
        try:
           self.client.container_destory(container)
           logger.info(f'destory container {container.name} successful')
        except Exception as e:
            logger.error(f'destory container {container.name} failed')
            raise e


    def compress_output(self, package):
        output_dir = f'{os.getcwd()}/output'
        if not os.path.exists(output_dir):
           os.mkdir(output_dir) 
        build_dir = f'{os.getcwd()}/build/{package}'
        package_dir = f'{os.getcwd()}/output/{package}.tar.gz'
        logger.info('compressing package ......')
        try:
            tar = tarfile.open(package_dir, 'w:gz')
            for root, dir, files in os.walk(build_dir):
                root_ = os.path.relpath(root,start=build_dir)
                for file in files:
                    fullpath = os.path.join(root,file)
                    tar.add(fullpath, arcname=os.path.join(root_,file))
            logger.info(f'Successfully! Package is stored in {os.getcwd()}/output')
        except Exception as e:
            logger.info(f'compress package failed')
            raise e
    
    
    def chmod_directory(self, container):
        resp_build = self.client.container_exec_command(container, 'chmod -R 777 /home/build', '/home')
        if resp_build.exit_code == 0:
            logger.info('chmod build directory successful')
        else:
            logger.error(resp_build.output.decode())
        resp_src = self.client.container_exec_command(container, 'chmod -R 777 /home/src', '/home')
        if resp_src.exit_code == 0:
            logger.info('chmod src directory successful')
        else:
            logger.error(resp_src.output.decode())
        resp_script = self.client.container_exec_command(container, 'chmod -R 777 /home/script', '/home')
        if resp_script.exit_code == 0:
            logger.info('chmod script directory successful')
        else:
            logger.error(resp_script.output.decode())


    def delete_directory(self):
        try:
            shutil.rmtree(f'{os.getcwd()}/build')
            shutil.rmtree(f'{os.getcwd()}/script')
            shutil.rmtree(f'{os.getcwd()}/src')
            shutil.rmtree(f'{os.getcwd()}/.ruyibuild')
        except Exception as e:
            logger.error(e)
            raise (e)
    

    def debug_finish(self):
        container_name = self.create_container_name()
        try:
            container = self.client.get_container(container_name)
        except Exception as e:
            logger.error(e)
            raise (e)
        self.chmod_directory(container)
        self.destory_container(container)
        



