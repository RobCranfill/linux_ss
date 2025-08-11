"""
https://github.com/steven-halla/screen_saver
"""

import pygame
import math
import random
import os
from datetime import datetime
from pygame import gfxdraw
import time

# This will install the SIGTEM handler.
import linux_ss_signal


# Initialize Pygame
pygame.init()

# Set up the display
displayInfo = pygame.display.Info()
WIDTH, HEIGHT = displayInfo.current_w, displayInfo.current_h

# cran: my 4K display, scaled by 1.5
# WIDTH, HEIGHT = 3840//1.5, 2160//1.5

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Screensaver Art")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Create screenshots directory
SCREENSHOTS_DIR = os.path.expanduser("~/Pictures/kaleidoscope_bg")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# --- Kaleidoscope Effect ---
class Kaleidoscope:
    def __init__(self):
        self.angle = 0

        # cran
        # self.segments = 24
        self.segments = 8

        self.radius = int(min(WIDTH, HEIGHT) * 0.45)
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.shapes = []
        self.generate_shapes()

    def generate_shapes(self):
        self.shapes = []

        # cran
        # num_shapes = random.randint(20, 40)
        num_shapes = random.randint(10, 20)
        
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
            num_points = random.randint(8, 24)
            for _ in range(num_points):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(shape['size'] * 0.5, shape['size'])
                x = math.cos(angle) * distance
                y = math.sin(angle) * distance
                shape['points'].append((x, y))
            self.shapes.append(shape)

    def draw(self):
        screen.fill(BLACK)
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
        self.angle += 0.008
        if self.angle >= 2 * math.pi:
            self.angle = 0
            self.generate_shapes()

# --- Bouncing Nodes Graph Effect ---
class BouncingNodesGraph:
    def __init__(self):
        self.num_nodes = random.randint(32, 48)
        self.nodes = []
        self.edges = []
        self.init_graph()
        self.frames_since_kick = 0
        self.start_time = time.time()

    def init_graph(self):
        self.nodes = []
        self.edges = []
        for _ in range(self.num_nodes):
            node = {
                'pos': [random.uniform(100, WIDTH-100), random.uniform(100, HEIGHT-100)],
                'vel': [random.uniform(-6, 6), random.uniform(-6, 6)],
                'radius': random.randint(10, 18),
                'color': (
                    random.randint(120, 255),
                    random.randint(120, 255),
                    random.randint(120, 255)
                ),
                'damp_freq': random.uniform(0.1, 0.5),
                'damp_phase': random.uniform(0, 2 * math.pi),
                'damp_amp': random.uniform(0.01, 0.04)
            }
            self.nodes.append(node)
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if random.random() < 0.12:
                    self.edges.append((i, j))
        self.frames_since_kick = 0
        self.start_time = time.time()

    def update(self):
        t = time.time() - self.start_time
        for i, node in enumerate(self.nodes):
            for j, other in enumerate(self.nodes):
                if i == j:
                    continue
                dx = node['pos'][0] - other['pos'][0]
                dy = node['pos'][1] - other['pos'][1]
                dist = math.hypot(dx, dy) + 0.1
                if dist < 120:
                    force = 1.5 / dist
                    node['vel'][0] += force * dx / dist
                    node['vel'][1] += force * dy / dist
        for (i, j) in self.edges:
            node1 = self.nodes[i]
            node2 = self.nodes[j]
            dx = node2['pos'][0] - node1['pos'][0]
            dy = node2['pos'][1] - node1['pos'][1]
            dist = math.hypot(dx, dy) + 0.1
            target = 180
            spring = 0.008
            force = spring * (dist - target)
            fx = force * dx / dist
            fy = force * dy / dist
            node1['vel'][0] += fx
            node1['vel'][1] += fy
            node2['vel'][0] -= fx
            node2['vel'][1] -= fy
        for node in self.nodes:
            osc = math.sin(t * node['damp_freq'] + node['damp_phase'])
            damping = 0.96 + node['damp_amp'] * osc
            node['pos'][0] += node['vel'][0]
            node['pos'][1] += node['vel'][1]
            node['vel'][0] *= damping
            node['vel'][1] *= damping
            if node['pos'][0] < node['radius'] or node['pos'][0] > WIDTH - node['radius']:
                node['vel'][0] *= -1
            if node['pos'][1] < node['radius'] or node['pos'][1] > HEIGHT - node['radius']:
                node['vel'][1] *= -1
            node['pos'][0] = max(node['radius'], min(WIDTH - node['radius'], node['pos'][0]))
            node['pos'][1] = max(node['radius'], min(HEIGHT - node['radius'], node['pos'][1]))
            speed = math.hypot(node['vel'][0], node['vel'][1])
            if speed < 0.5:
                node['vel'][0] += random.uniform(-12, 12)
                node['vel'][1] += random.uniform(-12, 12)

        self.frames_since_kick += 1
        if self.frames_since_kick > 120:
            avg_speed = sum(math.hypot(n['vel'][0], n['vel'][1]) for n in self.nodes) / len(self.nodes)
            if avg_speed < 0.7:
                for node in self.nodes:
                    node['vel'][0] += random.uniform(-2, 2)
                    node['vel'][1] += random.uniform(-2, 2)
            self.frames_since_kick = 0

    def draw(self):
        screen.fill((10, 10, 20))
        for (i, j) in self.edges:
            n1 = self.nodes[i]
            n2 = self.nodes[j]
            color = (
                (n1['color'][0] + n2['color'][0]) // 2,
                (n1['color'][1] + n2['color'][1]) // 2,
                (n1['color'][2] + n2['color'][2]) // 2,
                120
            )
            pygame.draw.aaline(screen, color, n1['pos'], n2['pos'])
        for node in self.nodes:
            pygame.gfxdraw.filled_circle(screen, int(node['pos'][0]), int(node['pos'][1]), node['radius'], node['color'])
            pygame.gfxdraw.aacircle(screen, int(node['pos'][0]), int(node['pos'][1]), node['radius'], (255,255,255))

    def step(self):
        self.update()
        self.draw()

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

# --- Screensaver Manager ---
class ScreensaverManager:
    def __init__(self):
        self.effects = [Kaleidoscope, BouncingNodesGraph, InfiniteTunnel]
        self.current = None
        self.pick_random_effect()

    def pick_random_effect(self):
        EffectClass = random.choice(self.effects)
        self.current = EffectClass()

    def draw(self):
        if isinstance(self.current, Kaleidoscope):
            self.current.draw()
        elif isinstance(self.current, BouncingNodesGraph):
            self.current.step()
        elif isinstance(self.current, InfiniteTunnel):
            self.current.draw()

    def refresh(self):
        self.pick_random_effect()

# --- Screenshot ---
def save_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screensaver_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    pygame.image.save(screen, filepath)
    print(f"Screenshot saved: {filepath}")

# --- Main Loop ---
def main():
    manager = ScreensaverManager()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    save_screenshot()
                elif event.key == pygame.K_r:
                    manager.refresh()
        manager.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main() 

