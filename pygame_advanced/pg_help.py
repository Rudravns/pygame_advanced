import pygame
import pygame.freetype
import sys
from . import vars, disk
from typing import Optional, Tuple

def quick_quit():
    pygame.quit()
    sys.exit()

_font_cache = {}

def render_text(
        text: str,
        position,
        size: int|float = 50,
        color: str | pygame.Color | tuple[int, int, int] = "#000000",
        font: Optional[str | pygame.font.Font] = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        draw: bool = True,
        centered: bool = False,
        surface: Optional[pygame.Surface] = None
) -> Tuple[pygame.Surface, pygame.Rect]:
    """Render text to the active display surface."""

    if surface:
        screen = surface
    else:
        screen = pygame.display.get_surface()

    if screen is None and draw:
        raise RuntimeError("Display surface not initialized. Call pygame.display.set_mode().")

    scaled_size = int(size*vars.SCALE["overall"])


    # 1. Determine font object or string name
    if isinstance(font, pygame.font.Font):
        font_obj = font
        # Apply pseudo-styles directly to an existing font object
        font_obj.set_bold(bold)
        font_obj.set_italic(italic)
        font_obj.set_underline(underline)
    else:
        # Default to Arial if no font is specified
        font_name = font if font is not None else "Arial"
        
        # Unique cache key based on all styling parameters
        key = (font_name, scaled_size, bold, italic, underline)
        
        if key not in _font_cache:
            # Check if it's one of our custom downloaded fonts
            if font_name in ["Rajdhani", "Silkscreen"]:
                # Load the custom file (handles bold internally by picking correct .ttf)
                new_font = disk.load_font(font_name, scaled_size, bold) # pyright: ignore[reportCallIssue]
                new_font.set_italic(italic)
                new_font.set_underline(underline)
            else:
                # Load standard system font
                new_font = pygame.font.SysFont(font_name, scaled_size)
                new_font.set_bold(bold)
                new_font.set_italic(italic)
                new_font.set_underline(underline)
                
            _font_cache[key] = new_font
        
        font_obj = _font_cache[key]

    # 2. Convert color string to pygame.Color
    if isinstance(color, str):
        color = pygame.Color(color)  # type: ignore

    # 3. Render text
    text_surface = font_obj.render(str(text), True, color) # pyright: ignore[reportOptionalMemberAccess]
    
    scaled_pos = (position[0]*vars.SCALE["width"], position[1]*vars.SCALE["height"])
    
    if centered:
        text_rect = text_surface.get_rect(center=scaled_pos)
    else:
        text_rect = text_surface.get_rect(topleft=scaled_pos)
    
    if draw:
        vars.DISPLAY.blit(text_surface, text_rect)

    return text_surface, text_rect