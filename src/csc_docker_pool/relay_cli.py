import logging
import docker
import os
import codecs
from builtins import IOError, FileNotFoundError

_logger = logging.getLogger(__name__)


def handle_relay(args):
    _logger.info("Start handling relay command")
    
    print('relay handler')


def handle_relay_init(args):
    _logger.info("Start handling relay init command")
    
    _logger.debug("Loading docker from environment")
    try:
        client = docker.from_env()
    except:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)
    
    if args.network[0] == 'main':
        options = "--datadir /root {}".format(
            'init'
        )
    else:
        options = "--datadir /root --testnet {}".format(
            'init'
        )
    if args.loglevel in [logging.INFO, logging.DEBUG]:
        options = "--debug " + options 
    _logger.debug("Command cetd {}".format(options))
    
    path = os.getcwd() + '/' + args.name;
    _logger.debug("Check the node folder {}".format(path))
    if os.path.exists(path):
        _logger.critical(msg="Node folder exist ({}). Remove node and init it again.".format(args.name))
        exit(1)
    
    _logger.debug("Create node folder {}".format(path))
    os.mkdir(path)
      
    _logger.info("Running genzbank/cetd container to init node {}".format(args.name))
    output = client.containers.run(
        "genzbank/cetd",
        options,
        user=os.getuid(),
        volumes=[path + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
    )
    for line in codecs.decode(output).splitlines():
        _logger.debug(" container>" + line)
    
    _logger.info("Node {} is initialized with default configuration".format(args.name))



def handle_relay_run(args):
    _logger.info("Running the relay node {}".format(args.name))
    
    _logger.debug("Loading docker from environment")
    try:
        client = docker.from_env()
    except:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)
        
    path = os.getcwd() + '/' + args.name;
    # TODO: convert this part to is_node
    _logger.debug("Check the node folder {}".format(path))
    if not os.path.exists(path):
        _logger.critical(msg="Node folder dose not exist! use `csc-docker-pool relay --name {} init` command.".format(args.name))
        exit(1)
        
    options = "--datadir /root"
    # TODO: maso, 2022: to support --syncmod
    
    _logger.info("Running genzbank/cetd container to init node {}".format(args.name))
    container = client.containers.run(
        "genzbank/cetd",
        options,
        user=os.getuid(),
        volumes=[path + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
        detach=True,
    )
    process = container.logs(stream=True, follow=True)
    for lines in process:
        for line in codecs.decode(lines).splitlines():
            _logger.debug(" container>" + line)
    
    
def parse_args(subparsers):
    parser = subparsers.add_parser(
        'relay',
        help='Manages a relay node'
    )
    relay_parser = parser.add_subparsers(
        title="Manages relay node",
        description="A relay node sync DB with the network. This command help you to manage a node."
    )
    parser.set_defaults(func=handle_relay)
    
    #----------------------------------------------------------
    # init
    #----------------------------------------------------------
    subparsers_init = relay_parser.add_parser(
        'init',
        help='Initialize the relay node'
    )
    subparsers_init.set_defaults(func=handle_relay_init)
    subparsers_init.add_argument(
        '--network',
        help='The name of the network (main, or test)',
        nargs=1,
        default='main',
        type=str,
        choices=['main', 'test'],
        required=False,
        dest='network'
    )
    
    #----------------------------------------------------------
    # run
    #----------------------------------------------------------
    subparsers_run = relay_parser.add_parser(
        'run',
        help='Run the relay node'
    )
    subparsers_run.set_defaults(func=handle_relay_run)
    subparsers_run.add_argument(
        '--name',
        help='target wallet name',
        dest='name',
        default='main'
    )
    subparsers_run.add_argument(
        '--syncmode',
        help='Sets the mode in DB sync (full, ..)',
        nargs=1,
        default='fast',
        type=str,
        choices=['fast', 'full', 'light'],
        required=False,
        dest='network'
    )
    











