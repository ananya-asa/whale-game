import pygame
import random

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shark Swim")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
POPUP_COLORS = [(255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 165, 0)]
RED = (255, 50, 50)

def load_image(filename, size=None, use_alpha=False):
    try:
        image = pygame.image.load(filename)
        if size:
            image = pygame.transform.scale(image, size)
        return image.convert_alpha() if use_alpha else image.convert()
    except pygame.error as e:
        print(f"Unable to load image: {filename}. Error: {e}")
        if size:
            placeholder = pygame.Surface(size, pygame.SRCALPHA)
            placeholder.fill((255, 0, 255))
            return placeholder
        return None

bg_image = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = load_image("shark.png", (120, 80), use_alpha=True)
fish_img = load_image("fish.png", (45, 30), use_alpha=True)
barrier_img = load_image("ice.png", use_alpha=True)
bg_x = 0

try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    crash_sound = pygame.mixer.Sound("crash.mp3")
    pygame.mixer.music.load("music.mp3")
except pygame.error as e:
    print(f"Could not load sound file. Game running without sound. Error: {e}")
    eat_sound, crash_sound = None, None

TITLE_FONT = pygame.font.Font(None, 100)
POPUP_FONT = pygame.font.Font(None, 60)
SCORE_FONT = pygame.font.Font(None, 48)
GAMEOVER_FONT = pygame.font.Font(None, 75)
RESTART_FONT = pygame.font.Font(None, 48)

EAT_TEXTS = ["Crunchy!", "Awesome!", "Tasty!", "Yum!", "Gulp!", "Sweet!", "Nice!"]
CRASH_TEXT = "Wiped Out!"

score = 0
game_over = False
game_started = False

def draw_text_with_outline(text, font, text_color, center_pos):
    text_surf = font.render(text, True, text_color)
    outline_surf = font.render(text, True, BLACK)
    for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
        screen.blit(outline_surf, (center_pos[0] - text_surf.get_width()//2 + dx, center_pos[1] - text_surf.get_height()//2 + dy))
    screen.blit(text_surf, (center_pos[0] - text_surf.get_width()//2, center_pos[1] - text_surf.get_height()//2))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, font):
        super().__init__()
        self.lifespan = 60
        self.initial_lifespan = self.lifespan
        self.y_velocity = -2
        text_surf = font.render(text, True, color)
        outline_surf = font.render(text, True, BLACK)
        self.image = pygame.Surface((text_surf.get_width() + 4, text_surf.get_height() + 4), pygame.SRCALPHA)
        for pos in [(0,0),(4,0),(0,4),(4,4)]:
            self.image.blit(outline_surf, pos)
        self.image.blit(text_surf, (2, 2))
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        self.rect.y += self.y_velocity
        self.lifespan -= 1
        alpha = max(0, 255 * (self.lifespan / self.initial_lifespan))
        self.image.set_alpha(alpha)
        if self.lifespan <= 0:
            self.kill()

class Shark(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT
    def reset(self):
        self.rect.center = (100, SCREEN_HEIGHT // 2)

class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fish_img
        self.rect = self.image.get_rect(midleft=(SCREEN_WIDTH, random.randint(50, SCREEN_HEIGHT - 50)))
        self.speed = random.randint(3, 6)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Barrier(pygame.sprite.Sprite):
    def __init__(self, top_or_bottom, height):
        super().__init__()
        scaled_image = pygame.transform.scale(barrier_img, (80, height))
        self.image = scaled_image if top_or_bottom == 'top' else pygame.transform.flip(scaled_image, False, True)
        if top_or_bottom == 'top':
            self.rect = self.image.get_rect(topright=(SCREEN_WIDTH, 0))
        else:
            self.rect = self.image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

def reset_game():
    global score, game_over, gap_index
    score, game_over, gap_index = 0, False, 0
    all_sprites.empty()
    fish_group.empty()
    barrier_group.empty()
    text_group.empty()
    all_sprites.add(shark)
    shark.reset()
    pygame.mixer.music.play(-1)

all_sprites = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()

shark = Shark()
all_sprites.add(shark)

ADD_FISH = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_FISH, 1500)
ADD_BARRIER = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_BARRIER, 2800)
gap_sizes = [140, 160, 180, 120, 130]
gap_index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
                pygame.mixer.music.play(-1)

        elif game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

        else:
            if event.type == ADD_FISH:
                new_fish = Fish()
                all_sprites.add(new_fish)
                fish_group.add(new_fish)

            if event.type == ADD_BARRIER:
                gap_y = random.randint(20, SCREEN_HEIGHT - 20 - gap_sizes[gap_index])
                top_h = gap_y
                bot_h = SCREEN_HEIGHT - (gap_y + gap_sizes[gap_index])
                if top_h > 0:
                    top_b = Barrier('top', top_h)
                    all_sprites.add(top_b)
                    barrier_group.add(top_b)
                if bot_h > 0:
                    bot_b = Barrier('bottom', bot_h)
                    all_sprites.add(bot_b)
                    barrier_group.add(bot_b)
                gap_index = (gap_index + 1) % len(gap_sizes)

    if game_started and not game_over:
        all_sprites.update()
        text_group.update()

        eaten_fish = pygame.sprite.spritecollide(shark, fish_group, True, pygame.sprite.collide_mask)
        if eaten_fish:
            score += len(eaten_fish)
            if eat_sound: eat_sound.play()
            pop_text = FloatingText(shark.rect.centerx, shark.rect.top, random.choice(EAT_TEXTS), random.choice(POPUP_COLORS), POPUP_FONT)
            all_sprites.add(pop_text)
            text_group.add(pop_text)

        if pygame.sprite.spritecollide(shark, barrier_group, False, pygame.sprite.collide_mask):
            game_over = True
            pygame.mixer.music.stop()
            if crash_sound: crash_sound.play()
            pop_text = FloatingText(shark.rect.centerx, shark.rect.centery, CRASH_TEXT, RED, GAMEOVER_FONT)
            all_sprites.add(pop_text)
            text_group.add(pop_text)

    bg_x -= 1
    if bg_x < -SCREEN_WIDTH:
        bg_x = 0
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + SCREEN_WIDTH, 0))

    if not game_started:
        draw_text_with_outline("Shark Swim", TITLE_FONT, (0, 150, 255), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        if pygame.time.get_ticks() // 500 % 2 == 0:
            draw_text_with_outline("Press Space to Start", RESTART_FONT, WHITE, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    else:
        all_sprites.draw(screen)
        draw_text(f"Score: {score}", SCORE_FONT, WHITE, SCREEN_WIDTH - 100, 30)
        if game_over:
            draw_text("Game Over", GAMEOVER_FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
            draw_text(f"Final Score: {score}", SCORE_FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)
            draw_text("Press 'R' to Restart", RESTART_FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
