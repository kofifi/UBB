import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants for screen dimensions and polygon properties
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
NUM_SIDES = 18
RADIUS = 150
BG_COLOR = pygame.Color('yellow')

# Function to calculate the polygon points
def calculate_polygon_points(center_x, center_y, sides, radius, scale_factor, rotation_angle):
    points = []
    angle_step = 2 * math.pi / sides
    for i in range(sides):
        angle = angle_step * i + rotation_angle
        x = center_x + math.cos(angle) * radius * scale_factor[0]
        y = center_y + math.sin(angle) * radius * scale_factor[1]
        points.append((x, y))
    return points

# Updated function to apply shearing to the polygon points on both X and Y
def shear_polygon_points(points, shearing_factor_x, shearing_factor_y):
    sheared_points = [(x + y * shearing_factor_x, y + x * shearing_factor_y) for x, y in points]
    return sheared_points

# https://elearning.ubb.edu.pl/pluginfile.php/122717/mod_resource/content/1/GrafikaKomputerowaLab.pdf
# Initial configuration with separate shearing factors for x and y
configurations = {
    pygame.K_1: {"scale_factor": (0.5, 0.5), "rotation_angle": math.radians(-45), "shearing_factor_x": 0, "shearing_factor_y": 0, "center_x": SCREEN_WIDTH // 2, "center_y": SCREEN_HEIGHT // 2},
    pygame.K_2: {"scale_factor": (1.0, 1.0), "rotation_angle": math.radians(0), "shearing_factor_x": 0.25, "shearing_factor_y": 0, "center_x": SCREEN_WIDTH // 2.60, "center_y": SCREEN_HEIGHT // 2},
    pygame.K_3: {"scale_factor": (0.75, 1.30), "rotation_angle": math.radians(45), "shearing_factor_x": 0, "shearing_factor_y": 0, "center_x": SCREEN_WIDTH // 2, "center_y": SCREEN_HEIGHT // 2},
    pygame.K_4: {"scale_factor": (1.5, 1.0), "rotation_angle": math.radians(-45), "shearing_factor_x": 0.5, "shearing_factor_y": 0, "center_x": SCREEN_WIDTH // 3.60, "center_y": SCREEN_HEIGHT // 2},
    pygame.K_5: {"scale_factor": (1.75, 0.5), "rotation_angle": math.radians(-45), "shearing_factor_x": 0, "shearing_factor_y": 0, "center_x": SCREEN_WIDTH // 2, "center_y": SCREEN_HEIGHT // 11},
    pygame.K_6: {"scale_factor": (1.0, 1.5), "rotation_angle": math.radians(-45), "shearing_factor_x": 0, "shearing_factor_y": -0.5, "center_x": SCREEN_WIDTH // 2, "center_y": SCREEN_HEIGHT // 1.35},
    pygame.K_7: {"scale_factor": (0.75, 1.30), "rotation_angle": math.radians(45), "shearing_factor_x": 0, "shearing_factor_y": 0, "center_x": SCREEN_WIDTH // 2, "center_y": SCREEN_HEIGHT // 2},
    pygame.K_9: {"scale_factor": (2, 1.5), "rotation_angle": math.radians(-135), "shearing_factor_x": 0, "shearing_factor_y": 0.25, "center_x": SCREEN_WIDTH // 1.35, "center_y": SCREEN_HEIGHT // 3.5},

}

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic Scaling Polygon")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key in configurations:
            config = configurations[event.key]
            center_x = config["center_x"]
            center_y = config["center_y"]
            scale_factor = config["scale_factor"]
            rotation_angle = config["rotation_angle"]
            shearing_factor_x = config["shearing_factor_x"]
            shearing_factor_y = config["shearing_factor_y"]

            # Calculate polygon points with current configuration
            polygon_points = calculate_polygon_points(center_x, center_y, NUM_SIDES, RADIUS, scale_factor, rotation_angle)
            # Apply shearing with factors for both axes
            sheared_polygon_points = shear_polygon_points(polygon_points, shearing_factor_x, shearing_factor_y)

            # Clear screen and redraw with new configuration
            screen.fill(BG_COLOR)
            pygame.draw.polygon(screen, (0, 0, 0), sheared_polygon_points)
            pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
