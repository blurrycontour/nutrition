from ..config import get_config
from ..utils import load_existing_data

def load():
    """Load diet data from the YAML file."""
    config = get_config(verbose=0)
    diet_file = config["diet"]
    diets = load_existing_data(diet_file)
    return diets, diet_file
