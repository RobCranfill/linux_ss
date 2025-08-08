"""
kaleidoscope screen saver
from https://github.com/steven-halla/screen_saver

this thing is awfully slow. something wrong?
"""

import math
import random

import pygame
from pygame import gfxdraw


# Initialize Pygame
pygame.init()

# Set up the display
displayInfo = pygame.display.Info()
WIDTH, HEIGHT = displayInfo.current_w, displayInfo.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Screensaver Art")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# --- Kaleidoscope Effect ---
class Kaleidoscope:
    def __init__(self, n_segments, min_shapes, max_shapes):
        self.angle = 0

        # cran
        # self.segments = 24
        self.segments = n_segments
        self.min_shapes = min_shapes
        self.max_shapes = max_shapes

        self.radius = int(min(WIDTH, HEIGHT) * 0.45)
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.shapes = []

        self.generate_shapes()


    def generate_shapes(self):
        self.shapes = []

        # cran
        # num_shapes = random.randint(20, 40)
        # FIXME: shapes_min are insance varrs
        num_shapes = random.randint(self.min_shapes, self.max_shapes)
        
        for _ in range(num_shapes):
            shape = {
                'points': [],
                'color': (
                    random.randint(80, 255),
                    random.randint(80, 255),
                    random.randint(80, 255)
                ),
                'size': random.randint(int(self.radius * 0.3), int(self.radius * 0.9)),
                'rotation': random.uniform(0, 2 * math.pi),
                'alpha': random.randint(120, 255)
            }

            # FIXME: parameterize num points?
            num_points = random.randint(8, 24)
            for _ in range(num_points):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(shape['size'] * 0.5, shape['size'])
                x = math.cos(angle) * distance
                y = math.sin(angle) * distance
                shape['points'].append((x, y))
            self.shapes.append(shape)

    def draw(self):
        screen.fill((0,0,0))
        for i in range(self.segments):
            segment_angle = (2 * math.pi / self.segments) * i + self.angle
            for shape in self.shapes:
                points = []
                for x, y in shape['points']:
                    total_angle = segment_angle + shape['rotation']
                    rotated_x = x * math.cos(total_angle) - y * math.sin(total_angle)
                    rotated_y = x * math.sin(total_angle) + y * math.cos(total_angle)
                    screen_x = int(self.center[0] + rotated_x)
                    screen_y = int(self.center[1] + rotated_y)
                    points.append((screen_x, screen_y))
                if len(points) > 2:
                    shape_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    color_with_alpha = (*shape['color'], shape['alpha'])
                    pygame.draw.polygon(shape_surf, color_with_alpha, points)
                    screen.blit(shape_surf, (0, 0))

        # FIXME: parameterize angle increment?
        self.angle += 0.008
        if self.angle >= 2 * math.pi:
            self.angle = 0
            self.generate_shapes()


# --- Main Loop ---
def main():

    saver = Kaleidoscope(8, 4, 8)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                continue

        saver.draw()
        pygame.display.flip()

        # clock.tick(60)
        clock.tick()

    pygame.quit()

if __name__ == "__main__":
    main() 

