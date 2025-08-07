"""Script to add a new meal to a YAML file"""
from ..utils import save_data
from .load import load

def configure_add_parser(parser):
    """Configure arguments for meal add command"""
    parser.set_defaults(func=handle_add)

def handle_add(_args):
    """Handle meal add command"""
    add_meal()

def get_user_input():
    """Collect user input for meal creation."""
    title = "Add a new meal 🥗"
    print(f"\n{title}\n{'=' * len(title)}")

    # Basic information
    name = input("Meal name: ").strip()

    print("\nAdd items to the meal:")
    items = []
    item_count = 0

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

        print(f"  ✔️ Added {quantity} {unit} of {item_name}")

    if not items:
        print("No items added. Meal creation cancelled.")
        return None

    # Create the meal data structure
    new_meal = {
        'name': name,
        'items': items
    }

    return new_meal

def add_meal():
    """Main function to add a new meal."""
    existing_data, file = load()
    new_meal = get_user_input()

    if new_meal is None:
        return

    existing_data.append(new_meal)
    save_data(existing_data, file)

    print(f"\n✔️ Successfully added meal '{new_meal['name']}' to {file}")
    print(f"✔️ Meal contains {len(new_meal['items'])} items")
