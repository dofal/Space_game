import pygame
pygame.font.init()
pygame.mixer.init()

#setting of game

hight = 800
width = 1400
fps = 60
hight_spaceship = 75
width_spaceship = 75
spaceship_speed = 10
bullet_speed = 20
max_bullets = 3

window = pygame.display.set_mode((width, hight))
border = pygame.Rect(width // 2 - 5, 0, 10, hight)
pygame.display.set_caption("the Game")
black = (0, 0, 0)
red_col = (255, 0, 0)
yellow_col = (255, 255, 255)
health_font = pygame.font.SysFont("roboto", 60)
winner_font = pygame.font.SysFont("Roboto", 120)
bullet_hit_sound = pygame.mixer.Sound("Grenade+1.mp3")
bullet_fire_sound = pygame.mixer.Sound("Gun+Silencer.mp3")

###################################
###import + settings of imports ###
###################################

#imports of images

spaceship1 = pygame.image.load("spaceship_yellow.png")
spaceship2 = pygame.image.load("spaceship_red.png")
space = pygame.image.load("space.jpg")

# import of sounds
yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

#settings of images(size, rotation)

spaceship1 = pygame.transform.scale(spaceship1, (width_spaceship, hight_spaceship))
spaceship1 = pygame.transform.rotate(spaceship1, 90)
spaceship2 = pygame.transform.scale(spaceship2, (width_spaceship, hight_spaceship))
spaceship2 = pygame.transform.rotate(spaceship2, 270)
space = pygame.transform.scale(space, (width, hight))





###################################
######### functions part ##########
###################################


def draw_window(red, yellow, left_bullets, right_bullets, yellow_health, red_health):
    window.blit(space, (0, 0))
    pygame.draw.rect(window, black, border)
    red_health_text = health_font.render("Health: " + str(red_health), 1, yellow_col )
    yellow_health_text = health_font.render("Health: " + str(yellow_health), 1, yellow_col )
    window.blit(red_health_text, (width/2 + 50, 50))
    window.blit(yellow_health_text, (width / 2 - 250, 50))
    window.blit(spaceship1,(yellow.x, yellow.y))
    window.blit(spaceship2, (red.x, red.y))
    for bullet in right_bullets:
        pygame.draw.rect(window, red_col, bullet)
    for bullet in left_bullets:
        pygame.draw.rect(window, yellow_col, bullet)
    pygame.display.update()

def left_movement(key_pressed, yellow):
        #left spaceship control
    if key_pressed[pygame.K_a] and yellow.x >= 5:
        yellow.x -= spaceship_speed
    elif key_pressed[pygame.K_d] and yellow.x <= width/2 - width_spaceship - 5:
        yellow.x += spaceship_speed
    elif key_pressed[pygame.K_w] and yellow.y >= 5:
        yellow.y -= spaceship_speed
    elif key_pressed[pygame.K_s] and yellow.y <= hight - hight_spaceship - 5:
        yellow.y += spaceship_speed

def right_movement(key_pressed, red):
       #right spaceship control
    if key_pressed[pygame.K_LEFT] and red.x >= width/2 + 5:
        red.x -= spaceship_speed
    elif key_pressed[pygame.K_RIGHT] and red.x <= width - width_spaceship - 5:
        red.x += spaceship_speed
    elif key_pressed[pygame.K_UP] and red.y >= 5:
        red.y -= spaceship_speed
    elif key_pressed[pygame.K_DOWN] and red.y <= hight - hight_spaceship - 5:
        red.y += spaceship_speed
    
def handle_bullets(left_bullets, right_bullets, yellow, red):
    for bullet in left_bullets:
        bullet.x += bullet_speed
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            left_bullets.remove(bullet)
            bullet_hit_sound.play()
        elif bullet.x >= width:
            left_bullets.remove(bullet)
    for bullet in right_bullets:
        bullet.x -= bullet_speed
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            right_bullets.remove(bullet)
            bullet_hit_sound.play()
        elif bullet.x <= 0:
            right_bullets.remove(bullet)

def win (text):
    draw_text = winner_font.render(text, 1, yellow_col)
    window.blit(draw_text, (width/2 - draw_text.get_width()/2, hight/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow = pygame.Rect(50, hight/2, width_spaceship, hight_spaceship)
    red = pygame.Rect(width - 100, hight/2, width_spaceship, hight_spaceship)
    clock = pygame.time.Clock()
    left_bullets = []
    right_bullets = []
    yellow_health = 10
    red_health = 10
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and len(left_bullets) <= max_bullets:
                    bullet = pygame.Rect(yellow.x + width_spaceship, yellow.y + hight_spaceship // 2 - 2, 10, 5)
                    left_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_m and len(right_bullets) <= max_bullets:
                    bullet = pygame.Rect(red.x, red.y + hight_spaceship // 2 - 2, 10, 5)
                    right_bullets.append(bullet)
                    bullet_fire_sound.play()
            if event.type == red_hit:
                red_health -= 1
            elif event.type == yellow_hit:
                yellow_health -= 1

        winner_text = "" 
        if red_health <= 0:
            winner_text = "Player on the left side won."
        if yellow_health <= 0:
            winner_text = "Player on the right side won."
        if winner_text != "":
            win(winner_text)
            break
        print(left_bullets, right_bullets)
        draw_window(red, yellow, left_bullets, right_bullets, yellow_health, red_health)
        key_pressed = pygame.key.get_pressed()
        handle_bullets(left_bullets, right_bullets, yellow, red)
        left_movement(key_pressed, yellow)
        right_movement(key_pressed, red)


    main()          

if __name__ == "__main__":
    main()

