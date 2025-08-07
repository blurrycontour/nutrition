import os
import sys

from ..utils import save_data, load_yaml
from ..vars import SETTINGS_FILE


def configure_set_parser(parser):
    """Configure arguments for config set command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the configuration to be set")
    parser.set_defaults(func=handle_set)


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
