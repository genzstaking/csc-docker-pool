



def parse_args(subparsers):
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