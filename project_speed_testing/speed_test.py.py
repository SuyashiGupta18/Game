import pygame
import time
import random

pygame.init()
pygame.mixer.init()
pygame.key.set_repeat(400, 40)
# ================= SCREEN =================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Speed Tester")

# ================= FONT =================
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 32)

# ================= BACKGROUND MUSIC =================
pygame.mixer.music.load("instrumental_melody.mp3")   # your file name
pygame.mixer.music.set_volume(0.5)      
pygame.mixer.music.play(-1)                          # -1 = infinite loop

# ================= COLORS =================
BG = (20, 20, 30)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)
BLUE = (100, 200, 255)
GRAY = (180, 180, 180)
BOX = (40, 40, 60)

# ================= SENTENCES =================
sentences = [
    "I don't chase I attract.",
    "A journey of a thousand miles begins with a single step.",
    "I will be the first millionaire of my whole bloodline.",
    "My name will be spoken among the most successful personalities."
]

# ================= STATES =================
state = "welcome"

user_text = ""
test_sentence = ""
start_time = 0
result = ""

# ================= BUTTON =================
button_rect = pygame.Rect(WIDTH//2 - 125, HEIGHT//2 - 35, 250, 70)

# ================= INPUT BOX =================
input_box = pygame.Rect(100, 300, 700, 60)

# ================= PARTICLES (ALPHABETS) =================
class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.size = random.randint(20, 35)
        self.font = pygame.font.Font(None, self.size)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def draw(self, screen):
        text = self.font.render(self.letter, True, (150, 200, 255))
        screen.blit(text, (self.x, self.y))

particles = [Particle() for _ in range(80)]

# ================= CURSOR =================
cursor_visible = True
cursor_timer = 0

# ================= ACCURACY =================
def measure_accuracy(user_input, test_sentence):
    correct_chars = sum(1 for a, b in zip(user_input, test_sentence) if a == b)
    return (correct_chars / len(test_sentence)) * 100 if test_sentence else 0

# ================= TEXT WRAP FUNCTION =================
def draw_text_wrapped(text, x, y, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if small_font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    for i, line in enumerate(lines):
        surface = small_font.render(line, True, WHITE)
        screen.blit(surface, (x, y + i * 30))

# ================= LOOP =================
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    screen.fill(BG)

    # ===== BACKGROUND ANIMATION =====
    for p in particles:
        p.move()
        p.draw(screen)

    # Cursor blinking
    cursor_timer += dt
    if cursor_timer > 500:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===== MOUSE =====
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):

                if state == "welcome":
                    state = "typing"
                    test_sentence = random.choice(sentences)
                    user_text = ""
                    start_time = time.time()

                elif state == "result":
                    state = "welcome"

        # ===== KEYBOARD =====
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                if state == "welcome":
                    state = "typing"
                    test_sentence = random.choice(sentences)
                    user_text = ""
                    start_time = time.time()

                elif state == "typing":
                    end_time = time.time()
                    time_taken = end_time - start_time
                    word_count = len(test_sentence.split())

                    wps = (word_count / (time_taken/60))
                    accuracy = measure_accuracy(user_text, test_sentence)

                    result = f"WPM: {wps:.2f} | Accuracy: {accuracy:.2f}%"
                    state = "result"

                elif state == "result":
                    state = "welcome"

            elif state == "typing":
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    # ================= DRAW UI =================

    # -------- WELCOME --------
    if state == "welcome":
        title = font.render("Typing Speed Tester", True, WHITE)
        subtitle = small_font.render("Test your speed and accuracy here.", True, GRAY)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 200))

        color = LIGHT_GREEN if button_rect.collidepoint(mouse_pos) else GREEN
        pygame.draw.rect(screen, color, button_rect, border_radius=12)

        button_text = small_font.render("Start Test", True, WHITE)
        screen.blit(button_text, (
            button_rect.centerx - button_text.get_width()//2,
            button_rect.centery - button_text.get_height()//2
        ))

    # -------- TYPING --------
    elif state == "typing":

        # Sentence (wrapped)
        draw_text_wrapped(test_sentence, 100, 150, 700)

        # Input box
        pygame.draw.rect(screen, BOX, input_box, border_radius=10)
        pygame.draw.rect(screen, BLUE, input_box, 2, border_radius=10)

        user_surface = small_font.render(user_text, True, WHITE)

        # SCROLL LOGIC
        if user_surface.get_width() > input_box.width - 20:
            offset = user_surface.get_width() - (input_box.width - 20)
        else:
            offset = 0

        clip_rect = pygame.Rect(offset, 0, input_box.width - 20, input_box.height)
        screen.blit(user_surface, (input_box.x + 10, input_box.y + 15), clip_rect)

        # Cursor
        cursor_x = input_box.x + 10 + user_surface.get_width() - offset
        if cursor_visible:
            pygame.draw.line(screen, WHITE,
                             (cursor_x, input_box.y + 10),
                             (cursor_x, input_box.y + 50), 2)

        hint = small_font.render("Press 'ENTER' to finish.", True, GRAY)
        screen.blit(hint, (100, 400))

    # -------- RESULT --------
    elif state == "result":
        result_text = font.render(result, True, WHITE)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 180))

        color = LIGHT_GREEN if button_rect.collidepoint(mouse_pos) else GREEN
        pygame.draw.rect(screen, color, button_rect, border_radius=12)

        retry_text = small_font.render("Retry", True, WHITE)
        screen.blit(retry_text, (
            button_rect.centerx - retry_text.get_width()//2,
            button_rect.centery - retry_text.get_height()//2
        ))

    pygame.display.update()

pygame.quit()