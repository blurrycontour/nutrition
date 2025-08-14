import argparse

import nutrition.meal as nutmeal
import nutrition.item as nutitem
import nutrition.config as nutcfg
import nutrition.diet as nutdiet
from .__version__ import get_version


def main():
    """
    Main entry point for the Nutrition CLI
    """
    cli = argparse.ArgumentParser(description="Nutrition CLI")
    cli.add_argument("--version", "-v", action="version", version=get_version())
    subparsers = cli.add_subparsers(dest="object", help="Available commands")


    # Item subcommand
    item_parser = subparsers.add_parser("item", aliases=["items"], help="Item management")
    item_subparsers = item_parser.add_subparsers(dest="action", help="Actions")
    # Item add subcommand
    item_add_parser = item_subparsers.add_parser("add", aliases=["create"], help="Add a new food item")
    nutitem.configure_add_parser(item_add_parser)
    # Item get subcommand
    item_get_parser = item_subparsers.add_parser("get", aliases=["show", "calc"], help="Get food item information")
    nutitem.configure_get_parser(item_get_parser)
    # Item remove subcommand
    item_remove_parser = item_subparsers.add_parser("remove", aliases=["delete", "rm"], help="Remove a food item")
    nutitem.configure_remove_parser(item_remove_parser)
    # Item update subcommand
    item_update_parser = item_subparsers.add_parser("update", aliases=["edit"], help="Update a food item")
    nutitem.configure_update_parser(item_update_parser)


    # Meal subcommand
    meal_parser = subparsers.add_parser("meal", aliases=["meals"], help="Meal management")
    meal_subparsers = meal_parser.add_subparsers(dest="action", help="Actions")
    # Meal add subcommand
    meal_add_parser = meal_subparsers.add_parser("add", aliases=["create"], help="Add a new meal")
    nutmeal.configure_add_parser(meal_add_parser)
    # Meal get subcommand
    meal_get_parser = meal_subparsers.add_parser("get", aliases=["show"], help="Get meal information")
    nutmeal.configure_get_parser(meal_get_parser)
    # Meal remove subcommand
    meal_remove_parser = meal_subparsers.add_parser("remove", aliases=["delete", "rm"], help="Remove a meal")
    nutmeal.configure_remove_parser(meal_remove_parser)
    # Meal update subcommand
    meal_update_parser = meal_subparsers.add_parser("update", aliases=["edit"], help="Update a meal")
    nutmeal.configure_update_parser(meal_update_parser)
    # Meal calculate subcommand
    meal_calculate_parser = meal_subparsers.add_parser("calculate", aliases=["calc"], help="Calculate nutrition for a meal")
    nutmeal.configure_calculate_parser(meal_calculate_parser)


    # Diet subcommand
    diet_parser = subparsers.add_parser("diet", aliases=["diets"], help="Diet plan management")
    diet_subparsers = diet_parser.add_subparsers(dest="action", help="Actions")
    # Diet add subcommand
    diet_add_parser = diet_subparsers.add_parser("add", aliases=["create"], help="Add a new diet plan")
    nutdiet.configure_add_parser(diet_add_parser)
    # Diet get subcommand
    diet_get_parser = diet_subparsers.add_parser("get", aliases=["show"], help="Get diet plan information")
    nutdiet.configure_get_parser(diet_get_parser)
    # Diet remove subcommand
    diet_remove_parser = diet_subparsers.add_parser("remove", aliases=["delete", "rm"], help="Remove a diet plan")
    nutdiet.configure_remove_parser(diet_remove_parser)
    # Diet update subcommand
    diet_update_parser = diet_subparsers.add_parser("update", aliases=["edit"], help="Update a diet plan")
    nutdiet.configure_update_parser(diet_update_parser)
    # Diet calculate subcommand
    diet_calculate_parser = diet_subparsers.add_parser("calculate", aliases=["calc"], help="Calculate total nutrition for a diet plan")
    nutdiet.configure_calculate_parser(diet_calculate_parser)


    # Config subcommand
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(dest="action", help="Config actions")
    # Config add subcommand
    config_add_parser = config_subparsers.add_parser("add", aliases=["create"], help="Create a new configuration")
    nutcfg.configure_add_parser(config_add_parser)
    # Config get subcommand
    config_get_parser = config_subparsers.add_parser("get", aliases=["show"], help="Get current configuration")
    nutcfg.configure_get_parser(config_get_parser)
    # Config set subcommand
    config_set_parser = config_subparsers.add_parser("set", help="Set configuration")
    nutcfg.configure_set_parser(config_set_parser)
    # Config remove subcommand
    config_remove_parser = config_subparsers.add_parser("remove", aliases=["delete", "rm"], help="Remove a configuration")
    nutcfg.configure_remove_parser(config_remove_parser)

    args = cli.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        cli.print_help()
