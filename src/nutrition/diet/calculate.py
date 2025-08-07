from ..meal.calculate import calculate_meal
from .get_diet import get_diet

def configure_calculate_parser(parser):
    """Configure arguments for diet calculate command"""
    parser.add_argument("--name", "-n", required=True, help="Name of the diet to calculate")
    parser.add_argument("--summary", "-s", action="store_true", help="Show summary only")
    parser.set_defaults(func=handle_calculate)

def handle_calculate(args):
    """Handle diet calculate command"""
    calculate_diet(args.name, args.summary)

def calculate_diet(diet_name, summary_only=False):
    """Calculate the total nutrition values for all meals in the specified diet."""
    # Get the diet plan
    target_diet = get_diet(name=diet_name, verbose=0)

    if not target_diet or not isinstance(target_diet, dict) or 'meals' not in target_diet:
        print(f"❌ Diet '{diet_name}' not found or has no meals")
        return None

    print(f"\nCalculating total nutrition for diet: '{diet_name}'")
    print("=" * 60)

    if 'description' in target_diet:
        print(f"Description: {target_diet['description']}")

    print(f"Total meals in diet: {len(target_diet['meals'])}")
    print("-" * 60)

    # Initialize diet totals
    diet_totals = {
        'energy': {'value': 0, 'unit': 'kcal'},
        'carbohydrates': {'value': 0, 'unit': 'g', 'sugar': 0},
        'fat': {'value': 0, 'unit': 'g', 'saturated': 0, 'unsaturated': 0},
        'protein': {'value': 0, 'unit': 'g'},
        'salt': {'value': 0, 'unit': 'g'}
    }

    calculated_meals = []
    missing_meals = []

    # Calculate nutrition for each meal in the diet
    for i, diet_meal in enumerate(target_diet['meals'], 1):
        meal_name = diet_meal['name']

        # Display meal info
        meal_info = f"Meal {i}: {meal_name}"
        if 'day' in diet_meal:
            meal_info += f" (Day: {diet_meal['day']}"
            if 'type' in diet_meal:
                meal_info += f", Type: {diet_meal['type']}"
            meal_info += ")"
        elif 'type' in diet_meal:
            meal_info += f" (Type: {diet_meal['type']})"

        print(f"\n{meal_info}")
        print("-" * 40)

        try:
            # Calculate nutrition for this meal
            if not summary_only:
                meal_totals = calculate_meal(meal_name)
            else:
                # For summary mode, calculate silently
                meal_totals = calculate_meal_silent(meal_name)

            if meal_totals:
                # Add meal totals to diet totals
                add_to_totals(diet_totals, meal_totals)
                calculated_meals.append(meal_name)
            else:
                missing_meals.append(meal_name)
                print(f"⚠️  Could not calculate nutrition for meal '{meal_name}'")

        except Exception as e:
            missing_meals.append(meal_name)
            print(f"⚠️  Error calculating nutrition for meal '{meal_name}': {str(e)}")

    # Display diet summary
    print("\n" + "=" * 60)
    print("🍽️  TOTAL NUTRITION FOR ENTIRE DIET")
    print("=" * 60)
    print_nutrition_totals(diet_totals)

    # Summary information
    print("\n" + "-" * 60)
    print(f"✔️ Successfully calculated {len(calculated_meals)} out of {len(target_diet['meals'])} meals")

    if missing_meals:
        print(f"⚠️  Could not calculate nutrition for {len(missing_meals)} meals:")
        for meal in missing_meals:
            print(f"   - {meal}")

    print("-" * 60)

    return diet_totals

def add_to_totals(diet_totals, meal_totals):
    """Add meal nutrition totals to diet totals."""
    # Energy
    if meal_totals['energy']['value'] is not None:
        diet_totals['energy']['value'] += meal_totals['energy']['value']

    # Carbohydrates
    if meal_totals['carbohydrates']['value'] is not None:
        diet_totals['carbohydrates']['value'] += meal_totals['carbohydrates']['value']
    if meal_totals['carbohydrates']['sugar'] is not None:
        diet_totals['carbohydrates']['sugar'] += meal_totals['carbohydrates']['sugar']

    # Fat
    if meal_totals['fat']['value'] is not None:
        diet_totals['fat']['value'] += meal_totals['fat']['value']
    if meal_totals['fat']['saturated'] is not None:
        diet_totals['fat']['saturated'] += meal_totals['fat']['saturated']
    if meal_totals['fat']['unsaturated'] is not None:
        diet_totals['fat']['unsaturated'] += meal_totals['fat']['unsaturated']

    # Protein
    if meal_totals['protein']['value'] is not None:
        diet_totals['protein']['value'] += meal_totals['protein']['value']

    # Salt
    if meal_totals['salt']['value'] is not None:
        diet_totals['salt']['value'] += meal_totals['salt']['value']

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

def calculate_meal_silent(meal_name):
    """Calculate meal nutrition without printing details (for summary mode)."""
    import sys
    from io import StringIO

    # Capture stdout to suppress detailed output
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        result = calculate_meal(meal_name)
        return result
    finally:
        sys.stdout = old_stdout
