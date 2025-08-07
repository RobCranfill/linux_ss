"""
tunnel screensaver
based on https://github.com/steven-halla/screen_saver
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


# --- Infinite Tunnel Effect ---
class InfiniteTunnel:
    def __init__(self):
        self.num_rings = 18
        self.rings = []
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.max_depth = 1.0
        self.min_depth = 0.08
        self.speed = 0.012
        self.hue_offset = random.random() * 360
        self.frame = 0
        self.reset_rings()

    def reset_rings(self):
        self.rings = []
        for i in range(self.num_rings):
            depth = self.min_depth + (self.max_depth - self.min_depth) * (i / self.num_rings)
            self.rings.append(self._make_ring(depth))

    def _make_ring(self, depth):
        sides = random.randint(6, 16)
        twist = random.uniform(-math.pi, math.pi)
        hue = (self.hue_offset + random.uniform(-40, 40)) % 360
        return {
            'depth': depth,
            'sides': sides,
            'twist': twist,
            'hue': hue,
            'sat': random.uniform(0.6, 1.0),
            'val': random.uniform(0.7, 1.0)
        }

    def hsv2rgb(self, h, s, v):
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
        return int(r*255), int(g*255), int(b*255)

    def draw(self):
        screen.fill((0, 0, 0))
        self.frame += 1
        for ring in self.rings:
            # Move ring forward
            ring['depth'] -= self.speed * (1 + 0.2 * math.sin(self.frame * 0.01))
            if ring['depth'] < self.min_depth:
                # Reset to back with new properties
                ring.update(self._make_ring(self.max_depth))
                ring['depth'] = self.max_depth
            # Calculate size
            scale = 1.0 / ring['depth']
            radius = int(min(WIDTH, HEIGHT) * 0.18 * scale)
            # Color morphing
            hue = (ring['hue'] + self.frame * 0.7) % 360
            color = self.hsv2rgb(hue, ring['sat'], ring['val'])
            # Polygon points
            points = []
            for i in range(ring['sides']):
                angle = 2 * math.pi * i / ring['sides'] + ring['twist'] + self.frame * 0.01 * (1 + 0.5 * math.sin(ring['hue']))
                x = self.center[0] + math.cos(angle) * radius
                y = self.center[1] + math.sin(angle) * radius
                points.append((x, y))
            if len(points) > 2:
                pygame.draw.polygon(screen, color, points, width=6)
                # Optionally fill with a faint color
                faint = (color[0]//3, color[1]//3, color[2]//3, 60)
                poly_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(poly_surf, faint, points)
                screen.blit(poly_surf, (0, 0))


# --- Main Loop ---
def main():
    saver = InfiniteTunnel()
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
        clock.tick(60)

    # pygame.quit()

if __name__ == "__main__":
    main() 

