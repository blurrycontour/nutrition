from .load import load

def configure_get_parser(parser):
    """Configure arguments for diet get command"""
    parser.add_argument("--name", "-n", help="Name of the diet to retrieve")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle diet get command"""
    get_diet(args.name)

def get_diet(name=None, verbose=1):
    """Retrieve diet data from the specified YAML file."""
    diets, _ = load()
    if name:
        for diet in diets:
            if diet["name"] == name:
                if verbose > 0:
                    print_diet(diet)
                return diet
        print(f"❌ Diet '{name}' not found")
        return dict()
    all_diets = [diet["name"] for diet in diets]
    print(f"[Found ({len(all_diets)}) diets]")
    if all_diets:
        print("  " + "\n  ".join(all_diets))
    else:
        print("  No diets found")
    return all_diets

def print_diet(diet):
    """Print the details of a diet."""
    print(f"Diet: {diet['name']}")

    if 'description' in diet:
        print(f"Description: {diet['description']}")

    print(f"Meals ({len(diet['meals'])}):")

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
