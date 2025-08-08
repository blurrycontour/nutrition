from ..console import print_section_title, format_number, print_success, print_error
from ..utils import save_data
from ..loader import load

def configure_update_parser(parser):
    """Configure arguments for meal update command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the meal to update")
    parser.set_defaults(func=handle_update)

def handle_update(args):
    """Handle meal update command"""
    update_meal(args.name)

def get_user_input(existing_meal):
    """Collect user input for updating meal with existing values as defaults."""
    title = f"Update meal: {existing_meal['name']}"
    print_section_title(title)
    print("Press Enter to keep existing values, or type new values to update.")

    # Basic information
    name = input(f"Meal name [{existing_meal['name']}]: ").strip() or existing_meal['name']

    print(f"\nCurrent items in meal ({len(existing_meal['items'])}):")
    for i, item in enumerate(existing_meal['items'], 1):
        quantity = format_number(item['quantity'])
        print(f"  {i}. {quantity} {item['unit']} of {item['name']}")

    print("\nChoose an option:")
    print("1. Keep existing items and add new ones")
    print("2. Replace all items with new ones")
    print("3. Edit existing items")

    choice = input("Choice [1]: ").strip() or "1"

    if choice == "1":
        items = existing_meal['items'].copy()
        print("\nAdd new items (press Enter without typing anything to finish):")
        items.extend(get_new_items(len(items)))
    elif choice == "2":
        print("\nAdd new items (press Enter without typing anything to finish):")
        items = get_new_items()
    elif choice == "3":
        items = edit_existing_items(existing_meal['items'])
    else:
        print("Invalid choice, keeping existing items")
        items = existing_meal['items']

    # Create the updated meal data structure
    updated_meal = {
        'name': name,
        'items': items
    }

    return updated_meal

def get_new_items(start_count=0):
    """Get new items from user input."""
    items = []
    item_count = start_count

    while True:
        item_count += 1
        print(f"\nItem {item_count}:")

        item_name = input("  Item name (or press Enter to finish): ").strip()
        if not item_name:
            break

        quantity_input = input("  Quantity: ").strip()
        try:
            quantity = float(quantity_input) if quantity_input else 1.0
        except ValueError:
            print("  Invalid quantity, using 1.0")
            quantity = 1.0

        unit = input("  Unit [g]: ").strip() or "g"

        items.append({
            'name': item_name,
            'quantity': quantity,
            'unit': unit
        })

        print(f"  ✔️ Added {format_number(quantity)} {unit} of {item_name}")

    return items

def edit_existing_items(existing_items):
    """Edit existing items in the meal."""
    items = []

    for i, item in enumerate(existing_items, 1):
        print(f"\nItem {i}: {format_number(item['quantity'])} {item['unit']} of {item['name']}")
        print("Options: [k]eep, [e]dit, [d]elete, [s]kip to finish")

        action = input("Action [k]: ").strip().lower() or "k"

        if action == "k":
            items.append(item)
        elif action == "e":
            name = input(f"  Item name [{item['name']}]: ").strip() or item['name']

            quantity_display = format_number(item['quantity'])
            quantity_input = input(f"  Quantity [{quantity_display}]: ").strip()
            if quantity_input:
                try:
                    quantity = float(quantity_input)
                except ValueError:
                    print("  Invalid quantity, keeping existing")
                    quantity = item['quantity']
            else:
                quantity = item['quantity']

            unit = input(f"  Unit [{item['unit']}]: ").strip() or item['unit']

            items.append({
                'name': name,
                'quantity': quantity,
                'unit': unit
            })
            print(f"  ✔️ Updated to {format_number(quantity)} {unit} of {name}")
        elif action == "d":
            print(f"  ✗ Deleted {item['name']}")
        elif action == "s":
            # Add remaining items without changes
            items.extend(existing_items[i-1:])
            break

    return items


def update_meal(meal_name):
    """Update meal in the specified YAML file."""
    meals, file = load("meal")

    # Find and update the meal
    for i, meal in enumerate(meals):
        if meal["name"] == meal_name:
            updated_meal = get_user_input(meal)
            meals[i] = updated_meal
            save_data(meals, file)
            print_success(f"Successfully updated meal '{meal_name}' in {file}")
            print_success(f"Meal now contains {len(updated_meal['items'])} items")
            return updated_meal

    print_error(f"Meal '{meal_name}' not found in {file}")
    return None
