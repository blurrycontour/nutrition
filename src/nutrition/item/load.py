from ..config import get
from ..utils import load_yaml, load_existing_data

def load():
    """Load item data from the YAML file."""
    config_file = get(verbose=0)
    item_file = load_yaml(config_file)["item"]
    items = load_existing_data(item_file)
    return items, item_file
