import pygame
from . import vars, optimize
import math
import numpy as np




class Rect(pygame.Rect):
    def __init__(self, x: float, y: float, width: float, height: float, cache = True):
        """
        A wrapper for pygame.Rect that scales based on the display size.
        """
        self.base_x = x
        self.base_y = y
        self.base_width = width
        self.base_height = height
        
        super().__init__(x, y, width, height)
        self.update_scaling()

        #add obj to cache
        if cache:
            vars.ALL_OBJECTS_CACHE.append(self)
    

    def update_scaling(self):
        """Updates the rect dimensions based on the global scale."""
        self.x = int(self.base_x * vars.SCALE["width"])
        self.y = int(self.base_y * vars.SCALE["height"])
        self.width = int(self.base_width * vars.SCALE["width"])
        self.height = int(self.base_height * vars.SCALE["height"])
        self.topleft = (self.x, self.y)


    @property
    def center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)

    @center.setter
    def center(self, value):
        self.base_x = (value[0] / vars.SCALE["width"]) - (self.base_width / 2)
        self.base_y = (value[1] / vars.SCALE["height"]) - (self.base_height / 2)
        self.update_scaling()

    def move_ip(self, dx, dy):
        """Moves the rect in-place based on scaled coordinates."""
        self.base_x += dx / vars.SCALE["width"]
        self.base_y += dy / vars.SCALE["height"]
        self.update_scaling()
    
    def __del__(self):
        vars.ALL_OBJECTS_CACHE.remove(self)

class Circle:
    #use slots

    __slots__ = ("base_x", "base_y", "base_radius", "circle", "radius")

    def __init__(self, x: float, y: float, radius: float, cache = True):
        """
        A wrapper for pygame.Circle that scales based on the display size.
        """
        self.base_x = x
        self.base_y = y
        self.base_radius = radius
        
        self.circle = pygame.math.Vector2(x, y)
        self.update_scaling()
        #add obj to cache
        if cache:
            vars.ALL_OBJECTS_CACHE.append(self)
    
    
    def update_scaling(self):
        """Updates the circle position based on the global scale."""
        self.circle.x = self.base_x * vars.SCALE["width"]
        self.circle.y = self.base_y * vars.SCALE["height"]
        self.radius = self.base_radius * vars.SCALE["width"]
    
    @property
    def center(self):
        return (self.circle.x, self.circle.y)
    
    @center.setter
    def center(self, value):
        self.base_x = value[0] / vars.SCALE["width"]
        self.base_y = value[1] / vars.SCALE["height"]
        self.update_scaling()
    
    def move_ip(self, dx, dy):
        """Moves the circle in-place based on scaled coordinates."""
        self.base_x += dx
        self.base_y += dy
        self.update_scaling()
    
    def distance_to(self, other):
        """Calculates the distance between this circle and another circle."""
        return math.sqrt
    

    def draw(self, color, surface:pygame.Surface | None = None):
        """Draws the circle on the given surface."""
        if surface is None:
            surface = vars.DISPLAY
        pygame.draw.circle(surface, color, (int(self.circle.x), int(self.circle.y)), int(self.radius))
    
    def __del__(self):
        vars.ALL_OBJECTS_CACHE.remove(self)

class Polygon:
    #use slots
    __slots__ = ("base_points", "points", "base_center", "center")


    def __init__(self, points: list[tuple[float, float]], cache = True):
        """
        A wrapper for pygame.Polygon that scales based on the display size.
        """
        self.base_points = optimize.VectorizedPolygons(points)
        self.points = optimize.VectorizedPolygons(points)
        #center of the ploygon
        x = sum(point[0] for point in points) / len(points)
        y = sum(point[1] for point in points) / len(points)
        self.base_center = pygame.Vector2(x, y)
        self.center = pygame.Vector2(x, y)

        self.update_scaling()
        #add obj to cache
        if cache:
            vars.ALL_OBJECTS_CACHE.append(self)

    def update_scaling(self):
        """Updates the polygon points based on the global scale."""
        # Create a fresh copy from base_points to avoid compound scaling
        self.points.data = self.base_points.data.copy()
        
        # Scale both axes correctly
        scale_vec = np.array([vars.SCALE["width"], vars.SCALE["height"]], dtype=np.float32)
        self.points.data *= scale_vec

        # Update the center vector
        self.center.x = self.base_center.x * vars.SCALE["width"]
        self.center.y = self.base_center.y * vars.SCALE["height"]

    def move_ip(self, dx, dy):
        """Moves the polygon in-place based on scaled coordinates."""
        base_dx = dx / vars.SCALE["width"]
        base_dy = dy / vars.SCALE["height"]

        self.base_points.move_ip(base_dx, base_dy)
        self.base_center.x += base_dx
        self.base_center.y += base_dy

        self.update_scaling()

    def draw(self, color, surface:pygame.Surface | None = None):
        if surface is None:
            surface = vars.DISPLAY

        pygame.draw.polygon(surface, color, (self.points.get_points()))

    def __del__(self):
        vars.ALL_OBJECTS_CACHE.remove(self)

class Line:
    __slots__ = ("base_points", "points", "thickness")

    def __init__(self, *args: pygame.Vector2 | tuple[float, float], **kwargs) -> None:
        """
        A high-performance line class. 
        Accepts points as positional arguments: Line(p1, p2, p3...)
        Or via a 'points' keyword argument.
        """
        # Collect points from args and kwargs
        pts = list(args)
        if "points" in kwargs:
            pts.extend(kwargs["points"])

        if not pts:
            # Handle empty initialization safely
            self.base_points = optimize.VectorizedPolygons(np.zeros((0, 2)))
            self.points = optimize.VectorizedPolygons(np.zeros((0, 2)))
        else:
            # Convert to (V, 2) array for VectorizedPolygons
            # We use VectorizedPolygons to handle the math for us
            clean_pts = [list(p) for p in pts]
            self.base_points = optimize.VectorizedPolygons(clean_pts)
            self.points = optimize.VectorizedPolygons(clean_pts)
        
        self.thickness:int = 2
        if "thickness" in kwargs:
            self.thickness = kwargs["thickness"]
        


        self.update_scaling()
        if "cache" in kwargs:
            vars.ALL_OBJECTS_CACHE.append(self) 

    @classmethod
    def from_points(cls, *points: pygame.Vector2 | tuple[float, float]):
        """Alternative constructor using *args."""
        return cls(*points)

    def update_scaling(self):
        """Updates the line points based on the global scale using NumPy."""
        # Prevent cumulative errors: always scale from the base_points
        # We multiply the whole (1, V, 2) array by a [w, h] vector
        scale_vec = np.array([vars.SCALE["width"], vars.SCALE["height"]], dtype=np.float32)
        self.points.data = self.base_points.data * scale_vec

    def move_ip(self, dx, dy):
        """Moves the line in-place based on scaled coordinates."""
        
        # To move the 'base' points correctly, we reverse the scale of the movement
        base_dx = dx / vars.SCALE["width"] if vars.SCALE["width"] != 0 else 0
        base_dy = dy / vars.SCALE["height"] if vars.SCALE["height"] != 0 else 0

        self.base_points.move_ip(base_dx, base_dy)
        self.update_scaling()

    def draw(self, color, surface: pygame.Surface | None = None):
        if surface is None:
            surface = vars.DISPLAY

        pts = self.points.get_points() 

        if len(pts) < 2:
            return

        pygame.draw.lines(surface, color, False, pts, int(self.thickness))
    
    def __del__(self):
        vars.ALL_OBJECTS_CACHE.remove(self)