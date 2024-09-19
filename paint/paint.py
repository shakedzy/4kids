import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Paint for Kids")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Set up the drawing surface
drawing_surface = pygame.Surface((width, height - 60))
drawing_surface.fill(WHITE)

# Drawing properties
current_color = BLACK
brush_size = 5
drawing = False
fill_mode = False

# Shapes
FREEHAND = "freehand"
CIRCLE = "circle"
SQUARE = "square"
TRIANGLE = "triangle"
current_shape = FREEHAND

# Button dimensions
button_size = 40
color_buttons = [
    (RED, (10, height - 50)),
    (GREEN, (55, height - 50)),
    (BLUE, (100, height - 50)),
    (YELLOW, (145, height - 50)),
    (PURPLE, (190, height - 50)),
    (ORANGE, (235, height - 50)),
    (PINK, (280, height - 50)),
    (BLACK, (325, height - 50))
]

# Shape buttons
shape_buttons = [
    (FREEHAND, (370, height - 50)),
    (CIRCLE, (415, height - 50)),
    (SQUARE, (460, height - 50)),
    (TRIANGLE, (505, height - 50))
]

# Utility buttons
fill_button = pygame.Rect(550, height - 50, button_size, button_size)
clear_button = pygame.Rect(595, height - 50, button_size, button_size)
undo_button = pygame.Rect(640, height - 50, button_size, button_size)

# Undo history
history = []

def draw_buttons():
    for color, pos in color_buttons:
        pygame.draw.rect(screen, color, (pos[0], pos[1], button_size, button_size))
    
    for shape, pos in shape_buttons:
        pygame.draw.rect(screen, WHITE, (pos[0], pos[1], button_size, button_size))
        if shape == FREEHAND:
            pygame.draw.line(screen, BLACK, (pos[0]+10, pos[1]+20), (pos[0]+30, pos[1]+20), 2)
        elif shape == CIRCLE:
            pygame.draw.circle(screen, BLACK, (pos[0]+20, pos[1]+20), 15, 2)
        elif shape == SQUARE:
            pygame.draw.rect(screen, BLACK, (pos[0]+10, pos[1]+10, 20, 20), 2)
        elif shape == TRIANGLE:
            pygame.draw.polygon(screen, BLACK, [(pos[0]+20, pos[1]+10), (pos[0]+10, pos[1]+30), (pos[0]+30, pos[1]+30)], 2)
    
    # Fill button
    pygame.draw.rect(screen, WHITE if not fill_mode else (200, 200, 200), fill_button)
    pygame.draw.polygon(screen, BLACK, [(fill_button.x+10, fill_button.y+30), (fill_button.x+30, fill_button.y+30), (fill_button.x+20, fill_button.y+10)])
    pygame.draw.rect(screen, BLACK, (fill_button.x+15, fill_button.y+25, 10, 5))

    # Clear button (bin icon)
    pygame.draw.rect(screen, WHITE, clear_button)
    pygame.draw.rect(screen, BLACK, (clear_button.x+10, clear_button.y+15, 20, 20), 2)
    pygame.draw.rect(screen, BLACK, (clear_button.x+7, clear_button.y+10, 26, 5))
    pygame.draw.line(screen, BLACK, (clear_button.x+15, clear_button.y+20), (clear_button.x+15, clear_button.y+30), 2)
    pygame.draw.line(screen, BLACK, (clear_button.x+20, clear_button.y+20), (clear_button.x+20, clear_button.y+30), 2)
    pygame.draw.line(screen, BLACK, (clear_button.x+25, clear_button.y+20), (clear_button.x+25, clear_button.y+30), 2)

    # Undo button (simple left-pointing arrow)
    pygame.draw.rect(screen, WHITE, undo_button)
    pygame.draw.polygon(screen, BLACK, [
        (undo_button.x + 30, undo_button.y + 10),  # Top point
        (undo_button.x + 30, undo_button.y + 30),  # Bottom point
        (undo_button.x + 10, undo_button.y + 20)   # Left point
    ])

def handle_drawing(start, end):
    global drawing_surface
    if current_shape == FREEHAND:
        pygame.draw.line(drawing_surface, current_color, start, end, brush_size * 2)
    elif current_shape == CIRCLE:
        radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
        pygame.draw.circle(screen, current_color, start, radius, 0 if fill_mode else 2)
    elif current_shape == SQUARE:
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), 
                           abs(end[0] - start[0]), abs(end[1] - start[1]))
        pygame.draw.rect(screen, current_color, rect, 0 if fill_mode else 2)
    elif current_shape == TRIANGLE:
        mid_x = (start[0] + end[0]) // 2
        pygame.draw.polygon(screen, current_color, [(start[0], end[1]), (mid_x, start[1]), (end[0], end[1])], 0 if fill_mode else 2)

def finalize_shape(start, end):
    global drawing_surface
    if current_shape == CIRCLE:
        radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
        pygame.draw.circle(drawing_surface, current_color, start, radius, 0 if fill_mode else 2)
    elif current_shape == SQUARE:
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), 
                           abs(end[0] - start[0]), abs(end[1] - start[1]))
        pygame.draw.rect(drawing_surface, current_color, rect, 0 if fill_mode else 2)
    elif current_shape == TRIANGLE:
        mid_x = (start[0] + end[0]) // 2
        pygame.draw.polygon(drawing_surface, current_color, [(start[0], end[1]), (mid_x, start[1]), (end[0], end[1])], 0 if fill_mode else 2)

# Main game loop
start_pos = None
last_pos = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < height - 60:  # Above the button area
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
                history.append(drawing_surface.copy())
            else:
                for color, pos in color_buttons:
                    if pygame.Rect(pos[0], pos[1], button_size, button_size).collidepoint(event.pos):
                        current_color = color
                for shape, pos in shape_buttons:
                    if pygame.Rect(pos[0], pos[1], button_size, button_size).collidepoint(event.pos):
                        current_shape = shape
                if fill_button.collidepoint(event.pos):
                    fill_mode = not fill_mode
                if clear_button.collidepoint(event.pos):
                    history.append(drawing_surface.copy())
                    drawing_surface.fill(WHITE)
                if undo_button.collidepoint(event.pos) and history:
                    drawing_surface = history.pop()
        
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if current_shape in [CIRCLE, SQUARE, TRIANGLE]:
                    finalize_shape(start_pos, event.pos)
                drawing = False
        
        if event.type == pygame.MOUSEMOTION:
            if drawing and event.pos[1] < height - 60:
                if current_shape == FREEHAND:
                    handle_drawing(last_pos, event.pos)
                last_pos = event.pos

    # Draw everything
    screen.fill(WHITE)
    screen.blit(drawing_surface, (0, 0))
    if drawing and current_shape in [CIRCLE, SQUARE, TRIANGLE]:
        handle_drawing(start_pos, last_pos)
    draw_buttons()
    pygame.display.flip()

pygame.quit()