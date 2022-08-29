"""
References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from csc_docker_pool import __version__
import csc_docker_pool.wallet_cli as wallet_cli
import csc_docker_pool.config_cli as config_cli
import csc_docker_pool.relay_cli as relay_cli
import csc_docker_pool.validator_cli as validator_cli

__author__ = "maso"
__copyright__ = "maso"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        prog="GenZ Bank CSC Pool Manager",
        usage="genz-csc-pool",
        description="""GenZ Bank CSC Pool Manager and utilities to setup, manage and
        maintain CSC full node. It makes easy to create new wallet, bind address to a
        node and gain CET.
        Based on PoS consensus protocol, CoinEx Smart Chain is decentralized and energy 
        efficient. CSC makes it easy to build your own decentralized applications.
        """,
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True
    )
    parser.add_argument(
        "--version",
        action="version",
        version="csc-docker-pool {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    
    subparsers = parser.add_subparsers(
        title="Management command",
        description="Many commands are added to help you in maintenance and management."
    )
    
    wallet_cli.parse_args(subparsers)
    config_cli.parse_args(subparsers)
    relay_cli.parse_args(subparsers)
    validator_cli.parse_args(subparsers)
    
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, 
        stream=sys.stdout, 
        format=logformat, 
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing maintenance to be called with string arguments in a CLI 

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Fetch and run default function")
    args.func(args)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m csc_docker_pool.skeleton 42
    #
    run()
