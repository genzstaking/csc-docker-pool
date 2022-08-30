import logging
import docker
import os
import codecs
from builtins import IOError, FileNotFoundError
import time
import pandas
import random
_logger = logging.getLogger(__name__)


def get_option_value(node, args, key, required=False):
    val = node.get(key)
    if hasattr(args, key):
        arg_val = getattr(args, key)
        if arg_val:
            val = arg_val
    if required and not val:
        raise RuntimeError(msg="""
        The parameter with name {} is required but defined 
        neither in the node nor in the args.
        """.format(key))
    return val


def generate_staking_options(node, args):
    
    #   --from 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec  
    #   --validator.rewardaddr 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
    options += "--validator.moniker {} ".format(node.label) 
    options += "--validator.website {} ".format(node.website) 
    options += "--validator.email {} ".format(node.email)
    options += "--validator.detail {} ".format(node.description) 


def generate_relay_options(node, args):
    #   --node http://127.0.0.1:8545
    host = "localhost"
    port = "8545"
    return "--node http://{}:{} ".format(host, port)


#------------------- Data director -----------------------
def generate_data_dir_options(node, args):
    """ Add a data directory path
    
    The current directory path is mounted to the /root directory and
    is used as data directory.
    """
    return "--datadir /root "


def generate_node_dir_options(node, args):
    name = node.name
    if args.name:
        name = args.name
    root_path = os.getcwd() + "/" + name
    if not os.path.isdir(root_path):
        os.mkdir(root_path)
    return "--datadir /root/{} ".format(args.name)


#----------------------- Chain    -----------------------
def add_chain_arguments(parser):
    """
    Chain arguments are used in relay node
    """
    parser.add_argument(
        '--network',
        help='The name of the network (main, or test)',
        default='main',
        type=str,
        choices=['main', 'test'],
        required=False,
        dest='network'
    )
    parser.add_argument(
        '--port',
        help='Network listening port',
        default='36652',
        type=str,
        required=False,
        dest='port'
    )


def generate_chain_options(node, args):
    options = []
    net_type = get_option_value(node, args, 'network')
    if net_type == 'test':
        options.append(" --testnet ")
    elif net_type == "main":
        options.append(" ")
    else:
        raise RuntimeError(msg="""
            The type {} is not supported.
        """.format(net_type))
    options.append(" --port ")
    options.append(get_option_value(node, args, 'port'))
    return "".join(options)


###########################################################################
#                           Logger
#
###########################################################################
def generate_logging_options(node, args):
    if node.loglevel in [logging.INFO, logging.DEBUG]:
        return " --debug " 
    return ""


###########################################################################
#                           Boot Options
#
###########################################################################
def add_bootnodes_arguments(parser):
    parser.add_argument(
        '--bootnodes',
        help='Comma separated enode URLs for P2P discovery bootstrap',
        nargs=1,
        type=str,
        required=False,
        dest='bootnodes'
    )


def generate_bootnodes_options(node, args):
    options = ""
    if 'bootnodes' in args and args.bootnodes != None:
        options = "--bootnodes " + ",".join(args.bootnodes)
    elif node.bootnodes != None:
        options = "--bootnodes " + ",".join(args.bootnodes)
    return options


###########################################################################
#                           Sync Options
#
###########################################################################
def add_syncmode_arguments(parser):
    parser.add_argument(
        '--syncmode',
        help='Sets the mode in DB sync (full, ..)',
        nargs=1,
        default='fast',
        type=str,
        choices=['fast', 'full', 'light'],
        required=False,
        dest='network'
    )


def generate_syncmod_options(node, args):
    options = ""
    if 'syncmod' in args:
        options = "--syncmod " + args.syncmod[0]
    return options


###########################################################################
#                           Metrics
#
###########################################################################
def add_metric_arguments(parser):
    """ Adds metric arguments to the parser
    
    These are our common metric argumetns used to enable monitoring.
    
    @param parser: A argsparser
    """
    parser.add_argument(
        '--metrics',
        help='This option enables the reporting system.',
        default=None,
        type=str,
        choices=['none', 'influxdb'],
        required=False,
        dest='metrics'
    )
    parser.add_argument(
        '--metrics.influxdb.endpoint',
        help='The address of the InfluxDB server, e.g. http://localhost:8086.',
        type=str,
        required=False,
        dest='metrics_influxdb_endpoint',
        default='http://localhost:8086'
    )
    parser.add_argument(
        '--metrics.influxdb.database',
        help='The name of database in InfluxDB.',
        type=str,
        required=False,
        dest='metrics_influxdb_database',
        default='csc'
    )
    parser.add_argument(
        '--metrics.influxdb.username',
        help='InfluxDB username.',
        type=str,
        required=False,
        dest='metrics_influxdb_username',
        default='csc'
    )
    parser.add_argument(
        '--metrics.influxdb.password',
        help='InfluxDB password.',
        type=str,
        required=False,
        dest='metrics_influxdb_password'
    )

    
def generate_metrics_options(node, args):
    """Enables metrics options of the node
    
    @param realy node to load options from
    """
    options = ""
    
    # runtime options are much more important
    src = node
    if args.metrics is not None:
        src = args
    
    if src.metrics == "none" or src.metrics is None:
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
            "host=" + generate_relay_name(node))
    else:
        raise RuntimeError("""
            Metrics methods {} is not supported in current version.
            We just support influxdb report right now.
            """.format(src.metrics))
    return options


###########################################################################
#                           RPC
#
###########################################################################
def generate_rpc_http_options(node, args):
    """
    Here is list of options supported by ETCH
    
        --http                              Enable the HTTP-RPC server
        --http.addr value                   HTTP-RPC server listening interface (default: "localhost")
        --http.port value                   HTTP-RPC server listening port (default: 8545)
        --http.api value                    API's offered over the HTTP-RPC interface
        --http.corsdomain value             Comma separated list of domains from which to accept cross origin requests (browser enforced)
        --http.vhosts value                 Comma separated list of virtual hostnames from which to accept requests (server enforced). Accepts '*' wildcard. (default: "localhost")
    """
    return """
        --http 
        --http.port 8545 
        --http.vhosts localhost,{}
        """.format(generate_relay_name(node))


###########################################################################
#                           Name
#
###########################################################################
def add_name_arguments(parser):
    parser.add_argument(
        '--name',
        help='target wallet name',
        dest='name',
        default='main'
    )


def generate_relay_name(node, args=None):
    return "csc_relay_" + node.name + "_" + node.id


def generate_staking_name(node, args=None):
    return "csc_validator_" + node.name + "_" + node.id


#--------------------------- Keystore password file --------------------------
def add_password_file_arguments(parser):
    parser.add_argument(
        '--password',
        help='The password that protect keystore',
        type=str,
        required=True,
        dest='password',
    )


def generate_passowrd_file_options(node, args):
    name = get_option_value(node, args, 'name', required=True)
    with open("{}/{}/password.txt".format(os.getcwd(), name), 'w') as f:
        f.write(args.password)
    return "--password /root/{}/password.txt ".format(name)


#--------------------------- Key file --------------------------
def add_keyfile_arguments(parser):
    parser.add_argument(
        '--keyfile',
        help='The keyfile is assumed to contain an unencrypted private key in hexadecimal format.',
        type=str,
        required=True,
        dest='keyfile',
    )
    

def generate_keystore_options(node, args):
    #   --keystore ./data/keystore/
    path = "./data/keystore/"
    return " --keystore {} ".format(path)
