from ..utils import save_data
from .load import load

def configure_remove_parser(parser):
    """Configure arguments for item remove command"""
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", "-n", help="Name of the food item to remove")
    group.add_argument("--all", action="store_true", help="Remove all food items")
    parser.set_defaults(func=handle_remove)

def handle_remove(args):
    """Handle item remove command"""
    if args.all:
        remove_item("--all--")
    else:
        remove_item(args.name)

def remove_item(name):
    """Remove item from the specified YAML file."""
    items, file = load()
    # Remove all items
    if name == "--all--":
        items.clear()
        save_data(items, file)
        print(f"✔️ Successfully removed all items from {file}")
        return None

    # Find and remove the item
    for i, item in enumerate(items):
        if item["name"] == name:
            removed_item = items.pop(i)
            save_data(items, file)
            print(f"✔️ Successfully removed '{name}' from {file}")
            return removed_item

    print(f"❌ Item '{name}' not found in {file}")
    return None
