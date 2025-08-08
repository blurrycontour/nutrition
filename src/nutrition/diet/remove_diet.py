from ..console import print_success, print_error
from ..utils import save_data
from ..loader import load


def configure_remove_parser(parser):
    """Configure arguments for diet remove command"""
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", "-n", help="Name of the diet to remove")
    group.add_argument("--all", action="store_true", help="Remove all diets")
    parser.set_defaults(func=handle_remove)

def handle_remove(args):
    """Handle diet remove command"""
    if args.all:
        remove_diet("--all--")
    else:
        remove_diet(args.name)

def remove_diet(diet_name):
    """Remove diet from the specified YAML file."""
    diets, file = load("diet")

    # Remove all diets
    if diet_name == "--all--":
        diets.clear()
        save_data(diets, file)
        print_success(f"Successfully removed all diets from {file}")
        return None

    # Find and remove the diet
    for i, diet in enumerate(diets):
        if diet["name"] == diet_name:
            removed_diet = diets.pop(i)

            # Save the updated data
            save_data(diets, file)

            print_success(f"Successfully removed diet '{diet_name}' from {file}")
            print_success(f"Removed diet had {len(removed_diet['meals'])} meals")
            return removed_diet

    print_error(f"Diet '{diet_name}' not found in {file}")
    return None
