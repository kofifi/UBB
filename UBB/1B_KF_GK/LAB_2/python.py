import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants for screen dimensions and polygon properties
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
NUM_SIDES = 4
RADIUS = 150
BG_COLOR = pygame.Color('yellow')

# Custom center positions for each key press
CENTER_POSITIONS = {
    pygame.K_1: (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
    pygame.K_2: (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
    # ... Add more custom positions for keys 3-9
}

# Rotation angles for each key 1-9
ROTATION_ANGLES = {
    pygame.K_1: math.radians(-45),
    pygame.K_2: math.radians(0),
    # ... Complete with the other angles for keys 3-9
}

# Scale factors for each key press
SCALE_FACTORS = {
    pygame.K_1: (0.5, 0.5),
    pygame.K_2: (1.0, 1.0),
    # ... Add more scale factors for keys 3-9
}

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("18-sided Polygon with Rotation")

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

# Set default values for the center position and scale factor
center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
scale_factor = (1.0, 1.0)
rotation_angle = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                # Reset the rotation angle and scale factor
                rotation_angle = 0
                scale_factor = SCALE_FACTORS[pygame.K_1]
                # Reset the center position
                center_x, center_y = CENTER_POSITIONS[pygame.K_1]
            elif event.key in ROTATION_ANGLES:
                # Update the rotation angle, scale factor, and center position based on the key pressed
                rotation_angle = ROTATION_ANGLES[event.key]
                scale_factor = SCALE_FACTORS.get(event.key, (1.0, 1.0))
                center_x, center_y = CENTER_POSITIONS.get(event.key, (center_x, center_y))

    # Calculate the points of the polygon
    polygon_points = calculate_polygon_points(center_x, center_y, NUM_SIDES, RADIUS, scale_factor, rotation_angle)

    # Fill the background color
    screen.fill(BG_COLOR)

    # Draw the polygon
    pygame.draw.polygon(screen, (0, 0, 0), polygon_points)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
