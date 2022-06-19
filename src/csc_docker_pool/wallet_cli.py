

def parse_args(subparsers):
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