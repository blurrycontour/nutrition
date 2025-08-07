from ..utils import save_data
from .load import load

def configure_update_parser(parser):
    """Configure arguments for diet update command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the diet to update")
    parser.set_defaults(func=handle_update)

def handle_update(args):
    """Handle diet update command"""
    update_diet(args.name)

def get_user_input(existing_diet):
    """Collect user input for updating diet with existing values as defaults."""
    title = f"Update diet: {existing_diet['name']}"
    print(f"\n{title}\n{'=' * len(title)}")
    print("Press Enter to keep existing values, or type new values to update.")

    # Basic information
    name = input(f"Diet name [{existing_diet['name']}]: ").strip() or existing_diet['name']

    current_description = existing_diet.get('description', '')
    description = input(f"Description [{current_description}]: ").strip()
    if not description:
        description = current_description

    print(f"\nCurrent meals in diet ({len(existing_diet['meals'])}):")
    for i, meal in enumerate(existing_diet['meals'], 1):
        meal_info = meal['name']
        details = []
        if 'day' in meal:
            details.append(f"Day: {meal['day']}")
        if 'type' in meal:
            details.append(f"Type: {meal['type']}")
        if details:
            meal_info += f" ({', '.join(details)})"
        print(f"  {i}. {meal_info}")

    print("\nChoose an option:")
    print("1. Keep existing meals and add new ones")
    print("2. Replace all meals with new ones")
    print("3. Edit existing meals")

    choice = input("Choice [1]: ").strip() or "1"

    if choice == "1":
        meals = existing_diet['meals'].copy()
        print("\nAdd new meals (press Enter without typing anything to finish):")
        meals.extend(get_new_meals(len(meals)))
    elif choice == "2":
        print("\nAdd new meals (press Enter without typing anything to finish):")
        meals = get_new_meals()
    elif choice == "3":
        meals = edit_existing_meals(existing_diet['meals'])
    else:
        print("Invalid choice, keeping existing meals")
        meals = existing_diet['meals']

    # Create the updated diet data structure
    updated_diet = {
        'name': name,
        'meals': meals
    }

    if description:
        updated_diet['description'] = description

    return updated_diet

def get_new_meals(start_count=0):
    """Get new meals from user input."""
    meals = []
    meal_count = start_count

    while True:
        meal_count += 1
        print(f"\nMeal {meal_count}:")

        meal_name = input("  Meal name (or press Enter to finish): ").strip()
        if not meal_name:
            break

        day = input("  Day (optional): ").strip()
        meal_type = input("  Meal type (optional): ").strip()

        meal_entry = {'name': meal_name}
        if day:
            meal_entry['day'] = day
        if meal_type:
            meal_entry['type'] = meal_type

        meals.append(meal_entry)
        print(f"  ✔️ Added meal '{meal_name}'")

    return meals

def edit_existing_meals(existing_meals):
    """Edit existing meals in the diet."""
    meals = []

    for i, meal in enumerate(existing_meals, 1):
        meal_info = meal['name']
        details = []
        if 'day' in meal:
            details.append(f"Day: {meal['day']}")
        if 'type' in meal:
            details.append(f"Type: {meal['type']}")
        if details:
            meal_info += f" ({', '.join(details)})"

        print(f"\nMeal {i}: {meal_info}")
        print("Options: [k]eep, [e]dit, [d]elete, [s]kip to finish")

        action = input("Action [k]: ").strip().lower() or "k"

        if action == "k":
            meals.append(meal)
        elif action == "e":
            name = input(f"  Meal name [{meal['name']}]: ").strip() or meal['name']

            current_day = meal.get('day', '')
            day = input(f"  Day [{current_day}]: ").strip()
            if not day:
                day = current_day

            current_type = meal.get('type', '')
            meal_type = input(f"  Meal type [{current_type}]: ").strip()
            if not meal_type:
                meal_type = current_type

            meal_entry = {'name': name}
            if day:
                meal_entry['day'] = day
            if meal_type:
                meal_entry['type'] = meal_type

            meals.append(meal_entry)
            print(f"  ✔️ Updated meal '{name}'")
        elif action == "d":
            print(f"  ✗ Deleted meal '{meal['name']}'")
        elif action == "s":
            # Add remaining meals without changes
            meals.extend(existing_meals[i-1:])
            break

    return meals

def update_diet(diet_name):
    """Update diet in the specified YAML file."""
    diets, file = load()

    # Find and update the diet
    for i, diet in enumerate(diets):
        if diet["name"] == diet_name:
            updated_diet = get_user_input(diet)
            diets[i] = updated_diet
            save_data(diets, file)
            print(f"\n✔️ Successfully updated diet '{diet_name}' in {file}")
            print(f"✔️ Diet now contains {len(updated_diet['meals'])} meals")
            return updated_diet

    print(f"❌ Diet '{diet_name}' not found in {file}")
    return None
