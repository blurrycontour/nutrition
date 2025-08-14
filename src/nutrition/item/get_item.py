import re

from ..console import print_list_header, format_with_unit, print_item_detail, print_sub_item_detail
from ..loader import load
from ..utils import vprint


def configure_get_parser(parser):
    """Configure arguments for item get command"""
    parser.add_argument("name", nargs="?", default="", help="Name of the food item to retrieve (accepts regex)")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle item get command"""
    get_item(args.name)

def get_item(name=None, verbose=1):
    """Retrieve item data from the specified YAML file."""
    items, _ = load("item")
    matched_items = []
    matched_item_idx = -1
    for i, item in enumerate(items):
        if re.search(name, item["name"], re.IGNORECASE):
            matched_item_idx = i
            matched_items.append(item["name"])

    if verbose:
        print_list_header(len(matched_items), "item")
    if not matched_items:
        vprint("  No items found", verbose)
        return None, None
    if len(matched_items) == 1:
        if verbose > 0:
            print_item(items[matched_item_idx], indent=3)
        return items[matched_item_idx], matched_item_idx
    else:
        vprint("  " + "\n  ".join(matched_items), verbose)
        return matched_items, -1


def print_item(item, indent=2):
    """Print the details of a nutrition item."""

    print_item_detail("Name", item['name'], "")
    print_item_detail("Type", item['type'], "")
    print_item_detail(f"[Nutrition per {item['per']}]", "", "")

    base_indent = " " * indent
    sub_indent = " " * (indent * 2)

    energy_formatted = format_with_unit(item['nutrition']['energy']['value'], item['nutrition']['energy']['unit'])
    print_item_detail("Energy", energy_formatted, base_indent)

    carbs_formatted = format_with_unit(item['nutrition']['carbohydrates']['value'], item['nutrition']['carbohydrates']['unit'])
    sugar_formatted = format_with_unit(item['nutrition']['carbohydrates']['sugar'], item['nutrition']['carbohydrates']['unit'])
    print_item_detail("Carbohydrates", carbs_formatted, base_indent)
    print_sub_item_detail("Sugar", sugar_formatted, sub_indent)

    fat_formatted = format_with_unit(item['nutrition']['fat']['value'], item['nutrition']['fat']['unit'])
    fat_sat_formatted = format_with_unit(item['nutrition']['fat']['saturated'], item['nutrition']['fat']['unit'])
    fat_unsat_formatted = format_with_unit(item['nutrition']['fat']['unsaturated'], item['nutrition']['fat']['unit'])
    print_item_detail("Fat", fat_formatted, base_indent)
    print_sub_item_detail("Saturated", fat_sat_formatted, sub_indent)
    print_sub_item_detail("Unsaturated", fat_unsat_formatted, sub_indent)

    protein_formatted = format_with_unit(item['nutrition']['protein']['value'], item['nutrition']['protein']['unit'])
    salt_formatted = format_with_unit(item['nutrition']['salt']['value'], item['nutrition']['salt']['unit'])
    print_item_detail("Protein", protein_formatted, base_indent)
    print_item_detail("Salt", salt_formatted, base_indent)
