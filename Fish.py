#Testing
#0.05
import pygame

import time
import random
import sys
pygame.init(
)

pygame.font.init()
WIDTH, HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RThread")
clock = pygame.time.Clock()


BG =(0,0,20)
FONT = pygame.font.Font(None,48)


time_limit_ms = 5000
time_reduction_ms = 500
min_time_limit_ms = 1000
current_challenge = None
challenge_start_time = 0#
FPS = 60



class typing_challenge:
    def __init__(self, phrase, action_type, damage=0, heal = 0):
        self.full_phrase = phrase
        self.typed_phrase = ""
        self.expected_char_index = 0
        self.action_type = action_type
        self.damage_value = damage
        self.heal_value = heal
        self.char_list = list(phrase)
        

def start_new_challenge():
    damage_to_pass = 0
    heal_to_pass = 0
    phrases = [
    
        ("CAST THE LINE","Cast",20),
        ("REEL GENTLY","Gentle Reel",10),
        ("DRINK A PINT","Beverage",10),
        ("QUICK SIT DOWN","Zzzzz",10),
        ("REEL! REEL! REEL!","Strong reel",10)
    ]
    phrase , action , value = random.choice(phrases)
    if action == "CAST THE LINE":
        damage_to_pass = value
    elif action == "REEL":
        damage_to_pass = value
    elif action == "REEL GENTLY":
        heal_to_pass = value
    elif action == "HEAL":
        heal_to_pass = value
   
    global current_challenge, challenge_start_time
    current_challenge = typing_challenge(
        phrase,
        action,
        damage =damage_to_pass,
        heal=heal_to_pass,
         )
    challenge_start_time = pygame.time.get_ticks()





def draw(elapsed_time):
    WIN.fill((0,0,20))
    text_typed = FONT.render(current_challenge.typed_phrase,True,(0,255,0))
    WIN.blit(text_typed,(WIDTH// 4,300))
    remaining_phrase = current_challenge.full_phrase[current_challenge.expected_char_index:]
    text_remaining = FONT.render(remaining_phrase,True,(255,255,255))
    remaining_x = (WIDTH // 4) + text_typed.get_width()
    WIN.blit(text_remaining,(remaining_x,300))
    timer_ratio = elapsed_time / time_limit_ms
    timer_width = WIDTH * (1 - timer_ratio)
    timer_rect = pygame.Rect(0,0, timer_width,20)
    pygame.draw.rect(WIN,(255,0,0), timer_rect)
    pygame.display.flip()
    





def main():
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break   
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() or event.key == pygame.K_SPACE or event.key == pygame.K_EXCLAIM or event.key ==pygame.K_LSHIFT or event.key ==pygame.K_1:
                    pressed_char = event.unicode.upper()

                    if current_challenge.expected_char_index < len(current_challenge.full_phrase):
                        expected_char = current_challenge.full_phrase[current_challenge.expected_char_index]

                    if pressed_char == expected_char:
                        current_challenge.typed_phrase += pressed_char
                        current_challenge.expected_char_index += 1
            
                    if current_challenge.expected_char_index == len(current_challenge.full_phrase):
                        print(f"Challenge Complete, Applying {current_challenge.action_type}")
                        global time_limit_ms,time_reduction_ms,min_time_limit_ms
                        time_limit_ms = max(min_time_limit_ms, time_limit_ms - time_reduction_ms)
                        start_new_challenge()
                    

                else:
                    print("Incorrect Character")
                    current_challenge.typed_phrase = ""
                    current_challenge.expected_char_index = 0
                    

        elapsed_time = pygame.time.get_ticks() - challenge_start_time
        if elapsed_time > time_limit_ms:
            print("Time up!")
            time_limit_ms = 10000
            start_new_challenge()

        draw(elapsed_time)
        clock.tick(FPS)
        

        

    pygame.quit()

if __name__ == "__main__":
    start_new_challenge()
    main()




