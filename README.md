# Nutrition CLI Tool

A comprehensive command-line tool for managing nutritional information and analyzing meals and diet plans. Track food items, create meals, plan diets, and calculate total nutrition values with ease.

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

### 🗓️ Diet Plan Management
- **Create** comprehensive diet plans with multiple meals
- **Organize** meals by day and meal type (breakfast, lunch, dinner, snack)
- **Update** diet plans with new meals or modifications
- **Remove** diet plans from your collection
- **Calculate** total nutritional values for entire diet plans

### ⚙️ Configuration Management
- **Create** multiple configurations for different data sets
- **Set** and switch between configurations
- **View** current configuration and data file locations
- **Remove** unwanted configurations
- Supports multiple data sources and environments

## Installation

### From Source
#### Option 1
```bash
pip install -U git+<repository-url>
# e.g. pip install -U git+https://github.com/blurrycontour/nutrition.git@main
```
#### Option 2
```bash
git clone <repository-url>
cd nutrition
pip install -e .
```

### Requirements
- Python 3.12+

## Quick Start

### 1. Create a configuration
```bash
# Create a new configuration with data folder
nut config add --name "personal" --set-current
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

### 4. Create a diet plan
```bash
# Interactive diet plan creation
nut diet add

Diet name: Weekly Plan
Description: My weekly nutrition plan
Meal 1:
  Meal name: Healthy Breakfast
  Day: Monday
  Meal type: breakfast
# Continue adding meals...
```

### 5. Calculate nutrition
```bash
# Calculate single meal nutrition
nut meal calculate --name "Healthy Breakfast"

# Calculate entire diet plan nutrition
nut diet calculate --name "Weekly Plan"
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

### Diet Plan Commands

| Command | Description | Example |
|---------|-------------|---------|
| `nut diet add` | Create a new diet plan | `nut diet add` |
| `nut diet get` | List all diet plans | `nut diet get` |
| `nut diet get --name "Weekly Plan"` | Get specific diet plan details | `nut diet get --name "Weekly Plan"` |
| `nut diet update --name "Weekly Plan"` | Update an existing diet plan | `nut diet update --name "Weekly Plan"` |
| `nut diet remove --name "Weekly Plan"` | Remove a diet plan | `nut diet remove --name "Weekly Plan"` |
| `nut diet calculate --name "Weekly Plan"` | Calculate total nutrition for diet | `nut diet calculate --name "Weekly Plan"` |
| `nut diet calculate --name "Weekly Plan" --summary` | Calculate with summary output | `nut diet calc -n "Weekly Plan" -s` |

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `nut config add --name <name>` | Create a new configuration | `nut config add --name "personal"` |
| `nut config set --name <name>` | Set active configuration | `nut config set --name "personal"` |
| `nut config get` | Show current configuration | `nut config get` |
| `nut config get --all` | Show all configurations | `nut config get --all` |
| `nut config remove --name <name>` | Remove a configuration | `nut config remove --name "old-config"` |

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

### Diet Plans
Diet plans organize multiple meals with optional scheduling information:

```yaml
- name: "Weekly Diet Plan"
  description: "A balanced weekly diet plan"
  meals:
    - name: "Healthy Breakfast"
      day: "Monday"
      type: "breakfast"
    - name: "Light Lunch"
      day: "Monday"
      type: "lunch"
    - name: "Protein Dinner"
      day: "Monday"
      type: "dinner"
    - name: "Fruit Snack"
      type: "snack"
```

### Configuration
The configuration file specifies data file locations:

```yaml
current: "personal"
configs:
  - name: "personal"
    item: ".data-personal/items.yaml"
    meal: ".data-personal/meals.yaml"
    diet: ".data-personal/diets.yaml"
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

### Multi-level Configuration
- Support for multiple named configurations
- Easy switching between different data sets
- Automatic data folder creation
- Configuration validation and error handling

### Diet Plan Features
- **Meal Scheduling**: Organize meals by day and type
- **Flexible Structure**: Optional day and meal type fields
- **Comprehensive Calculation**: Total nutrition across all meals
- **Summary Mode**: Condensed output for diet calculations
- **Error Handling**: Graceful handling of missing meals

### Interactive Updates
When updating items, meals, or diets, the tool shows current values as defaults:
```bash
nut item update --name "Apple"
Item name [Apple]:
Energy [52]: 55
# Press Enter to keep existing values, or type new ones

nut diet update --name "Weekly Plan"
Choose an option:
1. Keep existing meals and add new ones
2. Replace all meals with new ones
3. Edit existing meals
```

### Command Aliases
Most commands support convenient aliases:
- `nut item add` = `nut items create`
- `nut meal calc` = `nut meal calculate`
- `nut diet rm` = `nut diet remove` = `nut diet delete`
- `nut config show` = `nut config get`

### Comprehensive Error Handling
- Clear error messages for missing items, meals, or diets
- Validation of user input and data integrity
- Graceful handling of missing nutrition data
- Unit conversion warnings and fallbacks
- Configuration existence checks

## Example Workflow

```bash
# 1. Initial setup
nut config add --name "my-nutrition" --set-current

# 2. Add food items
nut item add  # Add: Oats, Banana, Milk, Honey

# 3. Create meals
nut meal add  # Create: "Power Breakfast"
nut meal add  # Create: "Light Lunch"
nut meal add  # Create: "Protein Dinner"

# 4. Create a diet plan
nut diet add  # Create: "Weekly Plan" with the above meals

# 5. View diet plan details
nut diet get --name "Weekly Plan"

# 6. Calculate nutrition for entire diet
nut diet calculate --name "Weekly Plan"
```

**Diet Calculation Output:**
```
Calculating total nutrition for diet: 'Weekly Plan'
============================================================
Description: A balanced weekly diet plan
Total meals in diet: 3
------------------------------------------------------------

Meal 1: Power Breakfast (Day: Monday, Type: breakfast)
----------------------------------------
Calculating total nutrition for 'Power Breakfast'
--------------------------------------------------
Items in meal: 4
✓ 50 g of Oats (×0.5)
✓ 1 pcs of Banana (×1)
✓ 200 ml of Milk (×2)
✓ 15 g of Honey (×0.15)
💯 Total Nutrition Value
  Energy: 425 kcal
  Carbohydrates: 68.5 g
    Sugar: 35.2 g
  Fat: 8.1 g
    Saturated: 4.2 g
    Unsaturated: 3.4 g
  Protein: 16.8 g
  Salt: 0.2 g

[Similar output for other meals...]

============================================================
🍽️  TOTAL NUTRITION FOR ENTIRE DIET
============================================================
  Energy: 1890 kcal
  Carbohydrates: 245 g
    Sugar: 120 g
  Fat: 45 g
    Saturated: 18 g
    Unsaturated: 22 g
  Protein: 95 g
  Salt: 4.2 g

✓ Successfully calculated 3 out of 3 meals
------------------------------------------------------------
```

## File Structure

```
nutrition/
├── src/nutrition/
│   ├── cli.py              # Main CLI entry point
│   ├── utils.py            # Shared utilities
│   ├── vars.py             # Global variables
│   ├── config/             # Configuration management
│   │   ├── __init__.py
│   │   ├── add_config.py   # Create configurations
│   │   ├── get_config.py   # View configurations
│   │   ├── set_config.py   # Set active configuration
│   │   └── remove_config.py # Remove configurations
│   ├── item/               # Food item CRUD operations
│   │   ├── __init__.py
│   │   ├── add_item.py
│   │   ├── get_item.py
│   │   ├── update_item.py
│   │   ├── remove_item.py
│   │   └── load.py
│   ├── meal/               # Meal CRUD operations
│   │   ├── __init__.py
│   │   ├── add_meal.py
│   │   ├── get_meal.py
│   │   ├── update_meal.py
│   │   ├── remove_meal.py
│   │   ├── calculate.py
│   │   └── load.py
│   └── diet/               # Diet plan CRUD operations
│       ├── __init__.py
│       ├── add_diet.py
│       ├── get_diet.py
│       ├── update_diet.py
│       ├── remove_diet.py
│       ├── calculate.py
│       └── load.py
├── data/
│   ├── items.template.yaml    # Template for food items
│   ├── meals.template.yaml    # Template for meals
│   ├── diets.template.yaml    # Template for diet plans
│   ├── items.yaml            # Your food item database
│   ├── meals.yaml            # Your meal database
│   └── diets.yaml            # Your diet plan database
├── config/
│   └── config.template.yaml   # Configuration template
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
