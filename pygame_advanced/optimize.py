import numpy as np
import pygame

class VectorizedPolygons:
    """
    A NumPy-backed class to handle thousands of polygons simultaneously.
    Stores polygons as an (N, V, 2) float32 array:
      N = number of polygons
      V = number of vertices per polygon
      2 = [x, y] coordinates
    """
    def __init__(self, polygon_data):
        # polygon_data should be shaped (N, V, 2)
        # If a single polygon (V, 2) is passed, wrap it to (1, V, 2)
        data = np.array(polygon_data, dtype=np.float32)
        if data.ndim == 2:
            data = data[np.newaxis, :, :]
        self.data = data

    @classmethod
    def from_polygons(cls, poly_list):
        """
        Constructs the array from a list of custom polygon objects.
        Assumes each polygon object has a '.points' attribute yielding 
        a list/tuple of (x, y) coordinates.
        """
        data = [poly.points for poly in poly_list]
        return cls(data)

    # --- Coordinate Properties ---
    
    @property
    def x(self): 
        return self.data[:, :, 0]
    
    @x.setter
    def x(self, val): 
        self.data[:, :, 0] = val

    @property
    def y(self): 
        return self.data[:, :, 1]
    
    @y.setter
    def y(self, val): 
        self.data[:, :, 1] = val

    # --- Fast Bounding Box (AABB) Properties ---
    
    @property
    def left(self): return np.min(self.x, axis=1)
    
    @property
    def right(self): return np.max(self.x, axis=1)
    
    @property
    def top(self): return np.min(self.y, axis=1)
    
    @property
    def bottom(self): return np.max(self.y, axis=1)

    # --- Transformations ---

    def move_ip(self, dx, dy):
        """Moves all vertices of all polygons by dx, dy in-place."""
        self.data[:, :, 0] += dx
        self.data[:, :, 1] += dy

    def scale_ip(self, scale_x, scale_y, origin=None):
        """
        Scales all polygons in-place.
        If origin is None, scales relative to each polygon's individual centroid.
        """
        if origin is None:
            origin = np.mean(self.data, axis=1, keepdims=True)
        else:
            origin = np.array(origin, dtype=np.float32).reshape(1, 1, 2)
            
        self.data = (self.data - origin) * [scale_x, scale_y] + origin

    def rotate_ip(self, angle_degrees):
        """
        Rotates all polygons around their individual centroids in-place.
        """
        theta = np.radians(angle_degrees)
        c, s = np.cos(theta), np.sin(theta)
        
        centroids = np.mean(self.data, axis=1, keepdims=True)
        shifted = self.data - centroids
        
        x_new = shifted[:, :, 0] * c - shifted[:, :, 1] * s
        y_new = shifted[:, :, 0] * s + shifted[:, :, 1] * c
        
        self.data[:, :, 0] = x_new + centroids[:, 0, 0]
        self.data[:, :, 1] = y_new + centroids[:, 0, 1]

    # --- Collisions ---

    def collidepoint(self, px, py):
        """Vectorized Point-in-Polygon using Ray Casting."""
        x = self.x
        y = self.y
        x_next = np.roll(x, -1, axis=1)
        y_next = np.roll(y, -1, axis=1)

        cond1 = (y > py) != (y_next > py)
        with np.errstate(divide='ignore', invalid='ignore'):
            x_inter = x + (py - y) * (x_next - x) / (y_next - y)
        
        cond2 = px < x_inter
        intersections = cond1 & cond2
        return np.sum(intersections, axis=1) % 2 == 1

    def colliderect(self, other_rect):
        """Fast AABB collision."""
        if isinstance(other_rect, pygame.Rect):
            ox, oy, ow, oh = other_rect.x, other_rect.y, other_rect.w, other_rect.h
        else:
            ox, oy, ow, oh = other_rect

        oright = ox + ow
        obottom = oy + oh
        return (self.left < oright) & (self.right > ox) & \
               (self.top < obottom) & (self.bottom > oy)
    
    # --- Data Access for Drawing ---

    def get_points(self):
        return self.data.tolist()[0]

    def __getitem__(self, index):
        return self.data[index].tolist()[0]

    # --- Math Operators ---
    
    def __mul__(self, scaler):
        self.data *= scaler
        return self
    
    def __add__(self, scaler):
        self.data += scaler
        return self
    
    def __sub__(self, scaler):
        self.data -= scaler
        return self
    
    def __truediv__(self, scaler):
        self.data /= scaler
        return self

    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        return iter(self.data)
    

    