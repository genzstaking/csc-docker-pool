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


def check_relay_node_initialized(relay):
    _logger.info("Check the node folder {}".format(relay.path))
    if not relay.is_initialized:
        _logger.critical(msg="Node is not initialized! use `csc-docker-pool relay --name {} init`  to initialize the node.".format(relay.name))
        exit(1)


def load_docker():
    _logger.info("Loading docker from environment")
    try:
        client = docker.from_env()
    except:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)
    return client


def redirect_container_logs(container, args):
    if args.loglevel in [ logging.DEBUG, logging.INFO ]:
        process = container.logs(stream=True, follow=True)
        for lines in process:
            for line in codecs.decode(lines).splitlines():
                _logger.info(" container>" + line)


def generate_data_dir_options(relay, args):
    return "--datadir /root"


def generate_bootnodes_options(relay, args):
    options = ""
    if 'bootnodes' in args and args.bootnodes != None:
        options = "--bootnodes " + ",".join(args.bootnodes)
    elif relay.bootnodes != None:
        options = "--bootnodes " + ",".join(args.bootnodes)
    return options


def generate_syncmod_options(relay, args):
    options = ""
    if 'syncmod' in args:
        options = "--syncmod " + args.syncmod[0]
    return options


def generate_metrics_options(relay, args):
    """
    Enables metrics options of the node
    """
    options = ""
    
    # runtime options are much more important
    src = relay
    if args.metrics is not None:
        src = args
    
    if src.metrics == "none":
        _logger.info("Metric is disabled")
    elif src.metrics == "influxdb":
        _logger.info("Metrics well be reported to an InfluxDB")
        options = """
            --metrics 
            --metrics.influxdb
            --metrics.influxdb.endpoint  "{}" 
            --metrics.influxdb.database  "{}" 
            --metrics.influxdb.username  "{}" 
            --metrics.influxdb.password  "{}"
            --metrics.influxdb.tags      "{}"
        """.format(
            src.metrics_influxdb_endpoint,
            src.metrics_influxdb_database,
            src.metrics_influxdb_username,
            src.metrics_influxdb_password,
            "host=" + generate_relay_name(relay))
    else:
        _logger.error("We just support influxdb report")
        exit(2)
    return options

def generate_relay_name(relay):
    return "csc_relay_" + relay.name + "_" + relay.id
    
def handle_relay(args):
    _logger.info("Start handling relay command")
    
    print('relay handler')


def handle_relay_init(args):
    _logger.info("Start handling relay init command")
    client = load_docker()
    
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
    relay = create_relay_node(path)
    if relay.is_initialized:
        _logger.critical(msg="Node {} was initialized before. Remove node and init it again.".format(args.name))
        exit(1)
    
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(args.name))
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[relay.path + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
        detach=True,
    )
    redirect_container_logs(container, args)
    
    _logger.info("Node {} is initialized with default configuration".format(args.name))
    relay.is_initialized = True
    relay.network = args.network[0]
    relay.name = args.name
    relay.id = str(random.randint(100000000, 1000000000))
    # Metrics (simple copy)
    relay.metrics = args.metrics
    relay.metrics_influxdb_endpoint = args.metrics_influxdb_endpoint
    relay.metrics_influxdb_database = args.metrics_influxdb_database
    relay.metrics_influxdb_username = args.metrics_influxdb_username
    relay.metrics_influxdb_password = args.metrics_influxdb_password
    relay.save()


def handle_relay_run(args):
    _logger.info("Running the relay node {}".format(args.name))
    
    relay = create_relay_node(os.getcwd() + '/' + args.name)
    check_relay_node_initialized(relay)
    client = load_docker()
        
    options = "".join([
        generate_data_dir_options(relay, args),
        generate_bootnodes_options(relay, args),
        generate_syncmod_options(relay, args),
        generate_metrics_options(relay, args)
    ])

    _logger.info("Running ghcr.io/genz-bank/cetd container for node {}".format(args.name))
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        name= generate_relay_name(relay),
        user=os.getuid(),
        volumes=[relay.path + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
        detach=True,
    )
    relay.save()
    redirect_container_logs(container, args)


def handle_relay_list(args):
    root_path = os.getcwd()
    nodes = [ create_relay_node(f.path).__dict__ for f in os.scandir(root_path) if f.is_dir() and is_relay_node(f.path) ]
    frame = pandas.DataFrame(nodes, columns=['id', 'name', 'network', 'is_initialized'])
    print(frame)

def parse_args(subparsers):
    parser = subparsers.add_parser(
        'relay',
        help='Manages a relay node'
    )
    relay_parser = parser.add_subparsers(
        title="Relay Nodes Management",
        description="""
        A relay node sync DB with the network.
        On the other hand, a relay node is an edge node and connects to other nodes on the
        network. It fetch/push new blocks and keeps the ledger update.
        This command helps you to setup, manage and maintain a node over the network.
        You may have multiple relay node at the same time, where each of which deals with 
        and specific network. For example a node to keeps testnet data."""
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
    subparsers_init.add_argument(
        '--name',
        help='target wallet name',
        dest='name',
        default='main'
    )
    
    subparsers_init.add_argument(
        '--metrics',
        help='This option enables the reporting system.',
        default='none',
        type=str,
        choices=['none', 'influxdb'],
        required=False,
        dest='metrics'
    )
    subparsers_init.add_argument(
        '--metrics.influxdb.endpoint',
        help='The address of the InfluxDB server, e.g. http://localhost:8086.',
        type=str,
        required=False,
        dest='metrics_influxdb_endpoint',
        default='http://localhost:8086'
    )
    subparsers_init.add_argument(
        '--metrics.influxdb.database',
        help='The name of database in InfluxDB.',
        type=str,
        required=False,
        dest='metrics_influxdb_database',
        default='csc'
    )
    subparsers_init.add_argument(
        '--metrics.influxdb.username',
        help='InfluxDB username.',
        type=str,
        required=False,
        dest='metrics_influxdb_username',
        default='csc'
    )
    subparsers_init.add_argument(
        '--metrics.influxdb.password',
        help='InfluxDB password.',
        type=str,
        required=False,
        dest='metrics_influxdb_password'
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
    subparsers_run.add_argument(
        '--bootnodes',
        help='Comma separated enode URLs for P2P discovery bootstrap',
        nargs=1,
        type=str,
        required=False,
        dest='bootnodes'
    )
    
    subparsers_run.add_argument(
        '--metrics',
        help='This option enables the reporting system.',
        default=None,
        type=str,
        choices=['none', 'influxdb'],
        required=False,
        dest='metrics'
    )
    subparsers_run.add_argument(
        '--metrics.influxdb.endpoint',
        help='The address of the InfluxDB server, e.g. http://localhost:8086.',
        type=str,
        required=False,
        dest='metrics_influxdb_endpoint',
        default='http://localhost:8086'
    )
    subparsers_run.add_argument(
        '--metrics.influxdb.database',
        help='The name of database in InfluxDB.',
        type=str,
        required=False,
        dest='metrics_influxdb_database',
        default='csc'
    )
    subparsers_run.add_argument(
        '--metrics.influxdb.username',
        help='InfluxDB username.',
        type=str,
        required=False,
        dest='metrics_influxdb_username',
        default='csc'
    )
    subparsers_run.add_argument(
        '--metrics.influxdb.password',
        help='InfluxDB password.',
        type=str,
        required=False,
        dest='metrics_influxdb_password'
    )
    #----------------------------------------------------------
    # list
    #----------------------------------------------------------
    subparsers_lsit = relay_parser.add_parser(
        'list',
        help='To display list of created relay nodes'
    )
    subparsers_lsit.set_defaults(func=handle_relay_list)

