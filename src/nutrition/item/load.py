from ..config import get_config
from ..utils import load_yaml, load_existing_data

def load():
    """Load item data from the YAML file."""
    config = get_config(verbose=0)
    item_file = config["item"]
    items = load_existing_data(item_file)
    return items, item_file
