



def parse_args(subparsers):
    parser_config = subparsers.add_parser(
        'staking', 
        help='Manages staking node'
    )
    subparsers_config = parser_config.add_subparsers(
        title="Configuration commands",
        description="Many tools are provided to manage configuration. They are available view commands."
    )
    
    #----------------------------------------------------------
    # Config
    #----------------------------------------------------------
    parser_config_init = subparsers_config.add_parser(
        'init', 
        help='Initialize the configuration'
    )