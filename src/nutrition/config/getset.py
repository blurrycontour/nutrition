import json
import os
import yaml
from pathlib import Path
from nutrition.utils import save_data, load_yaml, vprint

# Default config file location in user's home directory
SETTINGS_FILE = os.getenv("NUTRITION_CONFIG", Path.home() / ".nutcfg.yaml")

def configure_set_parser(parser):
    """Configure arguments for config set command"""
    parser.add_argument("--file", "-f", required=True, help="Path to the configuration file")
    parser.set_defaults(func=handle_set)

def configure_get_parser(parser):
    """Configure arguments for config get command"""
    parser.add_argument("--verbose", "-v", type=int, default=2, help="Show configuration contents")
    parser.set_defaults(func=handle_get)

def handle_set(args):
    """Handle config set command"""
    config_file_path = args.file
    assert os.path.exists(config_file_path), f"❌ Configuration file '{config_file_path}' does not exist."
    settings = {"config": os.path.abspath(config_file_path)}
    save_data(settings, SETTINGS_FILE)

    print(f"✓ Configuration file set to: {os.path.abspath(config_file_path)}")
    print(f"✓ Settings saved in: {SETTINGS_FILE}")

def handle_get(args):
    """Handle config get command"""
    get(args.verbose)

def get(verbose=2):
    """Config get command"""
    assert os.path.exists(SETTINGS_FILE), "❌ No configuration file set. Use 'nut config set --file <filepath>' to set one."

    try:
        vprint(f"Reading settings from {SETTINGS_FILE}", verbose)
        settings = load_yaml(SETTINGS_FILE)
        config_file = settings.get('config')
        vprint(f"Current config file: {config_file}", verbose)

        # Show the contents of the config file if it exists
        if verbose == 2:
            if config_file and os.path.exists(config_file):
                config_contents = load_yaml(config_file)
                print(json.dumps(config_contents, indent=2))
            else:
                print(f"❌ Configuration file '{config_file}' does not exist.")

        return config_file
    except yaml.YAMLError as e:
        print(f"❌ Error reading configuration: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
