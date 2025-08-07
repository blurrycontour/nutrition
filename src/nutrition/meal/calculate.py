import re

from ..item.load import load as load_items
from .get_meal import get_meal

def configure_calculate_parser(parser):
    """Configure arguments for meal calculate command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the meal to calculate")
    parser.set_defaults(func=handle_calculate)

def handle_calculate(args):
    """Handle meal calculate command"""
    calculate_meal(args.name)

def calculate_meal(meal_name):
    """Calculate the total nutrition values for the specified meal."""
    items, _ = load_items()
    # Find the specified meal
    target_meal = get_meal(name=meal_name, verbose=0)
    # Create a lookup dictionary for items
    item_lookup = {item["name"]: item for item in items}

    # Initialize totals
    totals = {
        'energy': {'value': 0, 'unit': 'kcal'},
        'carbohydrates': {'value': 0, 'unit': 'g', 'sugar': 0},
        'fat': {'value': 0, 'unit': 'g', 'saturated': 0, 'unsaturated': 0},
        'protein': {'value': 0, 'unit': 'g'},
        'salt': {'value': 0, 'unit': 'g'}
    }

    missing_items = []
    calculated_items = []

    print(f"Calculating total nutrition for '{meal_name}'")
    print("-" * 50)
    print(f"Items in meal: {len(target_meal['items'])}\n") # type: ignore

    # Calculate nutrition for each item in the meal
    for meal_item in target_meal['items']:  # type: ignore
        item_name = meal_item['name']
        quantity = meal_item['quantity']
        unit = meal_item['unit']

        if item_name not in item_lookup:
            missing_items.append(item_name)
            print(f"⚠️  {format_number(quantity)} {unit} of {item_name} - NOT FOUND")
            continue

        food_item = item_lookup[item_name]

        # Calculate multiplier based on quantity
        # Assume nutrition data is per 100g and convert accordingly
        base_amount = get_base_amount(food_item['per'])
        multiplier = calculate_multiplier(quantity, unit, base_amount)

        if multiplier is None:
            print(f"⚠️  {format_number(quantity)} {unit} of {item_name} - UNIT CONVERSION ISSUE")
            continue

        # Add to totals
        nutrition = food_item['nutrition']

        # Energy
        if nutrition['energy']['value'] is not None:
            totals['energy']['value'] += nutrition['energy']['value'] * multiplier

        # Carbohydrates
        if nutrition['carbohydrates']['value'] is not None:
            totals['carbohydrates']['value'] += nutrition['carbohydrates']['value'] * multiplier
        if nutrition['carbohydrates']['sugar'] is not None:
            totals['carbohydrates']['sugar'] += nutrition['carbohydrates']['sugar'] * multiplier

        # Fat
        if nutrition['fat']['value'] is not None:
            totals['fat']['value'] += nutrition['fat']['value'] * multiplier
        if nutrition['fat']['saturated'] is not None:
            totals['fat']['saturated'] += nutrition['fat']['saturated'] * multiplier
        if nutrition['fat']['unsaturated'] is not None:
            totals['fat']['unsaturated'] += nutrition['fat']['unsaturated'] * multiplier

        # Protein
        if nutrition['protein']['value'] is not None:
            totals['protein']['value'] += nutrition['protein']['value'] * multiplier

        # Salt
        if nutrition['salt']['value'] is not None:
            totals['salt']['value'] += nutrition['salt']['value'] * multiplier

        calculated_items.append(item_name)
        print(f"✔️ {format_number(quantity)} {unit} of {item_name} (×{format_number(multiplier)})")

    # Display results
    print("-" * 50)
    print("-" * 50)
    print("💯 Total Nutrition Value\n")
    print_nutrition_totals(totals)

    if missing_items:
        print(f"\n⚠️  Missing nutrition data for {len(missing_items)} items:")
        for item in missing_items:
            print(f"   - {item}")
    print("-" * 50)


    print(f"\n✔️ Calculated nutrition for {len(calculated_items)} items")

    return totals

def get_base_amount(per_string):
    """Extract the base amount from the 'per' field (e.g., '100g' -> 100)."""
    match = re.search(r'(\d+)', per_string)
    return float(match.group(1)) if match else 100.0

def calculate_multiplier(quantity, unit, base_amount):
    """Calculate the multiplier for nutrition values based on quantity and unit."""
    # Convert everything to grams for simplicity
    # This is a basic conversion - you might want to extend this

    quantity_in_grams = quantity

    # Basic unit conversions to grams
    if unit.lower() in ['kg', 'kilogram', 'kilograms']:
        quantity_in_grams = quantity * 1000
    elif unit.lower() in ['g', 'gram', 'grams']:
        quantity_in_grams = quantity
    elif unit.lower() in ['mg', 'milligram', 'milligrams']:
        quantity_in_grams = quantity / 1000
    elif unit.lower() in ['oz', 'ounce', 'ounces']:
        quantity_in_grams = quantity * 28.35
    elif unit.lower() in ['lb', 'pound', 'pounds']:
        quantity_in_grams = quantity * 453.6
    elif unit.lower() in ['pcs', 'piece', 'pieces', 'pc']:
        # For pieces, assume each piece is 100g (you might want to make this configurable)
        quantity_in_grams = quantity * 100
    else:
        # Unknown unit, assume it's already in the correct proportion
        return quantity / base_amount

    # Calculate multiplier based on base amount (usually 100g)
    return quantity_in_grams / base_amount

def format_number(value):
    """Format a number to remove trailing zeros."""
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}".rstrip('0').rstrip('.')
    return str(value)

def format_with_unit(value, unit):
    """Format value with unit, or just '-' if value is None."""
    if value is None or value == 0:
        return "-"
    formatted_value = format_number(value)
    return f"{formatted_value} {unit}"

def print_nutrition_totals(totals):
    """Print the total nutrition values in a formatted way."""
    indent = "  "
    sub_indent = "    "

    energy_formatted = format_with_unit(totals['energy']['value'], totals['energy']['unit'])
    print(f"{indent}Energy: {energy_formatted}")

    carbs_formatted = format_with_unit(totals['carbohydrates']['value'], totals['carbohydrates']['unit'])
    sugar_formatted = format_with_unit(totals['carbohydrates']['sugar'], totals['carbohydrates']['unit'])
    print(f"{indent}Carbohydrates: {carbs_formatted}")
    print(f"{sub_indent}Sugar: {sugar_formatted}")

    fat_formatted = format_with_unit(totals['fat']['value'], totals['fat']['unit'])
    fat_sat_formatted = format_with_unit(totals['fat']['saturated'], totals['fat']['unit'])
    fat_unsat_formatted = format_with_unit(totals['fat']['unsaturated'], totals['fat']['unit'])
    print(f"{indent}Fat: {fat_formatted}")
    print(f"{sub_indent}Saturated: {fat_sat_formatted}")
    print(f"{sub_indent}Unsaturated: {fat_unsat_formatted}")

    protein_formatted = format_with_unit(totals['protein']['value'], totals['protein']['unit'])
    salt_formatted = format_with_unit(totals['salt']['value'], totals['salt']['unit'])
    print(f"{indent}Protein: {protein_formatted}")
    print(f"{indent}Salt: {salt_formatted}")
