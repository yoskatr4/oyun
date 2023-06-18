import pygame
import math

# Ekran boyutları
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600

# Renkler
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Pygame başlatılıyor
pygame.init()

# Ekran oluşturuluyor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kareler")

font = pygame.font.Font(None, 36)

# Kare boyutları ve başlangıç pozisyonları
square_size = 50
red_x = SCREEN_WIDTH // 4 - square_size // 2
red_y = SCREEN_HEIGHT // 2 - square_size // 2
blue_x = 3 * SCREEN_WIDTH // 4 - square_size // 2
blue_y = SCREEN_HEIGHT // 2 - square_size // 2

# Hızlar
blue_speed_easy = 4
blue_speed_hard = 50

# Oyun durumu
game_started = False
game_over = False
difficulty_chosen = False

# Skor
score = 0
score_increase = 1.7  # Skor artış hızı

score_timer = 0
score_delay = 0.75  # Skor artış gecikmesi (saniye)

scoreh = 0
score_increaseh = 1.7  # Skor artış hızı

score_timerh = 0
score_delayh = 0.75  # Skor artış gecikmesi (saniye)


# Pygame için saat objesi oluşturuluyor
clock = pygame.time.Clock()

# FPS göstergesi için font ve renk ayarları
fps_font = pygame.font.Font(None, 24)
fps_color = WHITE

def show_difficulty_options():
    easy_text = font.render("Kolay Mod", True, WHITE)
    easy_text_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(easy_text, easy_text_rect)

    hard_text = font.render("Zor Mod", True, WHITE)
    hard_text_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(hard_text, hard_text_rect)

    return easy_text_rect, hard_text_rect

def show_menu():
    menu_text = font.render("Ana Menü", True, WHITE)
    menu_text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(menu_text, menu_text_rect)

    restart_text = font.render("Yeniden Başla", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(restart_text, restart_text_rect)

    return menu_text_rect, restart_text_rect

def show_game_over_menu():
    game_over_text = font.render("Oyun Bitti!", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(game_over_text, game_over_text_rect)

    menu_text1 = font.render("Ana Menü", True, WHITE)
    menu_text_rect1 = menu_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(menu_text1, menu_text_rect1)

    restart_text = font.render("Yeniden Başla", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
    screen.blit(restart_text, restart_text_rect)

    score_text = font.render("Toplam Skor: " + str(int(score)), True, WHITE)
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(score_text, score_text_rect)

    return menu_text_rect1, restart_text_rect

def reset_game():
    global red_x, red_y, blue_x, blue_y, game_started, game_over, difficulty_chosen
    red_x = SCREEN_WIDTH // 4 - square_size // 2
    red_y = SCREEN_HEIGHT // 2 - square_size // 2
    blue_x = 3 * SCREEN_WIDTH // 4 - square_size // 2
    blue_y = SCREEN_HEIGHT // 2 - square_size // 2
    game_started = False
    game_over = False
    difficulty_chosen = False

# Oyun döngüsü
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Geçen süreyi saniyeye çevir

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started and not difficulty_chosen:
                if easy_text_rect.collidepoint(event.pos):
                    blue_speed = blue_speed_easy
                    difficulty_chosen = True
                    game_started = True
                elif hard_text_rect.collidepoint(event.pos):
                    blue_speed = blue_speed_hard
                    difficulty_chosen = True
                    game_started = True
            elif game_over:
                if menu_text_rect.collidepoint(event.pos):
                    reset_game()
                elif restart_text_rect.collidepoint(event.pos):
                    reset_game()
                    game_started = True

    if game_started and not game_over:
        # Klavye girdilerini kontrol etmek için
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            red_y -= 5
        if keys[pygame.K_s]:
            red_y += 5
        if keys[pygame.K_a]:
            red_x -= 5
        if keys[pygame.K_d]:
            red_x += 5

        # Mavi karenin kırmızı kareye doğru hareket etmesi
        angle = math.atan2(red_y - blue_y, red_x - blue_x)
        blue_x += blue_speed * math.cos(angle)
        blue_y += blue_speed * math.sin(angle)

        # Kırmızı karenin mavi kareye veya pencerenin kenarlarına temas ettiğini kontrol et
        if (
            math.sqrt((red_x - blue_x) ** 2 + (red_y - blue_y) ** 2) < (square_size + square_size) / 2
            or red_x < square_size // 2
            or red_x > SCREEN_WIDTH - square_size // 2
            or red_y < square_size // 2
            or red_y > SCREEN_HEIGHT - square_size // 2
        ):
            game_over = True

    # Ekranı temizle
    screen.fill((0, 0, 0))

    if not game_started:
        if not difficulty_chosen:
            easy_text_rect, hard_text_rect = show_difficulty_options()
        else:
            menu_text_rect, restart_text_rect = show_menu()
    elif game_over:
        menu_text_rect, restart_text_rect = show_game_over_menu()
    else:
        # Kareleri çiz
        pygame.draw.rect(screen, RED, pygame.Rect(red_x, red_y, square_size, square_size))
        pygame.draw.rect(screen, BLUE, pygame.Rect(blue_x, blue_y, square_size, square_size))
        # Skoru güncelle
        score_timer += dt
        if score_timer >= score_delay:
                score += score_increase
                score_timer = 0

        # Skoru ekrana yazdır
        score_text = font.render("Toplam Skor: " + str(int(score)), True, WHITE)
        screen.blit(score_text, (10, 10))

        # FPS göstergesini güncelle
        fps = clock.get_fps()
        fps_text = fps_font.render("FPS: {:.2f}".format(fps), True, fps_color)
        screen.blit(fps_text, (SCREEN_WIDTH - 80, 10))


    # Ekranı güncelle
    pygame.display.flip()

# Pygame'i kapat
pygame.quit()
