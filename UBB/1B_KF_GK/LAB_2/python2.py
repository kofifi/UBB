import pygame
import sys

class ShapeDrawer:
    def __init__(self, screen):
        self.screen = screen

    def draw_chevron(self, points, color):
        pygame.draw.polygon(self.screen, color, points)

    def draw_circle_with_square(self, circle_center, circle_radius, square_side_length, circle_color, square_color):
        pygame.draw.circle(self.screen, circle_color, circle_center, circle_radius)
        square_top_left = (circle_center[0] - square_side_length / 2, circle_center[1] - square_side_length / 2)
        pygame.draw.rect(self.screen, square_color, (*square_top_left, square_side_length, square_side_length))

    def draw_z_shape(self, top_left, width, height, color, line_width):
        start_top = top_left
        end_top = (start_top[0] + width, start_top[1])
        diagonal_start = end_top
        diagonal_end = (start_top[0], start_top[1] + height)
        start_bottom = diagonal_end
        end_bottom = (start_bottom[0] + width, start_bottom[1])
        pygame.draw.line(self.screen, color, start_top, end_top, line_width)
        pygame.draw.line(self.screen, color, diagonal_start, diagonal_end, line_width)
        pygame.draw.line(self.screen, color, start_bottom, end_bottom, line_width)

    def draw_hourglass(self, top_center, side_length, square_height, color):
        half_side = side_length / 2
        top_triangle = [(top_center[0] - half_side, top_center[1]),
                        (top_center[0] + half_side, top_center[1]),
                        (top_center[0], top_center[1] + half_side)]
        square_top_left = (top_center[0] - half_side, top_center[1] + half_side)
        pygame.draw.polygon(self.screen, color, top_triangle)
        pygame.draw.rect(self.screen, color, (*square_top_left, side_length, square_height))
        bottom_triangle_base_y = square_top_left[1] + square_height
        bottom_triangle = [(top_center[0] - half_side, bottom_triangle_base_y + half_side),
                           (top_center[0] + half_side, bottom_triangle_base_y + half_side),
                           (top_center[0], bottom_triangle_base_y)]
        pygame.draw.polygon(self.screen, color, bottom_triangle)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Shape Drawing")
    screen.fill(pygame.Color('white'))
    drawer = ShapeDrawer(screen)

    # Draw shapes
    drawer.draw_chevron([(600.0, 212.5), (650.0, 150.0), (700.0, 212.5), (700.0, 100.0), (600.0, 100.0)], (0, 255, 0))
    drawer.draw_circle_with_square((200, 150), 40, 40, (0, 0, 0), (255, 255, 0))
    drawer.draw_hourglass((200, 300), 100, 60, (0, 0, 255))

    # Configure and draw the "Z"
    z_width = 150
    z_height = 150
    margin = 100
    z_top_left = (800 - z_width - margin, 600 - z_height - margin)
    drawer.draw_z_shape(z_top_left, z_width, z_height, (255, 0, 0), 5)

    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
