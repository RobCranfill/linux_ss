"""
 my big bang screensaver
 based on https://pythonprogramming.altervista.org/particles-screensaver-with-pygame/
"""

# TODO: start particiles in a circule, not square?


import math
import random
import pygame


def radians(degrees):
    return degrees*math.pi/180

class Particle:
    def __init__(self, xy, radius, speed, angle, colour, surface):
        self.x = xy[0]
        self.y = xy[1]
        self.speed = speed
        self.angle = angle
        self.radius = radius
        self.surface = surface
        self.colour = colour
        self.rect = pygame.draw.circle(surface,(255,255,0),
                           (int(round(self.x,0)),
                            int(round(self.y,0))),
                            self.radius)
    def move(self):
        """ Update speed and position based on speed, angle """
        # for constant change in position values.
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        # pygame.rect likes int arguments for x and y
        self.rect.x = int(round(self.x))
        self.rect.y = int(round(self.y))

    def draw(self):
        """ Draw the particle on screen"""
        pygame.draw.circle(self.surface, self.colour, self.rect.center, self.radius)

    def bounce(self):
        """ Tests whether a particle has hit the boundary of the environment """

        if self.x > self.surface.get_width() - self.radius: # right
            self.x = 2*(self.surface.get_width() - self.radius) - self.x
            self.angle = - self.angle

        elif self.x < self.radius: # left
            self.x = 2*self.radius - self.x
            self.angle = - self.angle            

        if self.y > self.surface.get_height() - self.radius: # bottom
            self.y = 2*(self.surface.get_height() - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius: # top
            self.y = 2*self.radius - self.y
            self.angle = math.pi - self.angle

def random_rgb():
    r = random.randrange(0,255)
    g = random.randrange(0,255)
    b = random.randrange(0,255)
    return r,g,b

def create_particles(n_particles, max_x, max_y, size, screen):

    particles = []
    for i in range(n_particles):
        color = random_rgb()
        x = max_x / 2 + random.randint(0, size)
        y = max_y / 2 + random.randint(0, size)
        speed = random.randrange(0, 20) * 0.1 + 0.1 # no zero speed particles!
        angle = random.randrange(0, 360)
        radius = 3
        particles.append( Particle((x, y), radius, speed, angle, color, screen) )
    return particles


def main():

    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    screen_info = pygame.display.Info()
    xmax = screen_info.current_w
    ymax = screen_info.current_h

    white = (0, 0, 0)
    black = (200,0,100)
    grey = (255,255,128)

    INITIAL_SIZE = 100

    iter_count = 0
    particles = create_particles(random.randint(500, 2000), xmax, ymax, INITIAL_SIZE, screen)
    iter_max = random.randint(1000, 4000)

    done = False
    while not done:

        iter_count += 1
        if iter_count > iter_max:
            print("Restarting!")
            iter_count = 0
            particles = create_particles(random.randint(500, 2000), xmax, ymax, INITIAL_SIZE, screen)
            iter_max = random.randint(1000, 4000)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.KEYDOWN: #  and event.key == pygame.K_ESCAPE:
                done = True
                break
        if done:
            break

        screen.fill(white)
        for p in particles:
            p.move()
            p.bounce()
            p.draw()

        # bigger number expands faster?
        clock.tick(80)

        pygame.display.flip()

    # pygame.quit()

if __name__ == "__main__":
    main()
