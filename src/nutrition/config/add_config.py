import os

from ..utils import save_data, load_yaml
from ..vars import SETTINGS_FILE

def configure_add_parser(parser):
    """Configure arguments for config add command"""
    parser.add_argument("--name", "-n", required=True, help="Give a name of the configuration")
    parser.add_argument("--set-current", "-s", required=False, help="Set this configuration as the current one", action="store_true")
    parser.set_defaults(func=handle_add)

def handle_add(args):
    """Handle config add command"""
    add_config(args.name, args.set_current)

def add_config(name, set_current):
    """Create a new configuration file"""
    if os.path.exists(SETTINGS_FILE):
        settings = load_yaml(SETTINGS_FILE)
    else:
        print("No existing configuration file found, creating a new one.")
        settings = {
            "current": None,
            "configs": []
        }

    # Create and add the new configuration
    assert name, "Configuration name cannot be empty."
    assert not any(cfg['name'] == name for cfg in settings['configs']), f"Configuration '{name}' already exists."
    config = {
        "name": name,
        "item": f"{os.path.join(os.getcwd(), name)}-data/items.yaml",
        "meal": f"{os.path.join(os.getcwd(), name)}-data/meals.yaml"
    }
    settings["configs"].append(config)
    if set_current:
        settings["current"] = name
    save_data(settings, SETTINGS_FILE)
    print(f"✔️ Created new configuration '{name}': {SETTINGS_FILE}")
