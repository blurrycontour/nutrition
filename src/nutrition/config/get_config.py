import os
import sys

from ..console import print_error
from ..utils import load_yaml, vprint, print_yaml
from ..vars import SETTINGS_FILE


def configure_get_parser(parser):
    """Configure arguments for config get command"""
    parser.add_argument("--all", "-a", action="store_true", help="Show all configurations")
    parser.add_argument("--verbose", "-v", type=int, default=2, help="Show configuration contents")
    parser.set_defaults(func=handle_get)


def handle_get(args):
    """Handle config get command"""
    get_config(args.verbose, args.all)


def get_config(verbose=2, all_configs=False):
    """Config get command"""
    if not os.path.exists(SETTINGS_FILE):
        print_error("No configurations created.\nUse 'nut config create --name <my-config>' to create one.")
        sys.exit(1)

    vprint(f"Reading settings from {SETTINGS_FILE}", verbose)
    settings = load_yaml(SETTINGS_FILE)
    current = settings.get("current", None)
    if not current:
        print_error("No configuration set.\nUse 'nut config set --name <my-config>' to set one.")
        print_yaml(settings, True)
        sys.exit(1)

    # Find the current config
    config = None
    for cfg in settings['configs']:
        if cfg['name'] == current:
            config = cfg
            break

    if not config:
        print_error(f"Current configuration '{current}' not found in configs.")
        sys.exit(1)

    # Show the contents of the config file if it exists
    if verbose > 0:
        print(f"Current config: '{current}'")
        print_yaml(config, lines=True)

    if all_configs:
        print("\nAll configurations:")
        print_yaml(settings, lines=True)

    return config
