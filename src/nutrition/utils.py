import os
import yaml

from .console import print_separator

def load_yaml(filepath):
    """Read YAML configuration file and return the contents as a dictionary."""
    with open(filepath, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

def load_existing_data(filename):
    """Load existing data from YAML file."""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data if data is not None else []
    else:
        return []

def save_data(data, filename):
    """Save data to YAML file."""
    # create file if not exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, sort_keys=False, allow_unicode=True, indent=2)

def vprint(text, verbose=0):
    """Print text if verbose level is sufficient."""
    if verbose > 0:
        print(text)

def print_yaml(data:dict, lines=False):
    """Print YAML data."""
    if lines: print_separator()
    print(yaml.dump(data, sort_keys=False, allow_unicode=True, indent=2))
    if lines: print_separator()
