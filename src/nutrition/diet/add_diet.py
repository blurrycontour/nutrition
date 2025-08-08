"""Script to add a new diet to a YAML file"""
from ..console import print_section_title, print_success
from ..utils import save_data
from ..loader import load


def configure_add_parser(parser):
    """Configure arguments for diet add command"""
    parser.set_defaults(func=handle_add)

def handle_add(_args):
    """Handle diet add command"""
    add_diet()

def get_user_input():
    """Collect user input for diet creation."""
    title = "Add a new diet plan 🥗"
    print_section_title(title)

    # Basic information
    name = input("Diet name: ").strip()
    description = input("Description (optional): ").strip()

    print("\nAdd meals to the diet:")
    meals = []
    meal_count = 0

    while True:
        meal_count += 1
        print(f"\nMeal {meal_count}:")

        meal_name = input("  Meal name (or press Enter to finish): ").strip()
        if not meal_name:
            break

        # Optional: day of the week
        day = input("  Day (optional, e.g., Monday): ").strip()

        # Optional: time/meal type
        meal_type = input("  Meal type (e.g., breakfast, lunch, dinner): ").strip()

        meal_entry = {
            'name': meal_name,
        }

        if day:
            meal_entry['day'] = day
        if meal_type:
            meal_entry['type'] = meal_type

        meals.append(meal_entry)
        print(f"  ✔️ Added meal '{meal_name}'")

    if not meals:
        print("No meals added. Diet creation cancelled.")
        return None

    # Create the diet data structure
    new_diet = {
        'name': name,
        'meals': meals
    }

    if description:
        new_diet['description'] = description

    return new_diet

def add_diet():
    """Main function to add a new diet."""
    existing_data, file = load("diet")
    new_diet = get_user_input()

    if new_diet is None:
        return

    existing_data.append(new_diet)
    save_data(existing_data, file)

    print_success(f"Successfully added diet '{new_diet['name']}' to {file}")
    print_success(f"Diet contains {len(new_diet['meals'])} meals")
