import math
import random

def generate_grid(lat, lon, radius=0.01, points=100):
    """
    Generate a circular grid of points around a center coordinate
    """
    grid_points = []
    
    for i in range(points):
        # Generate points in a spiral pattern
        angle = 2 * math.pi * i / points
        r = radius * math.sqrt(i / points)  # Spiral outwards
        
        # Calculate new coordinates
        grid_lat = lat + r * math.cos(angle)
        grid_lon = lon + r * math.sin(angle)
        
        grid_points.append((grid_lat, grid_lon))
    
    return grid_points
