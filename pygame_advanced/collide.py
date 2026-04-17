import pygame
import math
import numpy as np

# ------------------------
# INTERNAL HELPERS
# ------------------------

def get_points(obj):
    """Always returns points as (V, 2) array/list."""
    pts = obj.points

    # VectorizedPolygons
    if hasattr(pts, "data"):
        data = pts.data  # (N, V, 2)

        if data.ndim == 3:
            return data[0].astype(float)  # take first polygon → (V, 2)

        return data

    # Fallback
    if hasattr(pts, "get_points"):
        return pts.get_points()

    return pts


# ------------------------
# RECT COLLISIONS
# ------------------------

def rect_rect(a: pygame.Rect, b: pygame.Rect) -> bool:
    return a.colliderect(b)


# ------------------------
# CIRCLE COLLISIONS
# ------------------------

def circle_circle(a, b) -> bool:
    dx = a.circle.x - b.circle.x
    dy = a.circle.y - b.circle.y
    return (dx * dx + dy * dy) <= (a.radius + b.radius) ** 2


def rect_circle(rect: pygame.Rect, circle) -> bool:
    closest_x = max(rect.left, min(circle.circle.x, rect.right))
    closest_y = max(rect.top, min(circle.circle.y, rect.bottom))

    dx = circle.circle.x - closest_x
    dy = circle.circle.y - closest_y

    return (dx * dx + dy * dy) <= (circle.radius ** 2)


# ------------------------
# LINE COLLISIONS
# ------------------------

def line_rect(line, rect: pygame.Rect) -> bool:
    pts = get_points(line)

    if len(pts) < 2:
        return False

    thickness = getattr(line, "thickness", 1)

    # Broad phase
    if not line_aabb(line).inflate(thickness, thickness).colliderect(rect):
        return False

    # Narrow phase
    for i in range(len(pts) - 1):
        p1 = to_point(pts[i])
        p2 = to_point(pts[i + 1])

        if segment_rect(p1, p2, rect, thickness):
            return True

    return False

def to_point(p):
    return (float(p[0]), float(p[1]))

def segment_rect(p1, p2, rect, thickness=1):
    p1 = to_point(p1)
    p2 = to_point(p2)

    padded = rect.inflate(thickness, thickness)

    if padded.collidepoint(p1) or padded.collidepoint(p2):
        return True

    edges = [
        ((rect.left, rect.top), (rect.right, rect.top)),
        ((rect.right, rect.top), (rect.right, rect.bottom)),
        ((rect.right, rect.bottom), (rect.left, rect.bottom)),
        ((rect.left, rect.bottom), (rect.left, rect.top)),
    ]

    for e1, e2 in edges:
        if segment_intersect(p1, p2, e1, e2):
            return True

    return False
def segment_intersect(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and \
           (ccw(p1, p2, p3) != ccw(p1, p2, p4))


# ------------------------
# POLYGON (AABB fallback)
# ------------------------
def polygon_aabb(poly):
    pts = get_points(poly)

    xs = [float(p[0]) for p in pts]
    ys = [float(p[1]) for p in pts]

    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)

    return pygame.Rect(
        int(min_x),
        int(min_y),
        int(max_x - min_x),
        int(max_y - min_y)
    )


def polygon_rect(poly, rect: pygame.Rect) -> bool:
    return polygon_aabb(poly).colliderect(rect)


def polygon_circle(poly, circle) -> bool:
    return polygon_aabb(poly).colliderect(circle_aabb(circle))


def polygon_polygon(a, b) -> bool:
    return polygon_aabb(a).colliderect(polygon_aabb(b))


# ------------------------
# LINE HELPERS
# ------------------------

def line_aabb(line):
    pts = get_points(line)

    xs = [float(p[0]) for p in pts]
    ys = [float(p[1]) for p in pts]

    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)

    return pygame.Rect(
        int(min_x),
        int(min_y),
        int(max_x - min_x),
        int(max_y - min_y)
    )

# ------------------------
# HELPERS
# ------------------------

def circle_aabb(circle):
    return pygame.Rect(
        circle.circle.x - circle.radius,
        circle.circle.y - circle.radius,
        circle.radius * 2,
        circle.radius * 2
    )


# ------------------------
# MAIN DISPATCH
# ------------------------

def collide(a, b) -> bool:
    # Rect
    if isinstance(a, pygame.Rect) and isinstance(b, pygame.Rect):
        return rect_rect(a, b)

    # Circle
    if hasattr(a, "radius") and hasattr(b, "radius"):
        return circle_circle(a, b)

    # Rect ↔ Circle
    if isinstance(a, pygame.Rect) and hasattr(b, "radius"):
        return rect_circle(a, b)

    if hasattr(a, "radius") and isinstance(b, pygame.Rect):
        return rect_circle(b, a)

    # Line ↔ Rect
    if hasattr(a, "points") and isinstance(b, pygame.Rect):
        return line_rect(a, b)

    if hasattr(b, "points") and isinstance(a, pygame.Rect):
        return line_rect(b, a)

    # Polygon fallback
    if hasattr(a, "points") and hasattr(b, "points"):
        return polygon_polygon(a, b)

    return False