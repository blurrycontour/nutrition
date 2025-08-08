from ..console import print_list_header, print_error, print_item_detail
from ..loader import load


def configure_get_parser(parser):
    """Configure arguments for diet get command"""
    parser.add_argument("--name", "-n", help="Name of the diet to retrieve")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle diet get command"""
    get_diet(args.name)

def get_diet(name=None, verbose=1):
    """Retrieve diet data from the specified YAML file."""
    diets, _ = load("diet")
    if name:
        for diet in diets:
            if diet["name"] == name:
                if verbose > 0:
                    print_diet(diet)
                return diet
        print_error(f"Diet '{name}' not found")
        return dict()
    all_diets = [diet["name"] for diet in diets]
    print_list_header(len(all_diets), "diet")
    if all_diets:
        print("  " + "\n  ".join(all_diets))
    else:
        print("  No diets found")
    return all_diets

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
