from .load import load

def configure_get_parser(parser):
    """Configure arguments for item get command"""
    parser.add_argument("--name", "-n", help="Name of the food item to retrieve")
    parser.set_defaults(func=handle_get)

def handle_get(args):
    """Handle item get command"""
    get_item(args.name)

def get_item(name=None, verbose=1):
    """Retrieve item data from the specified YAML file."""
    items, _ = load()
    if name:
        for item in items:
            if item["name"] == name:
                if verbose > 0:
                    print_item(item, indent=3)
                return item
        return None
    all_items = [item["name"] for item in items]
    print(f"[Found ({len(all_items)}) items]")
    print("  "+"\n  ".join(all_items))
    return all_items


def print_item(item, indent=2):
    """Print the details of a nutrition item."""

    def format_number(value):
        """Format a number to remove trailing zeros, or return '-' for None."""
        if value is None:
            return None
        if isinstance(value, float):
            return f"{value:.2f}".rstrip('0').rstrip('.')
        return str(value)

    def format_with_unit(value, unit):
        """Format value with unit, or just '-' if value is None."""
        formatted_value = format_number(value)
        if formatted_value is None:
            return "?"
        return f"{formatted_value} {unit}"

    print(f"Name: {item['name']}")
    print(f"Type: {item['type']}")
    print(f"[Nutrition per {item['per']}]")

    indent = " " * indent

    energy_formatted = format_with_unit(item['nutrition']['energy']['value'], item['nutrition']['energy']['unit'])
    print(f"{indent}Energy: {energy_formatted}")

    carbs_formatted = format_with_unit(item['nutrition']['carbohydrates']['value'], item['nutrition']['carbohydrates']['unit'])
    sugar_formatted = format_with_unit(item['nutrition']['carbohydrates']['sugar'], item['nutrition']['carbohydrates']['unit'])
    print(f"{indent}Carbohydrates: {carbs_formatted}")
    print(f"{indent*2}Sugar: {sugar_formatted}")

    fat_formatted = format_with_unit(item['nutrition']['fat']['value'], item['nutrition']['fat']['unit'])
    fat_sat_formatted = format_with_unit(item['nutrition']['fat']['saturated'], item['nutrition']['fat']['unit'])
    fat_unsat_formatted = format_with_unit(item['nutrition']['fat']['unsaturated'], item['nutrition']['fat']['unit'])
    print(f"{indent}Fat: {fat_formatted}")
    print(f"{indent*2}Saturated: {fat_sat_formatted}")
    print(f"{indent*2}Unsaturated: {fat_unsat_formatted}")

    protein_formatted = format_with_unit(item['nutrition']['protein']['value'], item['nutrition']['protein']['unit'])
    salt_formatted = format_with_unit(item['nutrition']['salt']['value'], item['nutrition']['salt']['unit'])
    print(f"{indent}Protein: {protein_formatted}")
    print(f"{indent}Salt: {salt_formatted}")
