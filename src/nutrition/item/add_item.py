"""  Script to add a new nutrition item to a YAML file """
from ..utils import save_data
from .load import load

def configure_add_parser(parser):
    """Configure arguments for item add command"""
    parser.set_defaults(func=handle_add)

def handle_add(_args):
    """Handle item add command"""
    add_item()

def get_user_input():
    """Collect user input for all fields in the nutrition data template."""
    title = "Add a new nutrition item"
    print(f"\n{title}\n{'=' * len(title)}")

    # Basic information
    name = input("Item name: ").strip()
    item_type = input("Item type (e.g., Bread, Fruit, Vegetable): ").strip()
    per = input("Values are per (e.g., 100g, 1 piece) [100g]: ").strip() or "100g"

    nutrition_title = f"Nutrition information (per {per}):"
    print(f"\n{nutrition_title}\n{'-' * len(nutrition_title)}")

    # Energy
    energy_input = input("Energy: ").strip()
    energy_value = float(energy_input) if energy_input else None
    energy_unit = input("  Unit [kcal]: ").strip() or "kcal"

    # Carbohydrates
    carbs_value = input("Carbohydrates: ").strip()
    carbs_value = float(carbs_value) if carbs_value else None
    carbs_unit = input("  Unit [g]: ").strip() or "g"
    sugar_value = input("  Sugar: ").strip()
    sugar_value = float(sugar_value) if sugar_value else None

    # Fat
    fat_value = input("Fat: ").strip()
    fat_value = float(fat_value) if fat_value else None
    fat_unit = input("  Unit [g]: ").strip() or "g"
    fat_saturated = input("  Saturated: ").strip()
    fat_saturated = float(fat_saturated) if fat_saturated else None
    fat_unsaturated = input("  Unsaturated: ").strip()
    fat_unsaturated = float(fat_unsaturated) if fat_unsaturated else None

    # Protein
    protein_value = input("Protein: ").strip()
    protein_value = float(protein_value) if protein_value else None
    protein_unit = input("  Unit [g]: ").strip() or "g"

    # Salt
    salt_value = input("Salt: ").strip()
    salt_value = float(salt_value) if salt_value else None
    salt_unit = input("  Unit [g]: ").strip() or "g"

    # Create the data structure
    new_item = {
        'name': name,
        'type': item_type,
        'per': per,
        'nutrition': {
            'energy': {
                'value': energy_value,
                'unit': energy_unit
            },
            'carbohydrates': {
                'value': carbs_value,
                'unit': carbs_unit,
                'sugar': sugar_value
            },
            'fat': {
                'value': fat_value,
                'unit': fat_unit,
                'saturated': fat_saturated,
                'unsaturated': fat_unsaturated
            },
            'protein': {
                'value': protein_value,
                'unit': protein_unit
            },
            'salt': {
                'value': salt_value,
                'unit': salt_unit
            }
        }
    }

    return new_item

def add_item():
    """Main function to add a new nutrition item."""
    existing_data, file = load()
    new_item = get_user_input()
    existing_data.append(new_item)
    save_data(existing_data, file)

    print(f"\n✔️ Successfully added '{new_item['name']}' to {file}")
