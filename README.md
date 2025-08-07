# Nutrition CLI Tool

A comprehensive command-line tool for managing nutritional information and analyzing meals. Track food items, create meals, and calculate total nutrition values with ease.

## Features

### 🥗 Food Item Management
- **Add** new food items with complete nutritional information
- **Get** detailed nutrition facts for individual items or list all items
- **Update** existing food items with new nutritional data
- **Remove** food items from your database

### 🍽️ Meal Management
- **Create** meals by combining multiple food items with quantities
- **View** meal compositions and ingredients
- **Update** meal recipes and portions
- **Delete** meals from your collection
- **Calculate** total nutritional values for complete meals

### ⚙️ Configuration Management
- **Set** custom configuration files for flexible data storage
- **View** current configuration and data file locations
- Supports multiple data sources and environments

## Installation

### From Source
```bash
git clone <repository-url>
cd nutrition
pip install -e .
```

### Requirements
- Python 3.12+
- PyYAML

## Quick Start

### 1. Set up configuration
```bash
# Set your data files location
nut config set --file /path/to/your/config.yaml
```

### 2. Add some food items
```bash
# Interactive mode - will prompt for all nutrition data
nut item add

# Example: Adding an apple
Item name: Apple
Item type: Fruit
Values are per: 100g
Energy: 52
  Unit: kcal
Carbohydrates: 14
  Unit: g
  Sugar: 10.4
# ... continue with other nutrition fields
```

### 3. Create a meal
```bash
# Interactive meal creation
nut meal add

Meal name: Healthy Breakfast
Item 1:
  Item name: Oats
  Quantity: 50
  Unit: g
Item 2:
  Item name: Banana
  Quantity: 1
  Unit: pcs
# Press Enter to finish adding items
```

### 4. Calculate meal nutrition
```bash
nut meal calculate --name "Healthy Breakfast"
```

## Command Reference

### Item Commands

| Command | Description | Example |
|---------|-------------|---------|
| `nut item add` | Add a new food item | `nut item add` |
| `nut item get` | List all items | `nut item get` |
| `nut item get --name "Apple"` | Get specific item details | `nut item get --name "Apple"` |
| `nut item update "Apple"` | Update an existing item | `nut item update "Apple"` |
| `nut item remove "Apple"` | Remove an item | `nut item remove "Apple"` |

### Meal Commands

| Command | Description | Example |
|---------|-------------|---------|
| `nut meal add` | Create a new meal | `nut meal add` |
| `nut meal get` | List all meals | `nut meal get` |
| `nut meal get --name "Breakfast"` | Get specific meal details | `nut meal get --name "Breakfast"` |
| `nut meal update "Breakfast"` | Update an existing meal | `nut meal update "Breakfast"` |
| `nut meal remove "Breakfast"` | Remove a meal | `nut meal remove "Breakfast"` |
| `nut meal calculate --name "Breakfast"` | Calculate total nutrition | `nut meal calculate --name "Breakfast"` |

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `nut config set --file <path>` | Set configuration file | `nut config set --file config.yaml` |
| `nut config show` | Show current configuration | `nut config show` |

## Data Structure

### Food Items
Food items are stored with comprehensive nutritional information:

```yaml
- name: "Apple"
  type: "Fruit"
  per: "100g"
  nutrition:
    energy:
      value: 52
      unit: "kcal"
    carbohydrates:
      value: 14
      unit: "g"
      sugar: 10.4
    fat:
      value: 0.2
      unit: "g"
      saturated: 0.1
      unsaturated: 0.1
    protein:
      value: 0.3
      unit: "g"
    salt:
      value: 0.001
      unit: "g"
```

### Meals
Meals combine multiple food items with specific quantities:

```yaml
- name: "Healthy Breakfast"
  items:
    - name: "Oats"
      quantity: 50
      unit: "g"
    - name: "Banana"
      quantity: 1
      unit: "pcs"
    - name: "Milk"
      quantity: 200
      unit: "ml"
```

### Configuration
The configuration file specifies data file locations:

```yaml
item: "data/items.yaml"
meal: "data/meals.yaml"
```

## Features in Detail

### Smart Number Formatting
- Automatically removes trailing zeros from nutrition values
- Displays clean, readable numbers (5.0 → 5, 3.50 → 3.5)
- Shows "-" for missing or zero values

### Unit Conversion
The meal calculator supports various units:
- **Weight**: g, kg, mg, oz, lb
- **Count**: pcs, pieces, pc
- **Volume**: ml, l (for liquids)
- Automatic conversion to base units for accurate calculations

### Interactive Updates
When updating items or meals, the tool shows current values as defaults:
```bash
nut item update "Apple"
Item name [Apple]:
Energy [52]: 55
# Press Enter to keep existing values, or type new ones
```

### Comprehensive Error Handling
- Clear error messages for missing items
- Validation of user input
- Graceful handling of missing nutrition data
- Unit conversion warnings

## Example Workflow

```bash
# 1. Initial setup
nut config set --file my-nutrition-data.yaml

# 2. Add food items
nut item add  # Add: Oats, Banana, Milk, Honey

# 3. Create a meal
nut meal add  # Create: "Power Breakfast"

# 4. View meal details
nut meal get --name "Power Breakfast"

# 5. Calculate nutrition
nut meal calculate --name "Power Breakfast"
```

**Output:**
```
Calculating nutrition for meal: Power Breakfast
Items in meal: 4
--------------------------------------------------
✓ 50 g of Oats (×0.5)
✓ 1 pcs of Banana (×1)
✓ 200 ml of Milk (×2)
✓ 15 g of Honey (×0.15)
--------------------------------------------------
TOTAL NUTRITION FOR 'Power Breakfast':
  Energy: 425 kcal
  Carbohydrates: 68.5 g
    Sugar: 35.2 g
  Fat: 8.1 g
    Saturated: 4.2 g
    Unsaturated: 3.4 g
  Protein: 16.8 g
  Salt: 0.2 g

✓ Calculated nutrition for 4 items
```

## File Structure

```
nutrition/
├── src/nutrition/
│   ├── cli.py              # Main CLI entry point
│   ├── utils.py            # Shared utilities
│   ├── config/             # Configuration management
│   │   ├── __init__.py
│   │   └── getset.py
│   ├── item/               # Food item CRUD operations
│   │   ├── __init__.py
│   │   ├── add_item.py
│   │   ├── get_item.py
│   │   ├── update_item.py
│   │   ├── remove_item.py
│   │   └── load.py
│   └── meal/               # Meal CRUD operations
│       ├── __init__.py
│       ├── add_meal.py
│       ├── get_meal.py
│       ├── update_meal.py
│       ├── remove_meal.py
│       ├── calculate.py
│       └── load.py
├── data/
│   ├── items.template.yaml    # Template for food items
│   ├── meals.template.yaml    # Template for meals
│   ├── items.yaml            # Your food item database
│   └── meals.yaml            # Your meal database
├── pyproject.toml            # Project configuration
└── README.md
```

## Development

### Running Tests
```bash
pip install -e ".[dev]"
pytest
```

### Code Formatting
```bash
black src/
flake8 src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the project repository.
