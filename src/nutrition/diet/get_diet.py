import re

from ..console import print_list_header, print_error, print_item_detail
from ..loader import load
from ..utils import vprint


def configure_get_parser(parser):
    """Configure arguments for diet get command"""
    parser.add_argument("name", nargs="?", default="", help="Name of the diet to retrieve (accepts regex)")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle diet get command"""
    get_diet(args.name)

def get_diet(name=None, verbose=1):
    """Retrieve diet data from the specified YAML file."""
    diets, _ = load("diet")
    matched_diets = []
    matched_diet_idx = -1
    for i, diet in enumerate(diets):
        if re.search(name, diet["name"], re.IGNORECASE):
            matched_diet_idx = i
            matched_diets.append(diet["name"])

    if verbose:
        print_list_header(len(matched_diets), "diet")
    if not matched_diets:
        vprint("  No diets found", verbose)
        return None, None
    if len(matched_diets) == 1:
        if verbose > 0:
            print_diet(diets[matched_diet_idx])
        return diets[matched_diet_idx], matched_diet_idx
    else:
        vprint("  " + "\n  ".join(matched_diets), verbose)
        return matched_diets, -1


def print_diet(diet):
    """Print the details of a diet."""
    print_item_detail("Diet", diet['name'], "")

    if 'description' in diet:
        print_item_detail("Description", diet['description'], "")

    print_item_detail(f"Meals ({len(diet['meals'])})", "", "")

    if not diet['meals']:
        print("  No meals in this diet")
        return

    indent = "  "
    for meal in diet['meals']:
        meal_info = meal['name']

        details = []
        if 'day' in meal:
            details.append(f"Day: {meal['day']}")
        if 'type' in meal:
            details.append(f"Type: {meal['type']}")

        if details:
            meal_info += f" ({', '.join(details)})"

        print(f"{indent}{meal_info}")
