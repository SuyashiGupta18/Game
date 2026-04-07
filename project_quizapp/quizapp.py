import pygame
import time
import random
import math

pygame.init()
pygame.mixer.init()

# ================= SCREEN =================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Song Quiz Challenge")

# ================= FONT =================
title_font = pygame.font.Font(None, 70)
font = pygame.font.Font(None, 45)
small_font = pygame.font.Font(None, 32)

# ================= COLORS =================
BG = (20, 20, 30)  
CARD = (40, 40, 60)
OPTION = (200, 150, 255)
OPTION_HOVER = (220, 170, 255)
CORRECT = (0, 200, 120)
WRONG = (220, 80, 80)
WHITE = (255, 255, 255)
BLUE = (80, 150, 255)
BLUE_HOVER = (120, 180, 255)

# ================= QUIZ DATA =================
quiz = [
    { "question": "Who sang 'Shape of You'?",
      "options": ["Justin Bieber", "Ed Sheeran", "Shawn Mendes", "Charlie Puth"],
      "answer": "Ed Sheeran",
      "song": "shape_of_you.mp3" },

    { "question": "Who sang 'Hass Hass'?",
      "options": ["Diljit Dosanjh", "Badshah", "Yo Yo Honey Singh", "AP Dhillon"],
      "answer": "Diljit Dosanjh",
      "song": "hass_hass.mp3" },

    { "question": "Who sang 'Senorita'?",
      "options": ["Dua Lipa", "Shawn Mendes and Camila Cabello", "Katy Perry", "Selena Gomez and Miley Cyrus"],
      "answer": "Shawn Mendes and Camila Cabello",
      "song": "senorita.mp3" },

    { "question": "Who sang 'Brown Munde'?",
      "options": ["Yo Yo honey singh", "Karan Aujla", "AP Dhillon", "Badshah"],
      "answer": "Yo Yo honey singh",
      "song": "brown_munde.mp3" },

    { "question": "Who sang 'Tu Aake Dekhle'?",
      "options": ["Arijit Singh", "Badshah", "King", "Jubin Nautiyal"],
      "answer": "King",
      "song": "tu_aake_dekhle.mp3" },
    
    { "question": "Who sang 'Malang'?",
      "options": ["Siddharth Mahadevan", "Sukhwinder Singh", "Kailash Kher", "Mohit Chauhan"],
      "answer": "Siddharth Mahadevan",
      "song": "malang.mp3" },

    { "question": "Who sang 'Heat Waves'?",
      "options": ["Imagine Dragons", "Glass Animals", "Coldplay", "Maroon 5"],
      "answer": "Glass Animals",
      "song": "heat_waves.mp3" },

    { "question": "Who sang 'Deva Deva'?",
      "options": ["Arijit Singh", "Armaan Malik", "Jubin Nautiyal", "Sonu Nigam"],
      "answer": "Arijit Singh",
      "song": "om_deva_deva.mp3" },

    { "question": "Who sang 'Sitare'?",
      "options": ["Badshah", "Arijit Singh", "Divine", "Emiway Bantai"],
      "answer": "Arijit Singh",
      "song": "sitaare_sitaare.mp3" },
      
    { "question": "Who sang 'Na ja'?",
      "options": ["Pav Dharia", "Karan Aujla", "Armaan Malik", "Badshah"],
      "answer": "Pav Dharia",
      "song": "na_ja.mp3" }
]

# ================= PARTICLES =================
class MusicParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 1.2)
        self.symbol = random.choice(["♪", "♫"])
        self.size = random.randint(20, 35)
        self.offset = random.uniform(0, 100)
    def move(self):
        self.y += self.speed
        self.x += math.sin(self.y * 0.05 + self.offset)
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    def draw(self, screen, state):
        font = pygame.font.SysFont("timesnewroman", self.size)
        color = (150, 200, 255) if state != "welcome" else random.choice([(255,100,200),(180,100,255)])
        text = font.render(self.symbol, True, color)
        screen.blit(text, (self.x, self.y))

particles = [MusicParticle() for _ in range(25)]

# ================= VARIABLES =================
state = "welcome"
current_q = 0
feedback = ""
selected_option = None
play_song = False
song_start_time = 0
show_next = False
score = 0
clock = pygame.time.Clock()
running = True

# ================= MAIN LOOP =================
while running:
    screen.fill(BG)
    mouse_pos = pygame.mouse.get_pos()

    for p in particles:
        p.move()
        p.draw(screen, state)

    # ===== WELCOME =====
    if state == "welcome":
        title = title_font.render("Song Quiz Challenge", True, (220,140,200))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        start_rect = pygame.Rect(WIDTH//2 - 100, 300, 200, 60)
        color = BLUE_HOVER if start_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, color, start_rect, border_radius=12)
        screen.blit(font.render("Start", True, WHITE), (start_rect.centerx-40, start_rect.centery-15))

    # ===== QUIZ =====
    elif state == "quiz":
        question = quiz[current_q]
        screen.blit(small_font.render(f"Question {current_q+1}/{len(quiz)}", True, WHITE), (50,30))
        pygame.draw.rect(screen, CARD, (80,80,740,100), border_radius=12)
        screen.blit(font.render(question["question"], True, WHITE), (100,110))

        option_rects = []
        for i, option in enumerate(question["options"]):
            rect = pygame.Rect(150, 220 + i*70, 600, 55)
            option_rects.append((rect, option))
            if selected_option == option:
                color = CORRECT if option == question["answer"] else WRONG
            else:
                color = OPTION_HOVER if rect.collidepoint(mouse_pos) else OPTION
            pygame.draw.rect(screen, color, rect, border_radius=12)
            screen.blit(small_font.render(option, True, WHITE), (rect.x+15, rect.y+12))

        # Feedback
        fb_color = (0,200,120) if "Correct" in feedback else (255,80,80)
        screen.blit(small_font.render(feedback, True, fb_color), (WIDTH//2 - 100, 500))

        # Next button
        next_rect = pygame.Rect(350, 540, 200, 45)
        if show_next:
            pygame.draw.rect(screen, (0,200,120), next_rect, border_radius=10)
            screen.blit(small_font.render("Next", True, WHITE), (next_rect.centerx-30,next_rect.centery-10))

    # ===== SCORE SCREEN =====
    
    elif state == "score":
        title = title_font.render("Quiz Completed!", True, (220,140,200))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        score_text = font.render(f"Your Score: {score} / {len(quiz)}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 300))

        restart_rect = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
        color = BLUE_HOVER if restart_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, color, restart_rect, border_radius=12)

        # Center the text inside the button
        restart_text = font.render("Restart", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        screen.blit(restart_text, restart_text_rect)

    # ===== EVENTS =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "welcome" and start_rect.collidepoint(event.pos):
                state = "quiz"
            elif state == "quiz":
                for rect, option in option_rects:
                    if rect.collidepoint(event.pos) and not play_song:
                        selected_option = option
                        if option == question["answer"]:
                            feedback = "Correct! Playing song..."
                            pygame.mixer.music.load(question["song"])
                            pygame.mixer.music.play()
                            play_song = True
                            song_start_time = time.time()
                            show_next = True
                            score += 1
                        else:
                            feedback = "Wrong!"
                            show_next = True
                if show_next and next_rect.collidepoint(event.pos):
                    current_q += 1
                    if current_q >= len(quiz):
                        state = "score"
                    feedback = ""
                    selected_option = None
                    show_next = False
                    pygame.mixer.music.stop()
                    play_song = False
            elif state == "score" and restart_rect.collidepoint(event.pos):
                state = "welcome"
                current_q = 0
                score = 0
                feedback = ""
                selected_option = None
                show_next = False

    # ===== AUTO NEXT AFTER 30 SEC =====
    if play_song and time.time() - song_start_time > 30:
        pygame.mixer.music.stop()
        play_song = False
        current_q += 1
        if current_q >= len(quiz):
            state = "score"
        feedback = ""
        selected_option = None
        show_next = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()