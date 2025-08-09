"""
"nodes" screensaver
adapted from https://github.com/steven-halla/screen_saver
"""

import math
import os
import random
import time

import pygame
from pygame import gfxdraw

# # our import; this will install the handler
import linux_ss_signal


# import sys, signal
# def signal_handler(sig, frame):
#     print(f"{__name__} caught signal {sig}!")
#     sys.exit(0)
# signal.signal(signal.SIGTERM, signal_handler)
# print("local signal handler installed.")


# Initialize Pygame
pygame.init()

# Set up the display
displayInfo = pygame.display.Info()
WIDTH, HEIGHT = displayInfo.current_w, displayInfo.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Screensaver Art")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()


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


# --- Main Loop ---
def main():

    saver = BouncingNodesGraph()

    running = True
    while running:

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #         continue
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             running = False
        #             continue

        saver.step()
        
        pygame.display.flip()
        clock.tick(60)

    # pygame.quit()

if __name__ == "__main__":
    main() 

