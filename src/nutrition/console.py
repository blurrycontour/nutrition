"""Console output formatting utilities for the Nutrition CLI."""

import shutil


def get_terminal_width():
    """Get the current terminal width, with fallback to 80."""
    try:
        return shutil.get_terminal_size().columns
    except (OSError, AttributeError):
        return 80


def print_header(text, style='=', width=None):
    """Print a header with full-width underline.

    Args:
        text: The header text
        style: Character to use for underline ('=', '-', '━', etc.)
        width: Width of the line (None for terminal width)
    """
    if width is None:
        width = get_terminal_width()

    print(f"\n{text}")
    print(style * width)


def print_subheader(text, style='-', width=None):
    """Print a subheader with full-width underline.

    Args:
        text: The subheader text
        style: Character to use for underline ('=', '-', '━', etc.)
        width: Width of the line (None for terminal width)
    """
    if width is None:
        width = get_terminal_width()

    print(f"\n{text}")
    print(style * width)


def print_separator(style='-', width=None):
    """Print a horizontal separator line.

    Args:
        style: Character to use for the line ('=', '-', '━', etc.)
        width: Width of the line (None for terminal width)
    """
    if width is None:
        width = get_terminal_width()

    print(style * width)


def print_section_title(text, style='='):
    """Print a section title with text-length underline.

    Args:
        text: The section title text
        style: Character to use for underline ('=', '-', '━', etc.)
    """
    print(f"\n{text}")
    print(style * len(text))


def print_subsection_title(text, style='-'):
    """Print a subsection title with text-length underline.

    Args:
        text: The subsection title text
        style: Character to use for underline ('=', '-', '━', etc.)
    """
    print(f"\n{text}")
    print(style * len(text))


def print_success(message):
    """Print a success message with consistent formatting."""
    print(f"✔️ {message}")


def print_error(message):
    """Print an error message with consistent formatting."""
    print(f"❌ {message}")


def print_warning(message):
    """Print a warning message with consistent formatting."""
    print(f"⚠️  {message}")


def print_info(message):
    """Print an info message with consistent formatting."""
    print(f"ℹ️  {message}")


def print_list_header(count, item_type, plural_suffix="s"):
    """Print a standardized list header.

    Args:
        count: Number of items
        item_type: Type of items (e.g., 'item', 'meal', 'diet')
        plural_suffix: Suffix to add for pluralization
    """
    item_word = item_type if count == 1 else f"{item_type}{plural_suffix}"
    print(f"[Found {count} {item_word}]")


def print_nutrition_section(title):
    """Print a nutrition section header with consistent formatting."""
    print_subsection_title(f"{title}:")


def print_item_detail(label, value, indent="  "):
    """Print an item detail with consistent indentation."""
    print(f"{indent}{label}: {value}")


def print_sub_item_detail(label, value, indent="    "):
    """Print a sub-item detail with deeper indentation."""
    print(f"{indent}{label}: {value}")


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
    if formatted_value == "-":
        return "-"
    return f"{formatted_value} {unit}"
