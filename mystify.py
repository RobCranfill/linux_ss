"""
Adapted from https://github.com/avarokins/Mystify
"""
import pygame
import random
import sys

pygame.init()

WIDTH = 1280
HEIGHT = 720
THICKNESS = 3
DIFFERENCE = 25

Color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
BACKGROUND_COLOR = [0, 0, 0]

surface = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

SPEED = int(input("Enter speed(1-5) : "))

# Rectangle 1
Line1 = [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(0, WIDTH), random.randint(0, HEIGHT)]
Line2 = [Line1[2],Line1[3], random.randint(0, WIDTH), random.randint(0, HEIGHT)]
Line3 = [Line2[2],Line2[3], random.randint(0, WIDTH), random.randint(0, HEIGHT)]
Line4 = [Line3[2],Line3[3], Line1[0], Line1[1]]

# Rectangle 2
Line5 = [Line1[0]+DIFFERENCE,Line1[1]+DIFFERENCE,Line1[2]+DIFFERENCE,Line1[3]+DIFFERENCE,]
Line6 = [Line5[2],Line5[3],Line2[2]+DIFFERENCE,Line2[3]+DIFFERENCE]
Line7 = [Line6[2],Line6[3], Line3[2]+DIFFERENCE,Line3[3]+DIFFERENCE,]
Line8 = [Line7[2],Line7[3], Line5[0], Line5[1]]

# Rectangle 3
Line9 = [Line1[0]+2*DIFFERENCE,Line1[1]+2*DIFFERENCE,Line1[2]+2*DIFFERENCE,Line1[3]+2*DIFFERENCE,]
Line10 = [Line9[2],Line9[3],Line2[2]+2*DIFFERENCE,Line2[3]+2*DIFFERENCE]
Line11 = [Line10[2],Line10[3], Line3[2]+2*DIFFERENCE,Line3[3]+2*DIFFERENCE,]
Line12 = [Line11[2],Line11[3], Line9[0], Line9[1]]

# Rectangle 4
Line13 = [Line1[0]+3*DIFFERENCE,Line1[1]+3*DIFFERENCE,Line1[2]+3*DIFFERENCE,Line1[3]+3*DIFFERENCE,]
Line14 = [Line13[2],Line13[3],Line2[2]+3*DIFFERENCE,Line2[3]+3*DIFFERENCE]
Line15 = [Line14[2],Line14[3], Line3[2]+3*DIFFERENCE,Line3[3]+3*DIFFERENCE,]
Line16 = [Line15[2],Line15[3], Line13[0], Line13[1]]


# Rectangle 1
Line1D = [random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED)]
Line2D = [Line1D[2],Line1D[3], random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED)]
Line3D = [Line2D[2],Line2D[3], random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED)]
Line4D = [Line3D[2],Line3D[3], Line1D[0], Line1D[1]]

# Rectangle 2
Line5D = [Line1D[0],Line1D[1],Line1D[2],Line1D[3]]
Line6D = [Line2D[0],Line2D[1],Line2D[2],Line2D[3]]
Line7D = [Line3D[0],Line3D[1],Line3D[2],Line3D[3]]
Line8D = [Line4D[0],Line4D[1],Line4D[2],Line4D[3]]


# Rectangle 3
Line9D = [Line1D[0],Line1D[1],Line1D[2],Line1D[3]]
Line10D = [Line2D[0],Line2D[1],Line2D[2],Line2D[3]]
Line11D = [Line3D[0],Line3D[1],Line3D[2],Line3D[3]]
Line12D = [Line4D[0],Line4D[1],Line4D[2],Line4D[3]]

# Rectangle 4
Line13D = [Line1D[0],Line1D[1],Line1D[2],Line1D[3]]
Line14D = [Line2D[0],Line2D[1],Line2D[2],Line2D[3]]
Line15D = [Line3D[0],Line3D[1],Line3D[2],Line3D[3]]
Line16D = [Line4D[0],Line4D[1],Line4D[2],Line4D[3]]


def changeDirection(Line, LineD):
    if Line[0] < 0 or Line[0] > WIDTH:
        LineD[0] = -LineD[0]
    if Line[1] < 0 or Line[1] > HEIGHT:
        LineD[1] = -LineD[1]
    if Line[2] < 0 or Line[2] > WIDTH:
        LineD[2] = -LineD[2]
    if Line[3] < 0 or Line[3] > HEIGHT:
        LineD[3] = -LineD[3]


def update(Line,LineD):
    Line[0] += LineD[0]
    Line[1] += LineD[1]
    Line[2] += LineD[2]
    Line[3] += LineD[3]


def updateColor(Color):
    Color[0] = random.randint(0,255)
    Color[1] = random.randint(0, 255)
    Color[2] = random.randint(0, 255)


end = False

while not end:

    # Close window button to end program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                updateColor(Color)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                updateColor(BACKGROUND_COLOR)


    surface.fill(BACKGROUND_COLOR)

    # Rectangle 1
    pygame.draw.line(surface, Color, (Line1[0], Line1[1]), (Line1[2], Line1[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line2[0], Line2[1]), (Line2[2], Line2[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line3[0], Line3[1]), (Line3[2], Line3[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line4[0], Line4[1]), (Line4[2], Line4[3]), THICKNESS)

    # Rectangle 2
    pygame.draw.line(surface, Color, (Line5[0], Line5[1]), (Line5[2], Line5[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line6[0], Line6[1]), (Line6[2], Line6[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line7[0], Line7[1]), (Line7[2], Line7[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line8[0], Line8[1]), (Line8[2], Line8[3]), THICKNESS)

    # Rectangle 3
    pygame.draw.line(surface, Color, (Line9[0], Line9[1]), (Line9[2], Line9[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line10[0], Line10[1]), (Line10[2], Line10[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line11[0], Line11[1]), (Line11[2], Line11[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line12[0], Line12[1]), (Line12[2], Line12[3]), THICKNESS)

    # Rectangle 4
    pygame.draw.line(surface, Color, (Line13[0], Line13[1]), (Line13[2], Line13[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line14[0], Line14[1]), (Line14[2], Line14[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line15[0], Line15[1]), (Line15[2], Line15[3]), THICKNESS)
    pygame.draw.line(surface, Color, (Line16[0], Line16[1]), (Line16[2], Line16[3]), THICKNESS)


    # Rectangle 1
    update(Line1, Line1D)
    update(Line2, Line2D)
    update(Line3, Line3D)
    update(Line4, Line4D)

    # Rectangle 2
    update(Line5, Line5D)
    update(Line6, Line6D)
    update(Line7, Line7D)
    update(Line8, Line8D)

    # Rectangle 3
    update(Line9, Line9D)
    update(Line10, Line10D)
    update(Line11, Line11D)
    update(Line12, Line12D)

    # Rectangle 4
    update(Line13, Line13D)
    update(Line14, Line14D)
    update(Line15, Line15D)
    update(Line16, Line16D)




    # Rectangle 1
    changeDirection(Line1, Line1D)
    changeDirection(Line2, Line2D)
    changeDirection(Line3, Line3D)
    changeDirection(Line4, Line4D)

    # Rectangle 2
    changeDirection(Line5, Line5D)
    changeDirection(Line6, Line6D)
    changeDirection(Line7, Line7D)
    changeDirection(Line8, Line8D)

    # Rectangle 3
    changeDirection(Line9, Line9D)
    changeDirection(Line10, Line10D)
    changeDirection(Line11, Line11D)
    changeDirection(Line12, Line12D)

    # Rectangle 4
    changeDirection(Line13, Line13D)
    changeDirection(Line14, Line14D)
    changeDirection(Line15, Line15D)
    changeDirection(Line16, Line16D)


    clock.tick(60)
    pygame.display.update()
