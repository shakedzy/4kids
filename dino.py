import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino Game")

# Clock to control frame rate
CLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.6
game_speed = 5

# Dinosaur class
class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 100
        self.width = 44
        self.height = 47
        self.jump_vel = 0
        self.is_jumping = False
        self.is_ducking = False
        self.duck_height = 25
        self.run_img = self.get_run_img()
        self.duck_img = self.get_duck_img()
        self.current_img = self.run_img

    def get_run_img(self):
        # Draw the running dinosaur (simplified)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, BLACK, (0, 0, self.width, self.height))
        pygame.draw.circle(surface, WHITE, (int(self.width * 0.75), int(self.height * 0.25)), 5)
        return surface

    def get_duck_img(self):
        # Draw the ducking dinosaur (simplified)
        surface = pygame.Surface((self.width, self.duck_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, BLACK, (0, 0, self.width, self.duck_height))
        pygame.draw.circle(surface, WHITE, (int(self.width * 0.75), int(self.duck_height * 0.5)), 5)
        return surface

    def update(self, user_input):
        if self.is_jumping:
            self.jump()
        elif self.is_ducking:
            self.duck()
        else:
            self.run()

        if user_input[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.jump_vel = -12
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
        else:
            self.is_ducking = False

    def jump(self):
        self.y += self.jump_vel
        self.jump_vel += gravity
        if self.y >= HEIGHT - 100:
            self.y = HEIGHT - 100
            self.is_jumping = False

    def duck(self):
        self.current_img = self.duck_img
        self.height = self.duck_height

    def run(self):
        self.current_img = self.run_img
        self.height = 47

    def draw(self, screen):
        screen.blit(self.current_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Obstacle classes
class Cactus:
    def __init__(self, image, y_pos):
        self.x = WIDTH + random.randint(0, 500)
        self.y = y_pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.x -= game_speed
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class SmallCactus(Cactus):
    def __init__(self):
        self.image = self.get_image()
        super().__init__(self.image, HEIGHT - 75)

    def get_image(self):
        # Draw small cactus (simplified)
        surface = pygame.Surface((25, 50), pygame.SRCALPHA)
        pygame.draw.rect(surface, BLACK, (10, 0, 5, 50))
        pygame.draw.rect(surface, BLACK, (0, 20, 25, 5))
        return surface

class LargeCactus(Cactus):
    def __init__(self):
        self.image = self.get_image()
        super().__init__(self.image, HEIGHT - 100)

    def get_image(self):
        # Draw large cactus (simplified)
        surface = pygame.Surface((35, 70), pygame.SRCALPHA)
        pygame.draw.rect(surface, BLACK, (15, 0, 5, 70))
        pygame.draw.rect(surface, BLACK, (0, 30, 35, 5))
        return surface

# Function to generate random obstacles
def generate_obstacle():
    obstacle_type = random.choice(['small_cactus', 'large_cactus'])
    if obstacle_type == 'small_cactus':
        return SmallCactus()
    else:
        return LargeCactus()

# Main Function
def main():
    global game_speed
    run = True
    player = Dino()
    obstacles = []
    death_count = 0
    score = 0

    # Font for score
    font = pygame.font.SysFont(None, 30)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill(WHITE)

        user_input = pygame.key.get_pressed()

        player.update(user_input)
        player.draw(SCREEN)

        if len(obstacles) == 0:
            obstacles.append(generate_obstacle())

        for obstacle in list(obstacles):
            obstacle.update()
            obstacle.draw(SCREEN)
            if obstacle.rect.colliderect(player.get_rect()):
                pygame.time.delay(500)
                death_count += 1
                main()

            if obstacle.x < -obstacle.rect.width:
                obstacles.remove(obstacle)
                score += 1
                # Increase game speed every time an obstacle is successfully passed
                game_speed += 0.5

        # Draw ground
        pygame.draw.line(SCREEN, BLACK, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 2)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (WIDTH - 150, 20))

        pygame.display.update()
        CLOCK.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()