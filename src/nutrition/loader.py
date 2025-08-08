from .config import get_config
from .utils import load_existing_data


def load(identifier:str):
    """Load data from the YAML file."""
    config = get_config(verbose=0)
    file = config[identifier]
    data = load_existing_data(file)
    return data, file
