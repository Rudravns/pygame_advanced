from numpy import size
import os, pygame, sys, json

def load_json(path: str) -> dict:
    try:
        with open(path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print(f"Error: File '{path}' is not a valid JSON file.")
                return {}
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return {}

def save_json(data: dict, path: str, indent=4) -> None:
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=indent)
    except Exception as e:
        print(f"Error: Unable to save JSON data to '{path}': {e}")


def load_font(name: str, size: int, bold: bool = False) -> pygame.font.Font:
    """
    Load a font from disk based on the family name and style.
    Automatically grabs the -Bold.ttf variant if bold=True.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Determine which file variant to load based on the bold flag
    style = "Bold" if bold else "Regular"
    filename = f"{name}-{style}.ttf"

    # 1st try: Look inside a subfolder (e.g., Assets/Fonts/Rajdhani/Rajdhani-Regular.ttf)
    font_path = os.path.join(script_dir, name, filename)

    # 2nd try: Look in the main Fonts folder (e.g., Assets/Fonts/Rajdhani-Regular.ttf)
    if not os.path.exists(font_path):
        font_path = os.path.join(script_dir, filename)
        
    try:
        return pygame.font.Font(font_path, size)
    except Exception as e:
        print(f"Warning: Unable to load custom font '{filename}': {e}. Falling back to Arial.")
        # Fallback to standard system font
        sys_font = pygame.font.SysFont("Arial", size)
        sys_font.set_bold(bold)
        return sys_font