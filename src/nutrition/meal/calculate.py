import re

from ..console import *
from ..loader import load
from .get_meal import get_meal

def configure_calculate_parser(parser):
    """Configure arguments for meal calculate command"""
    parser.add_argument("name", help="Name of the meal to calculate (accepts regex)")
    parser.set_defaults(func=handle_calculate)

def handle_calculate(args):
    """Handle meal calculate command"""
    calculate_meal(args.name)

def calculate_meal(meal_name):
    """Calculate the total nutrition values for the specified meal."""
    items, _ = load("item")
    # Find the specified meal
    target_meal, idx = get_meal(name=meal_name, verbose=0)
    if idx is None:
        print_error(f"Meal '{meal_name}' not found")
        return None
    elif idx == -1:
        print_error(f"Multiple meals matched with '{meal_name}'")
        return None
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

    print_header(f"Calculating total nutrition for '{meal_name}'", '=')
    print(f"Items in meal: {len(target_meal['items'])}\n") # type: ignore

    # Calculate nutrition for each item in the meal
    for meal_item in target_meal['items']:  # type: ignore
        item_name = meal_item['name']
        quantity = meal_item['quantity']
        unit = meal_item['unit']

        if item_name not in item_lookup:
            missing_items.append(item_name)
            print_warning(f"{format_number(quantity)} {unit} of {item_name} - NOT FOUND")
            continue

        food_item = item_lookup[item_name]

        # Calculate multiplier based on quantity
        # Assume nutrition data is per 100g and convert accordingly
        base_amount = get_base_amount(food_item['per'])
        multiplier = calculate_multiplier(quantity, unit, base_amount)

        if multiplier is None:
            print_warning(f"{format_number(quantity)} {unit} of {item_name} - UNIT CONVERSION ISSUE")
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
    print_separator()
    print_header("💯 TOTAL NUTRITION FOR MEAL", '=')
    print_nutrition_totals(totals)

    if missing_items:
        print_warning(f"Missing nutrition data for {len(missing_items)} items:")
        for item in missing_items:
            print(f"   - {item}")
    print_separator()

    print_success(f"Calculated nutrition for {len(calculated_items)} items")

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


def print_nutrition_totals(totals):
    """Print the total nutrition values in a formatted way."""
    indent = "  "
    sub_indent = "    "

    energy_formatted = format_with_unit(totals['energy']['value'], totals['energy']['unit'])
    print_item_detail("Energy", energy_formatted, indent)

    carbs_formatted = format_with_unit(totals['carbohydrates']['value'], totals['carbohydrates']['unit'])
    sugar_formatted = format_with_unit(totals['carbohydrates']['sugar'], totals['carbohydrates']['unit'])
    print_item_detail("Carbohydrates", carbs_formatted, indent)
    print_sub_item_detail("Sugar", sugar_formatted, sub_indent)

    fat_formatted = format_with_unit(totals['fat']['value'], totals['fat']['unit'])
    fat_sat_formatted = format_with_unit(totals['fat']['saturated'], totals['fat']['unit'])
    fat_unsat_formatted = format_with_unit(totals['fat']['unsaturated'], totals['fat']['unit'])
    print_item_detail("Fat", fat_formatted, indent)
    print_sub_item_detail("Saturated", fat_sat_formatted, sub_indent)
    print_sub_item_detail("Unsaturated", fat_unsat_formatted, sub_indent)

    protein_formatted = format_with_unit(totals['protein']['value'], totals['protein']['unit'])
    salt_formatted = format_with_unit(totals['salt']['value'], totals['salt']['unit'])
    print_item_detail("Protein", protein_formatted, indent)
    print_item_detail("Salt", salt_formatted, indent)
