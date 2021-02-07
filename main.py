import pygame, sys, random
# from floor import draw_floor

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,900))
    screen.blit(floor_surface, (floor_x_pos + 576 ,900))

def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (824, random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (824, random_pipe_height-250))

    return bottom_pipe, top_pipe

def delete_pipes(pipes):
    if len(pipes) > 4:
        del pipes[0]
        return pipes

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    
    if bird_rect.top <= 0 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f"Score : {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288, 75))
        screen.blit(score_surface, score_rect)

    elif game_state == 'game_over':
        score_surface = game_font.render(f"Score : {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288, 75))
        screen.blit(score_surface, score_rect)

        high_score_surface = high_score_font.render(f"High Score : {int(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288, 130))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency= 48000, size = 32, channels = 1, buffer = 512)
pygame.init()

screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',35)
high_score_font = pygame.font.Font('04B_19.ttf', 55)

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')


# game variable
gravity = 0.15
bird_movement = 0
pipe_height = [440, 490, 560, 640]
game_active = True
score = 0
high_score = 0
score_sound_countdown = 100

# game surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png')).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png')).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100, 512))

pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
            elif event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.centery = 400
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            move_pipes(pipe_list)

        if event.type == BIRDFLAP:
            # print('changing bird')
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

# bg surface add
    screen.blit(bg_surface, (0,0))

    if game_active:
    # bird and movement
        bird_movement += gravity
        roated_bird = rotate_bird(bird_surface)        
        bird_rect.centery += bird_movement
        screen.blit(roated_bird, bird_rect)
        check_collision(pipe_list)
        game_active = check_collision(pipe_list)

    # pipes
        pipe_list = move_pipes(pipe_list)
        delete_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        score += 0.01
        score_display('main_game')

        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            # score_sound.play()
            score_sound_countdown = 100


    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    

    

# floor 
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)