from ..config import get_config
from ..utils import load_yaml, load_existing_data

def load():
    """Load meal data from the YAML file."""
    config = get_config(verbose=0)
    meal_file = config["meal"]
    meals = load_existing_data(meal_file)
    return meals, meal_file
