import pygame
import random

# Initialize pygame
pygame.init()

# Screen set up
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define constants
FPS = 30
GRAVITY = 1
JUMP = -10
PIPE_WIDTH = 70
PIPE_GAP = 150

# Load images
bird_img = pygame.Surface((30, 30))
bird_img.fill((255, 255, 0))  # Yellow bird

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def flap(self):
        self.vel = JUMP

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)

    def draw(self, win):
        win.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - (self.height + PIPE_GAP))

    def update(self):
        self.x -= 5
        self.top.topleft = (self.x, 0)
        self.bottom.topleft = (self.x, self.height + PIPE_GAP)

    def draw(self, win):
        pygame.draw.rect(win, GREEN, self.top)
        pygame.draw.rect(win, GREEN, self.bottom)

# Game Over Screen
def game_over(win, score):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    # Render the "Game Over" text and the score
    game_over_text = font_big.render("Game Over", True, BLACK)
    score_text = font_big.render(f"Score: {score}", True, BLACK)
    restart_text = font_small.render("Press any key to restart", True, BLACK)

    win.fill(WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()
    wait_for_restart()

# Wait for any key press to restart
def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                main()  # Restart the game by calling main()

# Main game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font = pygame.font.SysFont(None, 36)

    run = True
    while run:
        clock.tick(FPS)

        # เรียงลำดับเหตุการณ์
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        # อัพเดทนก
        bird.update()

        # อัพเดทท่อ
        if pipes[-1].x < WIDTH // 2:
            pipes.append(Pipe())

        for pipe in pipes[:]:
            pipe.update()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                score += 1

        # การชน
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                game_over(win, score)
                run = False

        if bird.y > HEIGHT or bird.y < 0:
            game_over(win, score)
            run = False

        # Draw everything
        win.fill(WHITE)
        bird.draw(win)
        for pipe in pipes:
            pipe.draw(win)
        score_text = font.render(f"Score: {score}", True, BLACK)
        win.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
