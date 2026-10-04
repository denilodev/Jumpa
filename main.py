TILE_SIZE = 8 * 4
GRID_HEIGHT = 16
GRID_WIDTH = 16

WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_WIDTH * TILE_SIZE

TITLE = "Jumpa"

GRAVITY = 0.4
JUMP_FORCE = 15
MAX_FALL_VELOCITY = 6
PLAYER_SPEED = 2

ENEMY_SPEED = 2

# some constants
LEFT = 'l'
RIGHT = 'r'
IDLE = "idle"
MOVING_RIGHT = "moving_right"
MOVING_LEFT = "moving_left"
JUMPING = "jumping"
FALLING = "falling"

# button variables
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 30
TEXT_START_GAME = "Start game"
TEXT_STOP_MUSIC = "Turn music OFF"
TEXT_PLAY_MUSIC = "Turn music ON"
TEXT_EXIT = "Exit"
MUSIC_FILE = "clement-panchout_lj_tel_hiphop"

# levels
FIRST_LEVEL = 0
level_list = [
# level[0] - menu
"\
################\
#              #\
#             e#\
#              #\
#              #\
#              #\
#              #\
#              #\
#              #\
#             @#\
#          #####\
# ####         #\
#              #\
#e      ####   #\
#  ^^^^      ^^#\
################",
# level[1]
"\
################\
#              #\
#             @#\
#    ###########\
#    #         #\
#    #         #\
#   ##   ###   #\
#              #\
#              #\
########     ###\
#     ##       #\
#              #\
#  p       #####\
#    ####      #\
#              #\
################",
# level[2]
"\
################\
#              #\
#@             #\
##             #\
#  #           #\
#    #         #\
#     ##       #\
#         ##   #\
#       ^   #  #\
#      ##      #\
#              #\
#    ###     ###\
# ^    #  ^    #\
# ##   ## ###  #\
#     p# ^^^^^^#\
################",
# level[3]
"\
################\
#              #\
#         @    #\
#         #    #\
#      ^###    #\
#    ###       #\
#             e#\
#  ######      #\
#              #\
#   #         e#\
#        ####  #\
#     #        #\
#  #p          #\
#  ##          #\
#^^^^^^^^^^^^^^#\
################",
# level[4]
"\
################\
#p      #      #\
#       #     @#\
###     e   ####\
#e      #      #\
#       ##     #\
#   e   #      #\
#^     ^#   ####\
##    ^##     e#\
#    ^####     #\
#   ^###       #\
# #####        #\
#       e   ####\
#        ##    #\
#              #\
################",
# level[5]
"\
################\
#              #\
#             e#\
#    #    #    #\
#  ^## ^###    #\
#  #####@    ^^#\
##    ##########\
#             e#\
#     #        #\
##e        ^^  #\
#        ####  #\
#     #        #\
#^^^      e  ^^#\
####   #########\
#p   e^^^^^^^^^#\
################",
# level[6]
"\
################\
#      @#     p#\
#   #####   ####\
#  #           #\
#e             #\
##   ^^^^^^#^# #\
#   #########  #\
#^e   ^        #\
###   #  ##### #\
#    ##^     ###\
#     #####   e#\
# #       #e   #\
#         #    #\
#    #    ###  #\
#^^^^^^^#      #\
################",
]

class TileSet:
    # tiles of the game
    tile_name = {}
    tile_name[' '] = "grass-tile"
    tile_name['#'] = "gold-tile"
    tile_name['^'] = "thorns-tile"
    tile_name['@'] = "red-flag-tile"
    # alive creatures (player, enemies, etc)
    tile_name['p'] = tile_name[' ']
    tile_name['e'] = tile_name[' ']
    # special lists
    solid_tiles = ['#']
    hazard_tiles = ['^']
    transparent_tiles = ['^', '@']

    def __init__(self, width: int, height: int, level_symbols: str):
        self.width = width
        self.height = height
        self.tiles = [[Actor(TileSet.tile_name[' ']) for _ in range(width)] for _ in range(height)]
        self.solid_list = []
        self.hazard_list = []
        self.enemies_list = []
        self.set_tiles(level_symbols)

    def get_tile_symbol(self, i: int, j: int) -> str:
        return self.tile_map[i * GRID_WIDTH + j]
    
    def get_tile_name(self, i: int, j: int) -> str:
        return TileSet.tile_name[self.tiles[i][j]]

    def get_tile(self, x_and_y: tuple) -> Actor:
        x = x_and_y[0]
        y = x_and_y[1]
        return self.tiles[x][y]
    
    def set_specific_tile(self, i: int, j: int, tile: Actor):
        self.tiles[i][j] = tile
    
    def set_tiles(self, tile_map: str):
        self.tile_map = tile_map
        self.have_flag = False
        self.player_initial_coord = (0, 0)
        if len(tile_map) != self.height * self.width:
            raise ValueError("Wrong size of tiles")
        for i in range(self.height):
            for j in range(self.width):
                symbol = tile_map[(self.height * i) + j]
                if symbol in TileSet.tile_name:
                    self.set_specific_tile(i, j, Actor(TileSet.tile_name[symbol]))
                    self.tiles[i][j].topleft = j * TILE_SIZE, i * TILE_SIZE
                    # player location
                    if symbol == 'p':
                        self.player_initial_coord = self.tiles[i][j].center
                    # enemies location
                    elif symbol == 'e':
                        self.new_enemy(self.tiles[i][j].center)
                    # flag location
                    elif symbol == '@':
                        self.have_flag = True
                        self.flag = self.tiles[i][j]
                else:
                    raise ValueError(f"This symbol ({symbol}) doesn't exist")
                if symbol in TileSet.solid_tiles:
                    self.solid_list.append((i, j))
                if symbol in TileSet.hazard_tiles:
                    self.hazard_list.append((i, j))
    
    def draw_tiles(self):
        for i in range(self.height):
            for j in range(self.width):
                # draw the sky behind the transparent tiles
                if self.get_tile_symbol(i, j) in TileSet.transparent_tiles:
                    Actor(TileSet.tile_name[' '], self.tiles[i][j].center).draw()
                self.tiles[i][j].draw()
        for enemy in self.enemies_list:
            enemy.draw()
    
    def coord_to_tile_symbol(self, x, y):
        tile_x = int(x / TILE_SIZE)
        tile_y = int(y / TILE_SIZE)
        return self.tiles[tile_y][tile_x]
    
    def new_enemy(self, coord):
        enemy = Character("ghost-right0", coord)
        enemy.add_state(MOVING_LEFT, all_sprites("ghost-left", 0, 1), 0.2)
        enemy.add_state(MOVING_RIGHT, all_sprites("ghost-right", 0, 1), 0.2)
        enemy.vx = ENEMY_SPEED
        enemy.set_state(MOVING_RIGHT)
        self.enemies_list.append(enemy)

class Button:
    def __init__(self, rect, normal_color, hover_color, text):
        self.text = text
        self.rect = rect
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.is_hover = False
    
    def draw(self):
        if self.is_hover:
            screen.draw.filled_rect(self.rect, self.hover_color)
        else:
            screen.draw.filled_rect(self.rect, self.normal_color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color="black")

class LevelManager:
    def __init__(self, level_list: list):
        if not level_list:
            raise ValueError("No levels in the list")
        
        self.level_list = [TileSet(GRID_WIDTH, GRID_HEIGHT, level) for level in level_list]
        self.last_scene_number = len(level_list)-1
        self.current_scene = FIRST_LEVEL

        # menu variables
        mid_of_screen = (WIDTH-BUTTON_WIDTH)/2
        button_size = (BUTTON_WIDTH, BUTTON_HEIGHT)
        self.list_of_buttons = [
            Button(Rect((mid_of_screen, 130), button_size), "yellow", "orange", TEXT_START_GAME),
            Button(Rect((mid_of_screen, 190), button_size), "yellow", "orange", TEXT_STOP_MUSIC),
            Button(Rect((mid_of_screen, 250), button_size), "yellow", "orange", TEXT_EXIT)
            ]

    def get_current_scene_number(self):
        return self.current_scene
    
    def change_to_next_scene(self):
        if self.current_scene == self.last_scene_number:
            self.current_scene = 0
        else:
            self.current_scene += 1
    
    def change_to_previous_scene(self):
        if self.current_scene == 0:
            self.current_scene = self.last_scene_number
        else:
            self.current_scene -= 1
    
    def level(self, level_number):
        if level_number < 0 or level_number > self.last_scene_number:
            return None
        return self.level_list[level_number]
    
    def current_level(self):
        return self.level_list[self.current_scene]

    def draw_menu(self):
        for button in self.list_of_buttons:
            button.draw()

class Character(Actor):
    def __init__(self, name, coord):
        super().__init__(name, coord)
        self.define_initial_coord(coord)
        self.vx = 0
        self.vy = 0
        self.already_jumped = False
        self.states = {}
        self.change_time = {}
        self.current_state_name = ""
        self.current_sprite = 0
        self.direction = LEFT
    
    def define_initial_coord(self, coord):
        self.initial_coord = coord
    
    def move_y(self):
        self.bottom += self.vy
    
    def move_x(self):
        self.right += self.vx

    def reset_position(self):
        self.center = self.initial_coord
    
    def add_state(self, state_name, sprite_list, change_time):
        self.states[state_name] = sprite_list
        self.change_time[state_name] = change_time
    
    def set_state(self, new_state_name):
        if self.current_state_name == new_state_name:
            return
        clock.unschedule(self.next_sprite)
        self.current_state_name = new_state_name
        self.current_sprite = 0
        self.image = self.states[self.current_state_name][self.current_sprite]
        clock.schedule_interval(self.next_sprite, self.change_time[self.current_state_name])
    
    def next_sprite(self):
        if self.current_sprite == len(self.states[self.current_state_name])-1:
            self.current_sprite = 0
        else:
            self.current_sprite += 1
        self.image = self.states[self.current_state_name][self.current_sprite]

def all_sprites(sprite_name, first_number, last_number):
    return [f"{sprite_name}{i}" for i in range(first_number, last_number+1)]

# singleton of level manager
LEVELS = LevelManager(level_list)

# player character
player = Character("player-idle0", LEVELS.current_level().player_initial_coord)
player.add_state(IDLE, all_sprites("player-idle", 0, 1), 0.5)
player.set_state(IDLE)
player.add_state(MOVING_RIGHT, all_sprites("player-walking-right", 0, 1), 0.1)
player.add_state(MOVING_LEFT, all_sprites("player-walking-left", 0, 1), 0.1)
player.add_state(JUMPING, ["player-jumping"], 1)
player.add_state(FALLING, ["player-falling"], 1)    

music.play(MUSIC_FILE)

def draw():
    screen.clear()
    LEVELS.current_level().draw_tiles()
    if LEVELS.get_current_scene_number() == 0:
        LEVELS.draw_menu()
    else:
        player.draw()

def update():
    ###### PLAYER MOVEMENT ######
    # gravity and jump
    player.vy += GRAVITY
    if player.vy > 0 and player.already_jumped:
        player.set_state(FALLING)
    if player.vy > MAX_FALL_VELOCITY:
        player.vy = MAX_FALL_VELOCITY
    if keyboard.space and not player.already_jumped:
        player.vy -= JUMP_FORCE
        player.already_jumped = True
        player.set_state(JUMPING)
    player.move_y()
    for tile in LEVELS.current_level().solid_list:
        tile_actor = LEVELS.current_level().get_tile(tile)
        if player.colliderect(tile_actor):
            if player.vy > 0:
                player.already_jumped = False
                player.bottom = tile_actor.top
            else:
                player.vy = 0
                player.top = tile_actor.bottom
    
    # horizontal movement
    player.vx = 0
    if keyboard.a:
        player.vx = -PLAYER_SPEED
        if not player.already_jumped:
            player.set_state(MOVING_LEFT)
    elif keyboard.d:
        player.vx = PLAYER_SPEED
        if not player.already_jumped:
            player.set_state(MOVING_RIGHT)
    if player.vx != 0:
        player.move_x()
        for tile in LEVELS.current_level().solid_list:
            tile_actor = LEVELS.current_level().get_tile(tile)
            if player.colliderect(tile_actor):
                if player.vx > 0:
                    player.right = tile_actor.left
                else:
                    player.left = tile_actor.right
    else:
        if not player.already_jumped:
            player.set_state(IDLE)

    # check if player touches in any hazard tile
    for tile in LEVELS.current_level().hazard_list:
        tile_actor = LEVELS.current_level().get_tile(tile)
        if player.colliderect(tile_actor):
            sounds.hit.play()
            player.reset_position()

    # check if touched the flag
    if LEVELS.current_level().have_flag:
        if player.colliderect(LEVELS.current_level().flag):
            LEVELS.change_to_next_scene()
            player.define_initial_coord(LEVELS.current_level().player_initial_coord)
            sounds.flag.play()
            player.reset_position()

    ###### ENEMIES MOVEMENT ######
    # horizontal movement
    for enemy in LEVELS.current_level().enemies_list:
        enemy.move_x()
        for tile in LEVELS.current_level().solid_list:
            tile_actor = LEVELS.current_level().get_tile(tile)
            if player.colliderect(enemy):
                player.reset_position()
                sounds.hit.play()
            if enemy.colliderect(tile_actor):
                if enemy.vx > 0:
                    enemy.right = tile_actor.left
                    enemy.set_state(MOVING_LEFT)
                else:
                    enemy.left = tile_actor.right
                    enemy.set_state(MOVING_RIGHT)
                enemy.vx = -enemy.vx
    
def on_mouse_move(pos):
    if LEVELS.get_current_scene_number() == 0:
        for button in LEVELS.list_of_buttons:
            if button.rect.collidepoint(pos):
                button.is_hover = True
            else:
                button.is_hover = False

def on_mouse_down(button):
    if button == mouse.LEFT and LEVELS.get_current_scene_number() == 0:
        if LEVELS.list_of_buttons[0].is_hover:
            LEVELS.change_to_next_scene()
            player.define_initial_coord(LEVELS.current_level().player_initial_coord)
            player.reset_position()
        elif LEVELS.list_of_buttons[1].is_hover:
            if music.is_playing(MUSIC_FILE):
                music.pause()
                LEVELS.list_of_buttons[1].text = TEXT_PLAY_MUSIC
            else:
                music.unpause()
                LEVELS.list_of_buttons[1].text = TEXT_STOP_MUSIC
            pass
        elif LEVELS.list_of_buttons[2].is_hover:
            # close the game (no way without import pygame or sys)
            raise RuntimeError("Couldn't find how to quit the game, so put this here :)")
            pass

def on_key_down(key):
    # change level
    if key == keys.L:
        LEVELS.change_to_next_scene()
        player.define_initial_coord(LEVELS.current_level().player_initial_coord)
        player.reset_position()
        for enemy in LEVELS.current_level().enemies_list:
            enemy.reset_position()
        LEVELS.current_level
        print(f"Going to level: {LEVELS.get_current_scene_number()}")
    elif keyboard.k:
        LEVELS.change_to_previous_scene()
        player.reset_position()
        for enemy in LEVELS.current_level().enemies_list:
            enemy.reset_position()
        print(f"Going to level: {LEVELS.get_current_scene_number()}")

        # if player_velocity_y < 0 and not can_go_up(alien, lvl1):
        #     player_velocity_y = 0
        # elif keyboard.space and can_go_up(alien, lvl1) and not can_go_down(alien, lvl1):
        #     player_velocity_y = -jump_force
        # elif can_go_down(alien, lvl1):
        #     player_velocity_y += GRAVITY
        #     if player_velocity_y > max_velocity:
        #         player_velocity_y = max_velocity
        # else:
        #     player_velocity_y = 0
        # alien.top += player_velocity_y
        # if keyboard.a and can_go_left(alien, lvl1):
        #     alien.right -= SPEED
        # if keyboard.d and can_go_right(alien, lvl1):
        #     alien.right += SPEED
