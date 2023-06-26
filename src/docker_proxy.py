import docker


class DockerProxy():
    def __init__(self):
        self.client = docker.from_env()
    
    def pull_docker_image(self, docker_image):
           imageobj = self.client.images.pull(docker_image)
           return imageobj

    def run_docker_container(self, image, name, volumes):
        container = self.client.containers.run(
            image=image,
            command='bash',
            name=name,
            volumes=volumes,
            privileged=True,
            tty=True,
            detach=True
        )
        return container
    
    def container_exec_command(self, container, command, workspace):
        resp = container.exec_run(
            cmd=command,
            user='root',
            workdir=workspace,
            stderr=True,
            stdout=True,
        )
        return resp

    def container_destory(self, container):
        container.stop()
        container.remove(v=True)

    def get_container(self, container_id):
        containerobj = self.client.containers.get(container_id)
        return containerobj