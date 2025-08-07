from ..utils import save_data
from .load import load

def configure_remove_parser(parser):
    """Configure arguments for meal remove command"""
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", "-n", help="Name of the meal to remove")
    group.add_argument("--all", action="store_true", help="Remove all meals")
    parser.set_defaults(func=handle_remove)

def handle_remove(args):
    """Handle meal remove command"""
    if args.all:
        remove_meal("--all--")
    else:
        remove_meal(args.name)

def remove_meal(meal_name):
    """Remove meal from the specified YAML file."""
    meals, file = load()

    # Remove all meals
    if meal_name == "--all--":
        meals.clear()
        save_data(meals, file)
        print(f"✔️ Successfully removed all meals from {file}")
        return None

    # Find and remove the meal
    for i, meal in enumerate(meals):
        if meal["name"] == meal_name:
            removed_meal = meals.pop(i)

            # Save the updated data
            save_data(meals, file)

            print(f"✔️ Successfully removed meal '{meal_name}' from {file}")
            print(f"✔️ Removed meal had {len(removed_meal['items'])} items")
            return removed_meal

    print(f"❌ Meal '{meal_name}' not found in {file}")
    return None
