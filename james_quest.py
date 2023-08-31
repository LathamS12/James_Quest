import time
import random
import pygame
from pygame.locals import *

ASSET_FOLDER = 'C:/Users/Scott/Desktop/James Quest/James Quest/Assets'
IMAGES = f'{ASSET_FOLDER}/Images'
SOUNDS = f'{ASSET_FOLDER}/Sound effects'

pygame.mixer.init()
pygame.init()

######### Define classes #########

class Room:
    def __init__(self, name, special=0):
        image_link = f'{IMAGES}/{name}'

        if special==1:
            self.wall_0 = Wall(f'{image_link}_0.png')

        else:
            self.wall_0 = Wall(f'{image_link}_0.png')
            self.wall_1 = Wall(f'{image_link}_1.png')
            self.wall_2 = Wall(f'{image_link}_2.png')
            self.wall_3 = Wall(f'{image_link}_3.png')


class Wall:
    def __init__(self, image):
        self.image = image
        self.surf = pygame.image.load(image).convert()


class Exit:
    def __init__(self, next_room):
        self.next_room = next_room


class Button:
    def __init__(self, name, colorkey, loc_x, loc_y):
        self.surf = pygame.image.load(f'{IMAGES}/{name}.png').convert()
        self.surf.set_colorkey(colorkey)
        self.loc_x = loc_x
        self.loc_y = loc_y



######## Set up game ##########
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1067
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 
TOP_LEFT_CORNER = (0, 0)

  
#intro, ending scenes (created as 'rooms')
intro = Room('Intro', 1)
ending = Room('Ending', 1)

#Map
crib = Room('Crib')

chair = Room('Chair')
chair.wall_2.exit = Exit('crib')
chair.wall_3.exit = Exit('nursery')

nursery = Room('Nursery')
nursery.wall_0.exit = Exit('chair')
nursery.wall_2.exit = Exit('landing')

landing = Room('Landing')
landing.wall_0.exit = Exit('nursery')
landing.wall_3.exit = Exit('loft1')

bedroom1 = Room('Bedroom1')
bedroom1.wall_0.exit = Exit('landing')
bedroom1.wall_3.exit = Exit('bedroom2')

bedroom2 = Room('Bedroom2')
bedroom2.wall_1.exit = Exit('bedroom1')

loft1 = Room('Loft1')
loft1.wall_1.exit = Exit('landing')
loft1.wall_3.exit = Exit('loft2')

loft2 = Room('Loft2')
loft2.wall_1.exit = Exit('loft1')

living_room1 = Room('Living_room1')
living_room1.wall_3.exit = Exit('living_room2')

living_room2 = Room('Living_room2')
living_room2.wall_1.exit = Exit('living_room1')
living_room2.wall_3.exit = Exit('dining_room1')

dining_room1 = Room('Dining_room1')
dining_room1.wall_1.exit = Exit('living_room2')
dining_room1.wall_3.exit = Exit('dining_room2')

dining_room2 = Room('Dining_room2')
dining_room2.wall_1.exit = Exit('dining_room1')
dining_room2.wall_3.exit = Exit('kitchen1')

kitchen1 = Room('Kitchen1')
kitchen1.wall_1.exit = Exit('dining_room2')
kitchen1.wall_2.exit = Exit('kitchen2')

kitchen2 = Room('Kitchen2')
kitchen2.wall_0.exit = Exit('kitchen1')


room_dict = {
    'intro': intro,
    'crib': crib, 
    'chair': chair,
    'nursery': nursery,
    'landing': landing,
    'bedroom1': bedroom1,
    'bedroom2': bedroom2,
    'loft1': loft1,
    'loft2': loft2,
    'living_room1': living_room1,
    'living_room2': living_room2,
    'dining_room1': dining_room1,
    'dining_room2': dining_room2,
    'kitchen1': kitchen1,
    'kitchen2': kitchen2,
    'ending': ending
}

#room_dict = {}
def add_room():
    pass
    #Create room,
    #Add to dictionary

################
# Game state
################
CURRENT_ROOM = intro #Starting room
DIRECTION_COUNTER = 0
DIRECTION = 0

BUNNIES_GRABBED = False
DAD_IS_AWAKE = False
PICTURE_DRAWN = False
PICTURE_FRAME_COUNTER = 0


#GUI
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

left_arrow = Button('arrow_left', WHITE, 75, 900)
right_arrow = Button('arrow_right', WHITE, 1325, 900)
forward_arrow = Button('arrow_forward', WHITE, 700, 725)


#Sounds
SOUND_ON=True

pygame.mixer.music.load(f'{SOUNDS}/James_Quest_theme.wav')

let_it_be = pygame.mixer.Sound(f'{SOUNDS}/Let_it_be.wav')
dad_waking_up = pygame.mixer.Sound(f'{SOUNDS}/Scott_waking_up.wav')
maggie_scratches_door = pygame.mixer.Sound(f'{SOUNDS}/maggie_scratches_door.wav')
go_downstairs = pygame.mixer.Sound(f'{SOUNDS}/go_downstairs.wav')
marker_squeak = pygame.mixer.Sound(f'{SOUNDS}/marker_squeak.wav')
end_scene = pygame.mixer.Sound(f'{SOUNDS}/end_scene.wav')

GRUNTS = []
SQUEALS = []
GIGGLES = []
MAGGIE_SOUNDS = []

TOTAL_GRUNTS = 27
TOTAL_SQUEALS = 15
TOTAL_GIGGLES = 5
TOTAL_MAGGIE_SOUNDS = 5


for x in range(1, TOTAL_GRUNTS+1):
    GRUNTS.append(pygame.mixer.Sound(f'{SOUNDS}/Grunt_{x}.wav'))

for x in range(1, TOTAL_SQUEALS+1):
    SQUEALS.append(pygame.mixer.Sound(f'{SOUNDS}/Squeal_{x}.wav'))

for x in range(1, TOTAL_GIGGLES+1):
    GIGGLES.append(pygame.mixer.Sound(f'{SOUNDS}/Giggle_{x}.wav'))

for x in range(1, TOTAL_MAGGIE_SOUNDS+1):
    MAGGIE_SOUNDS.append(pygame.mixer.Sound(f'{SOUNDS}/maggie_{x}.wav'))


def play_random_sound(sound_type, total, fraction_played=1):
    random_num = random.random() #defaults to 0-1
    play_it = random_num <= fraction_played

    if play_it:
        random_sound = random.randint(0, total-1) 
        sound_type[random_sound].play()




######## Define Game #############
def game_loop():
    running = True

    pygame.mixer.music.play(-1, 0.0)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                wall = get_wall(CURRENT_ROOM)
                handle_click(wall, mouse_x, mouse_y)

        #'View' is a surface      
        update_view()
        pygame.display.update()



def handle_click(wall, x, y):
    SPECIAL_ROOM = (CURRENT_ROOM is intro) or (CURRENT_ROOM is ending)  
    if SPECIAL_ROOM:
        pass

    else:
        left_button = (75 < x < 225) and (900 < y < 1000)
        right_button = (1325 < x < 1475) and (900 < y < 1000)
        forward_button = (700 < x < 800) and (725 < y < 800)

        if left_button:
            turn('left')

        if right_button:
            turn('right')
        
        if forward_button:
            exit_exists = check_for_exit()
            if exit_exists:
                print(wall.exit)
                move_to_room(wall.exit.next_room)
            else:
                print('No exit available')

    handle_special_click(wall, x, y)

#Basic movement
def turn(direction):  
    global DIRECTION_COUNTER, DIRECTION 
    
    if direction == 'left':
        print('Turning left')
        DIRECTION_COUNTER -= 1
        

    if direction == 'right':
        print('Turning right')
        DIRECTION_COUNTER += 1

    DIRECTION = DIRECTION_COUNTER % 4
    
    if SOUND_ON:
        play_random_sound(GRUNTS, TOTAL_GRUNTS, .50)



def move_to_room(room_name):
    global CURRENT_ROOM
    CURRENT_ROOM = room_dict[room_name]
    

def update_view():
    wall = get_wall(CURRENT_ROOM)
    current_view = wall.surf
    SCREEN.blit(current_view, TOP_LEFT_CORNER)
    
    if (CURRENT_ROOM is intro) or (CURRENT_ROOM is ending):
        buttons = []
    
    else:
        exit = check_for_exit()
        if exit:
            buttons = [left_arrow, right_arrow, forward_arrow]
        else:
            buttons = [left_arrow, right_arrow]
   
    for button in buttons:
        SCREEN.blit(button.surf, (button.loc_x, button.loc_y))


def check_for_exit():
    wall = get_wall(CURRENT_ROOM)
    try:
        if wall.exit.next_room:
            return True
    except AttributeError:
            return False


def get_wall(room):
    if DIRECTION == 0:
        return room.wall_0
    elif DIRECTION == 1:
        return room.wall_1
    elif DIRECTION == 2:
        return room.wall_2
    elif DIRECTION == 3:
        return room.wall_3
    else:
        print('View direction out of scope')



#Special clicks & events
def handle_special_click(wall, x, y):
    PLACEHOLDER = (200 < x < 1400) and (200 < y < 900)

    #Actions you have to complete to move forward
    start_game_button = (wall is intro.wall_0) and (1160 < x < 1510) and (720 < y < 945)
    if start_game_button:
        start_game()
    
    grab_bunnies = (wall is crib.wall_2) and (200 < x < 800) and (350 < y < 850)
    if grab_bunnies:
        grab_the_bunnies()

    stack_bunnies = BUNNIES_GRABBED and (wall is crib.wall_0) and (600 < x < 1100) and (350 < y < 700)
    if stack_bunnies:
        stack_the_bunnies()
    
    maggie_loft = (wall is loft2.wall_2) and (720 < x < 910) and (370 < y < 510)
    if maggie_loft:
        maggie_opens_door()
 
    bed_remote = (DAD_IS_AWAKE==False) and (wall is bedroom2.wall_3) and (1000 < x < 1050) and (500 < y < 590)
    if bed_remote:
        dad_wakes_up()

    dad_feet = DAD_IS_AWAKE and (wall is bedroom1.wall_2) and (400 < x < 1200) and (0 < y < 1067)
    if dad_feet: 
        dad_takes_james_downstairs()

    baby_walker = (wall is kitchen2.wall_2) and (500 < x < 1400) and (400 < y < 1067)
    if baby_walker:
        play_ending()
    

    #Other special events
    picture_living_room = (wall is living_room1.wall_0) and (575 < x < 850) and (250 < y < 660)
    if picture_living_room:
        change_picture_frame()

    maggie_living_room = (wall is living_room2.wall_2) and (1025 < x < 1325) and (650 < y < 850)
    if maggie_living_room:
        play_random_sound(MAGGIE_SOUNDS, TOTAL_MAGGIE_SOUNDS)
        

    dry_erase_board = (PICTURE_DRAWN == False) and (wall is kitchen1.wall_3) and (670 < x < 880) and (200 < y < 525)
    if dry_erase_board:
        draw_on_board()

    
        

    #Giggles
    toys_nursery = (wall is nursery.wall_3) and (525 < x < 1225) and (400 < y < 675)
    if toys_nursery:
        GIGGLES[3].play()

    james_mirror = (wall is bedroom2.wall_0) and (885 < x < 1065) and (350 < y < 560)
    if james_mirror:
        GIGGLES[4].play() 

    toys_living_room = (wall is living_room2.wall_0) and (200 < x < 1600) and (0 < y < 725)
    if toys_living_room:
        play_random_sound(GIGGLES, 3)



def start_game():
    pygame.mixer.music.stop()
    opening_scene()
    move_to_room('crib')

def opening_scene():   
    draw_to_screen('introscene_0', 2)
    
    let_it_be.play()
    draw_to_screen('introscene_1', 5)
    draw_to_screen('introscene_2', 5)
    draw_to_screen('introscene_3', 5)
    draw_to_screen('introscene_4', 4)
    draw_to_screen('introscene_5', 5)
    draw_to_screen('introscene_6', 2)
    draw_to_screen('introscene_7', 5)


def ending_scene():
    draw_to_screen('endscene_1', 3)
    
    end_scene.play()
    time.sleep(4)

    draw_to_screen('endscene_2', 5)
    draw_to_screen('endscene_3', 3.5)
    draw_to_screen('endscene_4', 3.5)
    draw_to_screen('endscene_5', 3.5)
    draw_to_screen('endscene_6', 3.5)


def draw_to_screen(image, seconds):
    image_surface = pygame.image.load(f'{ASSET_FOLDER}/Images/{image}.png').convert()
    SCREEN.blit(image_surface, TOP_LEFT_CORNER)
    pygame.display.update()
    time.sleep(seconds)


def grab_the_bunnies():
    global BUNNIES_GRABBED
    BUNNIES_GRABBED = True

    new_crib_wall = f'{IMAGES}/crib_2_part2.png'
    crib.wall_2.surf = pygame.image.load(new_crib_wall).convert()

def stack_the_bunnies():
    new_crib_wall = f'{IMAGES}/crib_0_part2.png'
    crib.wall_0.surf = pygame.image.load(new_crib_wall).convert()
    crib.wall_0.exit = Exit('chair')
     
    play_random_sound(SQUEALS, TOTAL_SQUEALS)

def maggie_opens_door():
    play_cutscene(maggie_scratches_door, 20)
    new_loft_wall = f'{IMAGES}/Loft2_2_part2.png'
    loft2.wall_2.surf = pygame.image.load(new_loft_wall).convert()

    new_landing_wall = f'{IMAGES}/Landing2_part2.png'
    landing.wall_2.surf = pygame.image.load(new_landing_wall).convert()
    landing.wall_2.exit = Exit('bedroom1')

def dad_wakes_up():
    global DAD_IS_AWAKE
    DAD_IS_AWAKE = True
    
    play_cutscene(dad_waking_up, 21)

    br1_wall = f'{IMAGES}/Bedroom1_2_part2.png'
    bedroom1.wall_2.surf = pygame.image.load(br1_wall).convert()

    br2_wall = f'{IMAGES}/Bedroom2_2_part2.png'
    bedroom2.wall_2.surf = pygame.image.load(br2_wall).convert()
    

def dad_takes_james_downstairs():
    global CURRENT_ROOM, DIRECTION, DIRECTION_COUNTER
    play_cutscene(go_downstairs, 17)

    CURRENT_ROOM = living_room2
    DIRECTION = 0
    DIRECTION_COUNTER = 0


def change_picture_frame():
    global PICTURE_FRAME_COUNTER

    PICTURE_FRAME_COUNTER +=1
    picture_number = PICTURE_FRAME_COUNTER % 5

    wall_image = f'{IMAGES}/Living_room1_0_pic{picture_number}.png'
    living_room1.wall_0.surf = pygame.image.load(wall_image).convert()


def draw_on_board():
    global PICTURE_DRAWN
    PICTURE_DRAWN = True

    marker_squeak.play()
    time.sleep(3)

    dry_erase_pic = f'{IMAGES}/Kitchen1_3_part2.png'
    kitchen1.wall_3.surf = pygame.image.load(dry_erase_pic).convert()


def play_ending():
    global CURRENT_ROOM, DIRECTION, DIRECTION_COUNTER
    DIRECTION_COUNTER = 0
    DIRECTION = 0
    CURRENT_ROOM = ending

    ending_scene()

    ending_screen = f'{IMAGES}/the_end.png'
    ending.wall_0.surf = pygame.image.load(ending_screen).convert()


def play_cutscene(scene, seconds):
    scene.play()
    pygame.draw.rect(SCREEN, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.flip()
    time.sleep(seconds)


def test_rect(x1, y1, len, ht):
    pygame.draw.rect(SCREEN, WHITE,(x1, y1, len, ht))
    pygame.display.flip()
    time.sleep(2)


game_loop()


'''
def check_if_quit2():
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            
    return quit

'''
