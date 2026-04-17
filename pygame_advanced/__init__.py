"""
**Description**: A python/pygame module to extend the features of pygame-ce
"""

# 1. Package Metadata
__version__ = "0.1.0"
__author__ = "Rudransh Kumar"

# 2. Package-level Constants/Configuration
DEFAULT_SETTING = True

# 3. Simplify Imports (Expose internal modules at the package level)
# This allows: from your_package import MainClass
from .main import *
from .vars import *
from .pg_help import *
from .pg_obj import *
from .collide import *
from .disk import *



# 4. Define Public API
# Controls what is exported when a user runs: from your_package import *
__all__ = [
    "create_display",

    "FULLSCREEN_SIZE", "BASE_SIZE","FULLSCREEN", "FULLSCREEN_KEY",

    "quick_quit", "render_text", 

    "Rect", "Circle", "Polygon", "Line", 

    "collide",

    "load_json", "save_json", "load_font",

]

# 5. Initialization Logic (Optional)
# This runs only once when the package is first imported
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
