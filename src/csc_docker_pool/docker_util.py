import logging
import docker
import os
import codecs
from builtins import IOError, FileNotFoundError
import time
import pandas
import random

_logger = logging.getLogger(__name__)


def load_docker():
    _logger.info("Loading docker from environment")
    try:
        client = docker.from_env()
    except:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)
    return client

def docker_is_running(container_name):
    """
    verify the status of a sniffer container by it's name
    :param container_name: the name of the container
    :return: Boolean if the status is ok
    """
    client = load_docker()
    try:
        container = client.containers.get(container_name)
        container_state = container.attrs['State']
        return container_state['Status'] == "running"
    except docker.errors.NotFound:
        return False
    except docker.errors.APIError:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)

def redirect_container_logs(container, args):
    if args.loglevel in [ logging.DEBUG, logging.INFO ]:
        process = container.logs(stream=True, follow=True)
        for lines in process:
            for line in codecs.decode(lines).splitlines():
                _logger.info(" container>" + line)


