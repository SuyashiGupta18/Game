
#======== BY USING RANDINT FUNCTION ===========

'''import random

def game_win(user, computer):

    if user == computer:
        return None
    
# Snake vs Water
    if user == "s" and computer == "w":
        return True
    if user == "w" and computer == "s":
        return False
     
# Water vs Gun
    if user == "w" and computer == "g":
        return True
    if user == "g" and computer == "w":
        return False
    
# Gun vs Snake
    if user == "g" and computer == "s":
        return True
    if user == "s" and computer == "g":
        return False
    
rand_no = random.randint(1, 3)


if rand_no == 1:
    computer = "s"
elif rand_no == 2:
    computer = "w"
else:
    computer = "g"

while True:

    user = input("\nYour turn: Snake(s), Water (w), Gun (g): ").lower()

    if user in ["s","w","g"]:
        break
       
    else:
        print("enter valid Input")



print(f"You chose: {user}")

print("\nComputer's turn: Snake(s), Water (w), Gun (g):")
print(f"Computer chose: {computer}")

result = game_win(user, computer)                               


if result is None:
    print("\nIts a draw!")
elif(result):
    print("\nYou win!")
else:
    print("\nYou lose!")'''


#========== BY USING CHOICE FUNCTION ============


'''import random

def game(user, computer):

    #For draw
    if user==computer:
        return "It's draw!"

    # Snake vs Water
    if user == "s" and computer == "w":
        return "you win!"
    if user == "w" and computer == "s":
        return "you lose!"

    # Water vs Gun
    if user == "w" and computer == "g":
        return "you win!"
    if user == "g" and computer == "w":
        return "you lose!"

    # Gun vs Snake
    if user == "g" and computer == "s":
        return "you win!"
    if user == "s" and computer == "g":
        return "you lose!"

        
while True:

    while True:  
    # Take user input first
        user = input("Enter s (snake), w (water), g (gun): ")

        if user in ["s","w","g"]:
           break
        else:
           print("enter valid Input!")

    # Random choice for computer
    choose = ["s", "w", "g"]
    computer = random.choice(choose)

    # Now call function
    result = game(user, computer)

    print("User chose:", user)
    print("Computer chose:", computer)

    print("Result:", result) 

    again= input("Wanna play again? y/n :").lower()

    if again!= "y":
        print("Thank you!")
        break'''


#====================================PYGAME COMMUNITY EDITION===========================================#


import pygame
import pygame.gfxdraw
import random
import math

pygame.init()
pygame.mixer.init()
# ================= SCREEN =================

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Snake Water Gun")

# ================= FONT =================

font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

# ================= COLORS =================

BG = (30, 30, 30)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (200,0,0)

# ================= LOAD IMAGES =================

snake = pygame.image.load("snake_img.jpg")
water = pygame.image.load("water_img.jpg")
gun = pygame.image.load("gun_img.png")

spin_sound = pygame.mixer.Sound("spinning_sound.wav")
win_sound  = pygame.mixer.Sound("win_sound.wav")
lose_sound = pygame.mixer.Sound("lose_sound.wav")
draw_sound = pygame.mixer.Sound("draw_sound.wav")

spin_sound.set_volume(0.7)
win_sound.set_volume(1.0)
lose_sound.set_volume(1.0)
draw_sound.set_volume(1.0)


# Resize (circle size)
SIZE = 190

def make_circle(img, SIZE):
    circle_surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    
    pygame.draw.circle(circle_surface, (255,255,255), (SIZE//2, SIZE//2), SIZE//2)
    
    circle_surface.blit(img, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    
    return circle_surface

snake = pygame.transform.scale(snake, (SIZE, SIZE))
snake = make_circle(snake, SIZE)

water = pygame.transform.scale(water, (SIZE, SIZE))
water = make_circle(water, SIZE)

gun = pygame.transform.scale(gun, (SIZE, SIZE))
gun = make_circle(gun, SIZE)


# ================= BUTTON POSITIONS =================
snake_pos = (250, 350)
water_pos = (450, 350)
gun_pos   = (650, 350)

radius = SIZE // 2

# Play again button
play_again = pygame.Rect(350, 450, 200, 50)

# ================= GAME LOGIC (YOUR SAME) =================
def game(user, computer):

    if user == computer:
        return "DRAW!"

    if user == "s" and computer == "w":
        return "YOU WON!"
    if user == "w" and computer == "s":
        return "YOU LOST!"

    if user == "w" and computer == "g":
        return "YOU WON!"
    if user == "g" and computer == "w":
        return "YOU LOST!"

    if user == "g" and computer == "s":
        return "YOU WON!"
    if user == "s" and computer == "g":
        return "YOU LOST!"

# ================= VARIABLES =================

state = "menu"
user = ""
comp = ""
result = ""

loading_start = 0
angle = 0
final_choice = ""

spin_playing = False
result_sound_played = False
# ================= MAIN LOOP =================
running = True
while running:

    screen.fill(BG)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ================= MENU ========================================
    if state == "menu":

        title = font.render("CHOOSE ONE", True, WHITE)
        screen.blit(title, title.get_rect(center=(450, 100)))

        # Draw images (centered)
        screen.blit(snake, (snake_pos[0]-radius, snake_pos[1]-radius))
        screen.blit(water, (water_pos[0]-radius, water_pos[1]-radius))
        screen.blit(gun, (gun_pos[0]-radius, gun_pos[1]-radius))

        # Draw circle borders

        ''' This gives pixelated border
        # pygame.draw.circle(screen, WHITE, snake_pos, radius, 2)
        # pygame.draw.circle(screen, WHITE, water_pos, radius, 2)
        # pygame.draw.circle(screen, WHITE, gun_pos, radius, 2) '''

        # This will give smooth border
        # First line → thin smooth circle
        # Second line → makes it slightly thicker

        pygame.gfxdraw.aacircle(screen, snake_pos[0], snake_pos[1], radius, WHITE)
        pygame.gfxdraw.aacircle(screen, snake_pos[0], snake_pos[1], radius-1, WHITE)

        pygame.gfxdraw.aacircle(screen, water_pos[0], water_pos[1], radius, WHITE)
        pygame.gfxdraw.aacircle(screen, water_pos[0], water_pos[1], radius-1, WHITE)

        pygame.gfxdraw.aacircle(screen, gun_pos[0], gun_pos[1], radius, WHITE)
        pygame.gfxdraw.aacircle(screen, gun_pos[0], gun_pos[1], radius-1, WHITE)

        # Click detection using distance formula
        def clicked(center):
            dist = math.sqrt((mouse[0]-center[0])**2 + (mouse[1]-center[1])**2)
            return dist <= radius

        if clicked(snake_pos) and click[0]:
            user = "s"
            state = "loading"
            loading_start = pygame.time.get_ticks()
            final_choice = ""

        if clicked(water_pos) and click[0]:
            user = "w"   # 
            state = "loading"
            loading_start = pygame.time.get_ticks()
            final_choice = ""

        if clicked(gun_pos) and click[0]:
            user = "g"
            state = "loading"
            loading_start = pygame.time.get_ticks()
            final_choice = ""
        

    elif state == "loading":

        screen.fill((20, 20, 20))

        #ONLY SPIN IF NOT DECIDED
        if final_choice == "":

            if not spin_playing:
                spin_sound.play(-1)
                spin_playing = True
                
            angle = (angle + 5) % 360

            snake_rot = pygame.transform.rotate(snake, angle)
            water_rot = pygame.transform.rotate(water, angle)
            gun_rot   = pygame.transform.rotate(gun, angle)

            screen.blit(snake_rot, snake_rot.get_rect(center=(250, 350)))
            screen.blit(water_rot, water_rot.get_rect(center=(450, 350)))
            screen.blit(gun_rot, gun_rot.get_rect(center=(650, 350)))

            text = font.render("Computer is choosing...", True, WHITE)
            screen.blit(text, text.get_rect(center=(450, 100)))

        #Decide result after 2 sec
        if pygame.time.get_ticks() - loading_start > 2000 and final_choice == "":
            final_choice = random.choice(["s","w","g"])
            comp = final_choice
            result = game(user, comp)

        #SHOW ONLY FINAL ICON (NO SPINNING)
        
        if final_choice != "":

            #Show text at top

            if spin_playing:
                spin_sound.stop()
                spin_playing = False

            text = font.render("Computer chose:", True, WHITE)
            screen.blit(text,text.get_rect(center=(450, 150))) 

            if final_choice == "s":
                screen.blit(snake, snake.get_rect(center=(450, 300)))
            elif final_choice == "w":
                screen.blit(water, water.get_rect(center=(450, 300)))
            else:
                screen.blit(gun, gun.get_rect(center=(450, 300)))

        if pygame.time.get_ticks() - loading_start > 3000:
            state = "result"

    # ================= RESULT ========================================
    elif state == "result":

        screen.fill((20, 20, 20))

        big_font = pygame.font.Font(None, 90)

        if result == "YOU WON!":
            text = big_font.render("YOU WON!", True, (0, 255, 0))
        elif result == "YOU LOST!":
            text = big_font.render("YOU LOST!", True, (255, 0, 0))
        else:
            text = big_font.render("DRAW", True, (255, 255, 0))

#========================SOUND BLOCK=====================================

        #PLAY RESULT SOUND (ONLY ONCE)
        
        if not result_sound_played:
            spin_sound.stop() 
            print(result)  
            if result == "YOU WON!":
                win_sound.play()
            elif result == "YOU LOST!":
                lose_sound.play()
            else:
                draw_sound.play()

            result_sound_played = True

        # X center = middle of screen (900 / 2 = 450)
        #Y = vertical position
        text_rect = text.get_rect(center=(450, 250)) 
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, RED, play_again)
        btn_text = small_font.render("Play Again", True, WHITE)
        screen.blit(btn_text, btn_text.get_rect(center=play_again.center))

        if play_again.collidepoint(mouse) and click[0]:
            result_sound_played = False
            spin_playing = False
            comp = ""
            final_choice = ""
            state = "menu"
                  

    pygame.display.update()

pygame.quit()