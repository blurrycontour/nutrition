import os
import sys

from ..utils import load_yaml, save_data
from ..vars import SETTINGS_FILE

def configure_remove_parser(parser):
    """Configure arguments for config remove command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the configuration to remove")
    parser.set_defaults(func=handle_remove)

def handle_remove(args):
    """Handle config remove command"""
    remove_config(args.name)

def remove_config(name):
    """Remove a configuration."""
    if not os.path.exists(SETTINGS_FILE):
        print("❌ No configurations created.\nUse 'nut config create --name <my-config>' to create one.")
        sys.exit(1)

    settings = load_yaml(SETTINGS_FILE)

    # Check if configuration exists
    config_to_remove = None
    for i, cfg in enumerate(settings['configs']):
        if cfg['name'] == name:
            config_to_remove = i
            break

    if config_to_remove is None:
        print(f"❌ Configuration '{name}' does not exist.")
        available_configs = [cfg['name'] for cfg in settings['configs']]
        if available_configs:
            print(f"Available configurations: {', '.join(available_configs)}")
        sys.exit(1)

    # Remove the configuration
    settings['configs'].pop(config_to_remove)

    # If we're removing the current configuration, unset it
    if settings.get("current") == name:
        settings["current"] = None
        print(f"⚠️  Removed current configuration '{name}'. No configuration is now set.")
        if settings['configs']:
            available_configs = [cfg['name'] for cfg in settings['configs']]
            print(f"Available configurations: {', '.join(available_configs)}")
            print("Use 'nut config set --name <config-name>' to set a configuration.")

    save_data(settings, SETTINGS_FILE)
    print(f"✔️ Successfully removed configuration '{name}' from {SETTINGS_FILE}")
