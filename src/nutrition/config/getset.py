import os
import sys
from pathlib import Path

from ..utils import save_data, load_yaml, vprint, print_yaml
from ..vars import SETTINGS_FILE

def configure_set_parser(parser):
    """Configure arguments for config set command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the configuration to be set")
    parser.set_defaults(func=handle_set)

def configure_get_parser(parser):
    """Configure arguments for config get command"""
    parser.add_argument("--verbose", "-v", type=int, default=2, help="Show configuration contents")
    parser.set_defaults(func=handle_get)

def handle_set(args):
    """Handle config set command"""
    set_config(args.name)

def set_config(name):
    """Set the configuration."""
    if not os.path.exists(SETTINGS_FILE):
        print("❌ No configurations created.\nUse 'nut config create --name <my-config>' to create one.")
        sys.exit(1)

    settings = load_yaml(SETTINGS_FILE)
    # Check if configuration exists
    config_exists = any(cfg['name'] == name for cfg in settings['configs'])
    assert config_exists, f"❌ Configuration '{name}' does not exist."
    settings["current"] = name
    save_data(settings, SETTINGS_FILE)

    print(f"✔️ Configuration set to: {name}")
    print(f"✔️ Settings saved in: {SETTINGS_FILE}")

def handle_get(args):
    """Handle config get command"""
    get_config(args.verbose)

def get_config(verbose=2):
    """Config get command"""
    if not os.path.exists(SETTINGS_FILE):
        print("❌ No configurations created.\nUse 'nut config create --name <my-config>' to create one.")
        sys.exit(1)

    vprint(f"Reading settings from {SETTINGS_FILE}", verbose)
    settings = load_yaml(SETTINGS_FILE)
    current = settings.get("current", None)
    if not current:
        print("❌ No configuration set.\nUse 'nut config set --name <my-config>' to set one.")
        print_yaml(settings, True)
        sys.exit(1)

    # Find the current config
    config = None
    for cfg in settings['configs']:
        if cfg['name'] == current:
            config = cfg
            break

    if not config:
        print(f"❌ Current configuration '{current}' not found in configs.")
        sys.exit(1)

    # Show the contents of the config file if it exists
    if verbose > 0:
        print(f"Current config: '{current}'")
        print_yaml(config, lines=True)

    return config
