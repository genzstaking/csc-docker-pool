"""
References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from csc_docker_pool import __version__

__author__ = "maso"
__copyright__ = "maso"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from csc_docker_pool.skeleton import fib`,
# when using this Python module as a library.


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a


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
    parser = argparse.ArgumentParser(description="GenZ Bank CSC Pool")
    parser.add_argument(
        "--version",
        action="version",
        version="csc-docker-pool {ver}".format(ver=__version__),
    )
    #parser.add_argument(
    #    dest="n", 
    #    help="n-th Fibonacci number", 
    #    type=int, 
    #    metavar="INT")
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
    #----------------------------------------------------------
    # Wallet
    #----------------------------------------------------------
    parser_wallet = subparsers.add_parser(
        'wallet', 
        help='Manages wallets'
    )
    parser_wallet.add_argument(
        '--name', 
        help='target wallet name'
    )
    
    
    
    #----------------------------------------------------------
    # Config
    #----------------------------------------------------------
    parser_config = subparsers.add_parser(
        'config', 
        help='Manages current pool configuration'
    )
    subparsers_config = parser_config.add_subparsers(
        title="Configuration commands",
        description="Many tools are provided to manage configuration. They are available view commands."
    )
    
    parser_config_init = subparsers_config.add_parser(
        'init', 
        help='Initialize the configuration'
    )
    
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing maintenance to be called with string arguments in a CLI 

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting configuration check...")
    
    _logger.info("Script ends here")


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
