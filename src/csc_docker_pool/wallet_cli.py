import logging
import docker
import os
import codecs
from builtins import IOError, FileNotFoundError
from csc_docker_pool.relay import is_relay_node, create_relay_node
import time
import pandas
import random

_logger = logging.getLogger(__name__)


def redirect_container_output(container):
    process = container.logs(stream=True, follow=True)
    for lines in process:
        for line in codecs.decode(lines).splitlines():
            print(line)
    
def redirect_container_logs(container, args):
    if args.loglevel in [ logging.DEBUG, logging.INFO ]:
        process = container.logs(stream=True, follow=True)
        for lines in process:
            for line in codecs.decode(lines).splitlines():
                _logger.info(" container>" + line)


def load_docker():
    _logger.info("Loading docker from environment")
    try:
        client = docker.from_env()
    except:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)
    return client


def generate_data_dir_options(args):
    root_path = os.getcwd() + "/" + args.name
    if not os.path.isdir(root_path):
        os.mkdir(root_path)
    return "--datadir /root/{} ".format(args.name)

def generate_passowrd_file_options(args):
    with open("{}/{}/password.txt".format(os.getcwd(), args.name), 'w') as f:
        f.write(args.password)
    return "--password /root/{}/password.txt ".format(args.name)
    

def handle_wallet_list(args):
    _logger.info("Start handling relay init command")
    client = load_docker()
    _logger.info("Getting list of wallets (accounts) in node {}".format(args.name))
    # Command options
    options = "".join([
        "account  list ",
        generate_data_dir_options(args)
    ])
    
    _logger.info("Running ghcr.io/genz-bank/cetd container to list accounts")
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[os.getcwd() + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
        detach=True,
    )
    redirect_container_output(container)

def handle_wallet_new(args):
    _logger.info("Start handling relay init command")
    client = load_docker()
    _logger.info("Getting list of wallets (accounts) in node {}".format(args.name))
        
    # Command options
    options = "".join([
        "account  new ",
        generate_data_dir_options(args),
        generate_passowrd_file_options(args),
    ])
    
    _logger.info("Running ghcr.io/genz-bank/cetd container to list accounts")
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[os.getcwd() + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
        detach=True,
    )
    redirect_container_logs(container, args)
    
def parse_args(subparsers):
    #----------------------------------------------------------
    # Wallet
    #----------------------------------------------------------
    parser = subparsers.add_parser(
        'wallet',
        help='Manages wallets/accounts.'
    )

    wallet_parser = parser.add_subparsers(
        title="Wallet Management",
        description="""
        In CSC network wallets are called account so. This command manage list of accounts.
        """
    )
    
    #----------------------------------------------------------
    # list
    #----------------------------------------------------------
    wallet_lsit = wallet_parser.add_parser(
        'list',
        help='To display list of created wallets'
    )
    wallet_lsit.add_argument(
        '--name',
        help='The name of a node (in each node there are many wallets)',
        dest='name',
        default='main'
    )
    
    wallet_lsit.set_defaults(func=handle_wallet_list)
    
    
    #----------------------------------------------------------
    # new
    #----------------------------------------------------------
    wallet_new = wallet_parser.add_parser(
        'new',
        help='To create a new wallets'
    )
    wallet_new.add_argument(
        '--name',
        help='The name of a node (in each node there are many wallets)',
        dest='name',
        default='main'
    )
    wallet_new.add_argument(
        '--password',
        help='The password that protect keystore',
        type=str,
        required=True,
        dest='password',
    )
    wallet_new.set_defaults(func=handle_wallet_new)
