from ..console import print_section_title, print_subsection_title, print_success, print_error
from ..utils import save_data
from ..loader import load
from .get_item import get_item


def configure_update_parser(parser):
    """Configure arguments for item update command"""
    parser.add_argument("name", help="Name of the food item to update (accepts regex)")
    parser.set_defaults(func=handle_update)

def handle_update(args):
    """Handle item update command"""
    update_item(args.name)

def get_user_input(existing_item):
    """Collect user input for updating nutrition item fields with existing values as defaults."""
    title = f"Update nutrition item: {existing_item['name']}"
    print_section_title(title)
    print("Press Enter to keep existing values, or type new values to update.")

    # Basic information
    name = input(f"Item name [{existing_item['name']}]: ").strip() or existing_item['name']
    item_type = input(f"Item type [{existing_item['type']}]: ").strip() or existing_item['type']
    per = input(f"Values are per [{existing_item['per']}]: ").strip() or existing_item['per']

    nutrition_title = f"Nutrition information (per {per})"
    print_subsection_title(nutrition_title)

    # Energy
    current_energy = existing_item['nutrition']['energy']['value']
    energy_display = current_energy if current_energy is not None else "None"
    energy_input = input(f"Energy [{energy_display}]: ").strip()
    if energy_input:
        energy_value = float(energy_input) if energy_input.lower() != 'none' else None
    else:
        energy_value = current_energy

    current_energy_unit = existing_item['nutrition']['energy']['unit']
    energy_unit = input(f"  Unit [{current_energy_unit}]: ").strip() or current_energy_unit

    # Carbohydrates
    current_carbs = existing_item['nutrition']['carbohydrates']['value']
    carbs_display = current_carbs if current_carbs is not None else "None"
    carbs_input = input(f"Carbohydrates [{carbs_display}]: ").strip()
    if carbs_input:
        carbs_value = float(carbs_input) if carbs_input.lower() != 'none' else None
    else:
        carbs_value = current_carbs

    current_carbs_unit = existing_item['nutrition']['carbohydrates']['unit']
    carbs_unit = input(f"  Unit [{current_carbs_unit}]: ").strip() or current_carbs_unit

    current_sugar = existing_item['nutrition']['carbohydrates']['sugar']
    sugar_display = current_sugar if current_sugar is not None else "None"
    sugar_input = input(f"  Sugar [{sugar_display}]: ").strip()
    if sugar_input:
        sugar_value = float(sugar_input) if sugar_input.lower() != 'none' else None
    else:
        sugar_value = current_sugar

    # Fat
    current_fat = existing_item['nutrition']['fat']['value']
    fat_display = current_fat if current_fat is not None else "None"
    fat_input = input(f"Fat [{fat_display}]: ").strip()
    if fat_input:
        fat_value = float(fat_input) if fat_input.lower() != 'none' else None
    else:
        fat_value = current_fat

    current_fat_unit = existing_item['nutrition']['fat']['unit']
    fat_unit = input(f"  Unit [{current_fat_unit}]: ").strip() or current_fat_unit

    current_fat_sat = existing_item['nutrition']['fat']['saturated']
    fat_sat_display = current_fat_sat if current_fat_sat is not None else "None"
    fat_sat_input = input(f"  Saturated [{fat_sat_display}]: ").strip()
    if fat_sat_input:
        fat_saturated = float(fat_sat_input) if fat_sat_input.lower() != 'none' else None
    else:
        fat_saturated = current_fat_sat

    current_fat_unsat = existing_item['nutrition']['fat']['unsaturated']
    fat_unsat_display = current_fat_unsat if current_fat_unsat is not None else "None"
    fat_unsat_input = input(f"  Unsaturated [{fat_unsat_display}]: ").strip()
    if fat_unsat_input:
        fat_unsaturated = float(fat_unsat_input) if fat_unsat_input.lower() != 'none' else None
    else:
        fat_unsaturated = current_fat_unsat

    # Protein
    current_protein = existing_item['nutrition']['protein']['value']
    protein_display = current_protein if current_protein is not None else "None"
    protein_input = input(f"Protein [{protein_display}]: ").strip()
    if protein_input:
        protein_value = float(protein_input) if protein_input.lower() != 'none' else None
    else:
        protein_value = current_protein

    current_protein_unit = existing_item['nutrition']['protein']['unit']
    protein_unit = input(f"  Unit [{current_protein_unit}]: ").strip() or current_protein_unit

    # Salt
    current_salt = existing_item['nutrition']['salt']['value']
    salt_display = current_salt if current_salt is not None else "None"
    salt_input = input(f"Salt [{salt_display}]: ").strip()
    if salt_input:
        salt_value = float(salt_input) if salt_input.lower() != 'none' else None
    else:
        salt_value = current_salt

    current_salt_unit = existing_item['nutrition']['salt']['unit']
    salt_unit = input(f"  Unit [{current_salt_unit}]: ").strip() or current_salt_unit

    # Create the updated data structure
    updated_item = {
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

    return updated_item

def update_item(item_name):
    """Update item in the specified YAML file."""
    items, file = load("item")
    item, idx = get_item(item_name, verbose=0)
    if idx is None:
        print_error(f"Item '{item_name}' not found in {file}")
        return None
    elif idx == -1:
        print_error(f"Multiple items matched with '{item_name}' in {file}")
        return None

    updated_item = get_user_input(item)
    items[idx] = updated_item
    save_data(items, file)
    print_success(f"Successfully updated '{item_name}' in {file}")
    return updated_item
