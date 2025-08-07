from .load import load

def configure_get_parser(parser):
    """Configure arguments for meal get command"""
    parser.add_argument("--name", "-n", help="Name of the meal to retrieve")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle meal get command"""
    get_meal(args.name)

def get_meal(name=None, verbose=1):
    """Retrieve meal data from the specified YAML file."""
    meals, _ = load()
    if name:
        for meal in meals:
            if meal["name"] == name:
                if verbose > 0:
                    print_meal(meal)
                return meal
        print(f"❌ Meal '{name}' not found")
        return None
    all_meals = [meal["name"] for meal in meals]
    print(f"[Found ({len(all_meals)}) meals]")
    if all_meals:
        print("  " + "\n  ".join(all_meals))
    else:
        print("  No meals found")
    return all_meals

def print_meal(meal):
    """Print the details of a meal."""
    print(f"Meal: {meal['name']}")
    print(f"Items ({len(meal['items'])}):")

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
