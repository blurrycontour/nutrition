import re

from ..console import format_number, print_item_detail
from ..console import print_list_header, print_error
from ..loader import load
from ..utils import vprint


def configure_get_parser(parser):
    """Configure arguments for meal get command"""
    parser.add_argument("name", nargs="?", default="", help="Name of the meal to retrieve (accepts regex)")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle meal get command"""
    get_meal(args.name)

def get_meal(name=None, verbose=1):
    """Retrieve meal data from the specified YAML file."""
    meals, _ = load("meal")
    matched_meals = []
    matched_meal_idx = -1
    for i, meal in enumerate(meals):
        if re.search(name, meal["name"], re.IGNORECASE):
            matched_meal_idx = i
            matched_meals.append(meal["name"])

    if verbose:
        print_list_header(len(matched_meals), "meal")
    if not matched_meals:
        vprint("  No meals found", verbose)
        return None, None
    if len(matched_meals) == 1:
        if verbose > 0:
            print_meal(meals[matched_meal_idx])
        return meals[matched_meal_idx], matched_meal_idx
    else:
        vprint("  " + "\n  ".join(matched_meals), verbose)
        return matched_meals, -1

def print_meal(meal):
    """Print the details of a meal."""
    print_item_detail("Meal", meal['name'], "")
    print_item_detail(f"Items ({len(meal['items'])})", "", "")

    if not meal['items']:
        print("  No items in this meal")
        return

    indent = "  "
    for item in meal['items']:
        quantity = format_number(item['quantity'])
        print(f"{indent}{quantity} {item['unit']} of {item['name']}")

def format_number(value):
    """Format a number to remove trailing zeros."""
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}".rstrip('0').rstrip('.')
    return str(value)
