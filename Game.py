# pylint: disable-msg=C0111
# pylint: disable-msg=C0301
""" Main file for the project till I have time to refactor the code to something more manage-able """
try:
    from TestTheme import TestTheme
    from CharCreator import CharCreator
    from Room import Room
    from pgu import gui
    from sets import Set
    import pygame
    import sys
    import math
    from math import sqrt
    import os
    from pprint import pprint #IGNORE:W0611
    from pygame.locals import * #IGNORE:W0614
    from MapTile import MapTile
    from pathfinder import PathFinder
    from random import randint, randrange, choice
    from Cursors import Cursors
    from CombatLog import CombatLog
    from Stats import Stats
    import ConfigParser
    from MonsterGenerator import MonsterGenerator
    from ItemGenerator import ItemGenerator
    import pickle
    from Inventory import Inventory
    from PlayerInfo import PlayerInfo
    from QuitDialogue import QuitDialogue
    from Misc import is_in_fov, make_cursor, move_cost, roll_damage, roll_d_20, pick_wall_tile, roll_d_10
except ImportError, err:
    print "couldn't load module, %s" % (err)
    sys.exit(2)
#Constants
CONFIG = ConfigParser.ConfigParser()
CONFIG.readfp(open('game.conf'))

FPS = 60
FULLSCREEN_WIDTH = CONFIG.getint('game', 'fullscreen_width')
FULLSCREEN_HEIGHT = CONFIG.getint('game', 'fullscreen_height')
TILE_WIDTH = 32

MOBS_PER_ROOM = [0, 1, 2, 4] # spawn rate

class Game:
    """Main game object"""
    def __init__(self):
        self.create_chars = True
        self.running = True # set the game loop good to go
        self.window_width = CONFIG.getint('game', 'window_width')
        self.window_height = CONFIG.getint('game', 'window_height')
        self.mapw = 100
        self.maph = 100
        self.fullscreen = False
        self.current_z = 0
        self.buttons = {}
        self.motion = None
        self.turn = 0
        self.moves = Set()
        self.win = None
        self.pathlines = []
        self.click_state = None
        self.show_inventory = False
        self.player_info = False
        self.show_quit_diag = False
        self.floor_images = [pygame.image.load(os.path.join('images', 'floor.png'))]
        self.fog_images = [pygame.image.load(os.path.join('images', 'fog.png')), # 0 
                            pygame.image.load(os.path.join('images', 'fog_b.png')), # 1
                            pygame.image.load(os.path.join('images', 'fog_b_l.png')), # 2
                            pygame.image.load(os.path.join('images', 'fog_b_l_r.png')), # 3
                            pygame.image.load(os.path.join('images', 'fog_b_r.png')), # 4
                            pygame.image.load(os.path.join('images', 'fog_b_t_l.png')), # 5
                            pygame.image.load(os.path.join('images', 'fog_b_t_r.png')), # 6
                            pygame.image.load(os.path.join('images', 'fog_l.png')), # 7
                            pygame.image.load(os.path.join('images', 'fog_l_r.png')), # 8
                            pygame.image.load(os.path.join('images', 'fog_r.png')), # 9
                            pygame.image.load(os.path.join('images', 'fog_t.png')), # 10
                            pygame.image.load(os.path.join('images', 'fog_t_b.png')), # 11
                            pygame.image.load(os.path.join('images', 'fog_t_l.png')), # 12 
                            pygame.image.load(os.path.join('images', 'fog_t_l_r.png')), # 13
                            pygame.image.load(os.path.join('images', 'fog_t_r.png')), # 14
                            pygame.image.load(os.path.join('images', 'fog_t_l_corner.png')), # 15
                            pygame.image.load(os.path.join('images', 'fog_t_r_corner.png')), # 16
                            pygame.image.load(os.path.join('images', 'fog_b_l_corner.png')), # 17
                            pygame.image.load(os.path.join('images', 'fog_b_r_corner.png')), # 18
                            pygame.image.load(os.path.join('images', 'fog_b_tl_corner.png')), # 19
                            pygame.image.load(os.path.join('images', 'fog_b_tr_corner.png')), # 20
                            pygame.image.load(os.path.join('images', 'fog_b_tl_tr_corner.png')), # 21
                            pygame.image.load(os.path.join('images', 'fog_t_bl_corner.png')), # 22
                            pygame.image.load(os.path.join('images', 'fog_t_br_corner.png')), # 23
                            pygame.image.load(os.path.join('images', 'fog_t_bl_br_corner.png')), # 24
                            pygame.image.load(os.path.join('images', 'fog_pillar.png')), # 25
                            pygame.image.load(os.path.join('images', 'fog_l_br_corner.png')), # 26
                            pygame.image.load(os.path.join('images', 'fog_l_tr_corner.png')), # 27
                            pygame.image.load(os.path.join('images', 'fog_r_bl_corner.png')), # 28
                            pygame.image.load(os.path.join('images', 'fog_r_tl_corner.png')), # 29
                            ]
        self.wall_images = [pygame.image.load(os.path.join('images', 'gray.png')), # 0 
                            pygame.image.load(os.path.join('images', 'wall_b.png')), # 1
                            pygame.image.load(os.path.join('images', 'wall_b_l.png')), # 2
                            pygame.image.load(os.path.join('images', 'wall_b_l_r.png')), # 3
                            pygame.image.load(os.path.join('images', 'wall_b_r.png')), # 4
                            pygame.image.load(os.path.join('images', 'wall_b_t_l.png')), # 5
                            pygame.image.load(os.path.join('images', 'wall_b_t_r.png')), # 6
                            pygame.image.load(os.path.join('images', 'wall_l.png')), # 7
                            pygame.image.load(os.path.join('images', 'wall_l_r.png')), # 8
                            pygame.image.load(os.path.join('images', 'wall_r.png')), # 9
                            pygame.image.load(os.path.join('images', 'wall_t.png')), # 10
                            pygame.image.load(os.path.join('images', 'wall_t_b.png')), # 11
                            pygame.image.load(os.path.join('images', 'wall_t_l.png')), # 12 
                            pygame.image.load(os.path.join('images', 'wall_t_l_r.png')), # 13
                            pygame.image.load(os.path.join('images', 'wall_t_r.png')), # 14
                            pygame.image.load(os.path.join('images', 'wall_t_l_corner.png')), # 15
                            pygame.image.load(os.path.join('images', 'wall_t_r_corner.png')), # 16
                            pygame.image.load(os.path.join('images', 'wall_b_l_corner.png')), # 17
                            pygame.image.load(os.path.join('images', 'wall_b_r_corner.png')), # 18
                            pygame.image.load(os.path.join('images', 'wall_b_tl_corner.png')), # 19
                            pygame.image.load(os.path.join('images', 'wall_b_tr_corner.png')), # 20
                            pygame.image.load(os.path.join('images', 'wall_b_tl_tr_corner.png')), # 21
                            pygame.image.load(os.path.join('images', 'wall_t_bl_corner.png')), # 22
                            pygame.image.load(os.path.join('images', 'wall_t_br_corner.png')), # 23
                            pygame.image.load(os.path.join('images', 'wall_t_bl_br_corner.png')), # 24
                            pygame.image.load(os.path.join('images', 'wall_pillar.png')), # 25
                            pygame.image.load(os.path.join('images', 'wall_l_br_corner.png')), # 26
                            pygame.image.load(os.path.join('images', 'wall_l_tr_corner.png')), # 27
                            pygame.image.load(os.path.join('images', 'wall_r_bl_corner.png')), # 28
                            pygame.image.load(os.path.join('images', 'wall_r_tl_corner.png')), # 29
                           ]
        self.images = [pygame.image.load(os.path.join('images',"grass.png")), 
                       pygame.image.load(os.path.join('images',"wall.png")), 
                       pygame.image.load(os.path.join('images',"water.png")), 
                       pygame.image.load(os.path.join('images',"dig.png")), 
                       pygame.image.load(os.path.join('images',"grass4.png"))]
        self.dead_images = [pygame.image.load(os.path.join('images', "deddorf.png"))]
        pygame.init()
        self.stats = Stats(250, 250)
        #setup the default screen size
        if self.fullscreen == True: # check the config file for fullscreen options
            self.screen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.window_width, self.window_height), RESIZABLE)
        pygame.display.set_caption('SPACEBAR to advance a turn')
        self.mouse_box = False
        self.mouse_box_rect = pygame.Rect((0, 0), (TILE_WIDTH, TILE_WIDTH))
        self.mainclock = pygame.time.Clock()
        # various rendering offsets
        self.vp_render_offset = (TILE_WIDTH, TILE_WIDTH)
        self.stats_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH)
        self.click_state_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 2)
        self.stat_box_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 5)
        self.view_port_coord = [0, 0] # Starting coordinates for the view port
        self.vp_dimensions = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.char_box_top = math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH  # rectangle for the char box
        self.char_box_left = 0
        self.char_box_width = math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH
        self.char_box_height = math.floor(int(0.2 * self.window_height) / TILE_WIDTH) * TILE_WIDTH
        self.combat_log_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = self.window_width - self.combat_log_offset[0]
        self.combat_log_height = self.window_height - self.combat_log_offset[1] 
        self.app = gui.App(theme=TestTheme())
        self.combat_log = CombatLog("", self.combat_log_width, self.combat_log_height)
        self.log = []
        self.log.append("Welcome to the game")
        self.end_turn_button = gui.Button("End Turn")
        self.end_turn_button.connect(gui.CLICK, self.advance_turn)
        self.end_turn_button_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.z_up_button = gui.Button("+")
        self.z_up_button.connect(gui.CLICK, self.button_click_z_up)
        self.z_down_button = gui.Button("-")
        self.z_down_button.connect(gui.CLICK, self.button_click_z_down)
        self.up_button = gui.Button("^")
        self.up_button.connect(gui.CLICK, self.button_click_up)
        self.down_button = gui.Button("v")
        self.down_button.connect(gui.CLICK, self.button_click_down)
        self.left_button = gui.Button("<")
        self.left_button.connect(gui.CLICK, self.button_click_left)
        self.right_button = gui.Button(">")
        self.right_button.connect(gui.CLICK, self.button_click_right)
        self.z_up_button_offset = (math.floor(int(0.5 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.z_down_button_offset = (math.floor(int(0.6 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.up_button_offset = (math.floor(int(0.4 * self.window_width) / TILE_WIDTH) * TILE_WIDTH , TILE_WIDTH / 4)
        self.down_button_offset = (math.floor(int(0.4 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.left_button_offset = (TILE_WIDTH / 8, math.floor(int(0.4 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.right_button_offset = (self.combat_log_offset[0], math.floor(int(0.4 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.gui_container.add(self.z_up_button, self.z_up_button_offset[0], self.z_up_button_offset[1])
        self.gui_container.add(self.z_down_button, self.z_down_button_offset[0], self.z_down_button_offset[1])
        self.gui_container.add(self.up_button, self.up_button_offset[0], self.up_button_offset[1])
        self.gui_container.add(self.down_button, self.down_button_offset[0], self.down_button_offset[1])
        self.gui_container.add(self.left_button, self.left_button_offset[0], self.left_button_offset[1])
        self.gui_container.add(self.right_button, self.right_button_offset[0], self.right_button_offset[1])
        self.gui_container.add(self.end_turn_button, self.end_turn_button_offset[0], self.end_turn_button_offset[1] )
        self.app.init(self.gui_container)
        self.view_port_step = TILE_WIDTH # move 1 tile over.
        self.view_port_shift_step = TILE_WIDTH * 10 # move 10 tile over.
        self.min_h_scroll_bound = 0
        self.min_v_scroll_bound = 0
        self.max_h_scroll_bound = self.mapw * TILE_WIDTH
        self.max_v_scroll_bound = self.maph * TILE_WIDTH
        self.num_x_tiles = int(math.ceil(int(self.vp_dimensions[0]) / TILE_WIDTH)) # the number of tiles to be shown at one time for X
        self.num_y_tiles = int(math.ceil(int(self.vp_dimensions[1]) / TILE_WIDTH)) # the number of tiles to be shown at one time for y
        self.start_x_tile = math.floor(int(self.view_port_coord[0]) / TILE_WIDTH)
        self.start_y_tile = math.floor(int(self.view_port_coord[1]) / TILE_WIDTH)
        self.selected_player = None
        self.selected_mob = None
        self.dead_mobs = []
        self.dead_players = []
        self.view_port = Set()
        if not pygame.font.get_init():
            pygame.font.init()
        self.arial_font = pygame.font.SysFont('Arial', 16)
        self.zlevels = 5
        self.mapdata = [[[ MapTile(1) for cols in range(self.maph)] for rows in range(self.mapw)] for z in range(self.zlevels)] #IGNORE:W0612         
        self.clickdata = [[[ 0 for cols in range(self.maph)] for rows in range(self.mapw)] for z in range(self.zlevels)] #          
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.players = []
        self.mobs = []
        self.cursors = Cursors()

    def advance_turn(self):
        """ Advance one turn in game time """
        # process the players moves
        self.turn = self.turn + 1
        self.log.append("Advancing to turn " + str(self.turn))
        self.combat()
        self.remove_dead_stuff()
        self.player_movement()
        # mob movement
        self.mob_movement()
    
    def button_click_z_up(self):
        """ + button was clicked to go up a zlevel """
        self.current_z = self.current_z + 1
        
    def button_click_z_down(self):
        """ - button was clicked to go down a zlevel """
        self.current_z = self.current_z - 1
    
    def button_click_up(self):
        """ ^ button clicked to move the viewport up """
        self.view_port_coord[1] = self.view_port_coord[1] - self.view_port_shift_step
        
    def button_click_down(self):
        """ v button clicked to move the viewport down """
        self.view_port_coord[1] = self.view_port_coord[1] + self.view_port_shift_step
        
    def button_click_left(self):
        """ < button clicked to move the viewport left """
        self.view_port_coord[0] = self.view_port_coord[0] - self.view_port_shift_step
        
    def button_click_right(self):
        """ > button clicked to move the viewport right """
        self.view_port_coord[0] = self.view_port_coord[0] + self.view_port_shift_step
    
    def center_vp_on(self, x, y, z):
        """ Center the view port onto the coords x, y, z """
        center_x, center_y = self.get_center_of_vp()
        offset_x = center_x * -TILE_WIDTH
        offset_y = center_y * -TILE_WIDTH
        self.view_port_coord[0] = offset_x + x * TILE_WIDTH 
        self.view_port_coord[1] = offset_y + y * TILE_WIDTH
        self.current_z = z
        return
        
    def center_vp_on_player(self):
        """ Center the viewport on the player """
        for p in self.players:
            x, y, z = p.x, p.y, p.z
            center_x, center_y = self.get_center_of_vp()
            offset_x = center_x * -TILE_WIDTH
            offset_y = center_y * -TILE_WIDTH
            self.view_port_coord[0] = offset_x + x * TILE_WIDTH 
            self.view_port_coord[1] = offset_y + y * TILE_WIDTH
            self.current_z = z
            return
    
    def compute_path(self, start, end):
        """ Return the individual steps of a path in a list between two points """
        pf = PathFinder(self.successors, move_cost, move_cost)
        pathlines = list(pf.compute_path(start, end))
        return pathlines
    
    def compute_path_mob(self, start, end):
        """ Return the individual steps of a path in a list between two points, ignoring fog tiles for monsters. """
        pf = PathFinder(self.successors_for_mobs, move_cost, move_cost)
        pathlines = list(pf.compute_path(start, end))
        return pathlines
                
    def click_in_viewport(self, x, y):
        """ Is the mouse click in the viewport? """
        if x < self.num_x_tiles * TILE_WIDTH + self.vp_render_offset[0] and x > self.vp_render_offset[0] and y < self.num_y_tiles * TILE_WIDTH + self.vp_render_offset[1] and y > self.vp_render_offset[1]: #within the map viewport
            return True
        else:
            return False
    
    def check_player_portrait_clicks(self, mx, my):
        """ Was the click in on the portrait """
        uuid = ""
        for p in self.players:
            if p.pressed_portrait(mx, my):
                uuid = p.uuid
                self.center_vp_on(p.x, p.y, p.z)
                self.selected_player = p.uuid
                self.click_state = "MoveSelect"
        for p in self.players:
            if uuid == p.uuid:
                p.selected = True
            else:
                p.selected = False
        if uuid is not "":
            return True        
        return False
    
    def check_mob_portrait_clicks(self, mx, my):
        """ Was the click on the portrait? """
        uuid = ""
        for m in self.mobs:
            if m.pressed_portrait(mx, my):
                uuid = m.uuid
                self.center_vp_on(m.x, m.y, m.z)
                self.selected_mob = m.uuid
                
        for m in self.players:
            if uuid == m.uuid:
                m.selected = True
            else:
                m.selected = False
        if uuid is not "":
            return True        
        return False
    
    def check_map_for_player(self, x, y, z):
        """ check a map location for players, and flag them as selected """
        uuid = ""
        for p in self.players:
            if p.x == x and p.y == y and p.z == z:
                uuid = p.uuid
            
        for p in self.players:
            if p.uuid == uuid:
                p.selected = True
            else:
                p.selected = False
                
        if uuid is not "":
            return uuid
        return None
     
    def check_map_for_mob(self, x, y, z):
        """ check the map location for a monster and flag it as selected """
        for m in self.mobs:
            if m.x == x and m.y == y and m.z == z:
                m.selected = True
                return m.uuid
        return None
    
    def create_room(self, room, z):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.mapdata[z][x][y].blocked = False
                self.mapdata[z][x][y].block_sight = False
     
    def create_h_tunnel(self, x1, x2, y, z):
        #horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.mapdata[z][x][y].blocked = False
            self.mapdata[z][x][y].block_sight = False
 
    def create_v_tunnel(self, y1, y2, x, z):
        #vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.mapdata[z][x][y].blocked = False
            self.mapdata[z][x][y].block_sight = False
            
    def check_mob_collision(self, x, y, z, xx, yy, zz): # mob coords, player coords
        """ checks the adjacent tiles of a monster for the presence of a player  """
        area = self.successors_and_center(xx, yy, zz)
        for a in area:
            if a == (x, y, z):
                return True
        return False
                    
    def check_map(self, x, y, zlevel):
        """ returns the mapdata value for the coords """
        return self.mapdata[zlevel][int(x)][int(y)].value
    
    def check_click_map(self, x, y, z):
        """ checks the click map """
        return self.mapdata[z][int(x)][int(y)]
    
    def combat(self):
        """ initiate combat """
        combat_list = []
        for m in self.mobs:
            for p in self.players:
                if is_in_fov(m, p):
                    if self.check_mob_collision(m.x, m.y, m.z, p.x, p.y, p.z):
                        p.pathlines = []
                        m.pathlines = []
                        combat_list.append((p.uuid, m.uuid))
                        # clear paths so they don't move around for combat.
                    else:
                        if m.pathlines:
                            if len(m.pathlines) < 2:
                                start = (m.x, m.y, m.z) # start position
                                end = (p.x, p.y, p.z)
                                templist = self.compute_path_mob(start, end)   
                                if templist:
                                    m.pathlines = templist
                            else:
                                pass
                        else:
                            # pick a player to go after.
                            start = (m.x, m.y, m.z) # start position
                            end = (p.x, p.y, p.z)
                            templist = self.compute_path_mob(start, end)   
                            if templist:
                                m.pathlines = templist
        
        # Combat 
        for (player, monster) in combat_list:
            p = self.lookup_player_by_uuid(player)
            m = self.lookup_mob_by_uuid(monster)
            if p == None or m == None:
                continue 
            self.log.append("Combat Started Rolling Initiative:")
            # add the initiative bonus at some point
            player_initiative = roll_d_20()
            mob_initiative = roll_d_20()
            
            if player_initiative >= mob_initiative:
                #player won init
                #chance to hit
                player_roll = roll_d_20()
                to_log = p.name + " rolled a " + str(player_roll) + " +" + str(p.get_attack_bonus())
                self.log.append(to_log)
                player_chance_to_hit = player_roll + p.get_attack_bonus()
                if player_roll == 1:
                    to_log = p.name + " critically misses " + m.name + "!"
                    self.log.append(to_log)
                    #critical miss
                elif player_chance_to_hit > m.get_defense_bonus() or player_roll == 20:
                    #hit
                    damage = roll_damage(p.job.damage) + p.get_attack_bonus()
                    if player_roll == 20:
                        #crit
                        to_log = p.name + " scored a critical hit on " + m.name + "!"
                        self.log.append(to_log)
                        damage = damage * 2 # crit mutliplier won't be hard coded at some point
                    if m.take_damage(damage): 
                        #monster still has hp left after the hit
                        to_log = m.name + " takes " + str(damage) + " from " + p.name + "!"
                        self.log.append(to_log)
                        mob_roll = roll_d_20()
                        mob_hit_chance = mob_roll + m.get_level()
                        to_log = m.name + " tries to counter-attack with a roll of " + str(mob_roll) + " +" + str(m.get_level())
                        self.log.append(to_log)
                        if mob_roll == 1:
                            to_log = m.name + " critically misses " + p.name + "!"
                            self.log.append(to_log)
                            #crit miss
                            
                        elif mob_hit_chance > p.get_defense_bonus() or mob_roll == 20:
                            #hit
                            damage = roll_damage(m.job.damage) + m.get_attack_bonus()
                            if mob_roll == 20:
                                #crit
                                to_log = m.name + " scored a critical hit on " + p.name + "!"
                                self.log.append(to_log)
                                damage = damage * 2 # crit mult
                            if p.take_damage  (damage):
                                to_log = p.name + " takes " + str(damage) + " from " + m.name + "'s attack!"
                                self.log.append(to_log)
                                #player still alive
                            else:
                                #player dead
                                to_log = p.name + " takes " + str(damage) + " from " + m.name + "'s attack and dies!"
                                self.log.append(to_log)
                                p.alive = False
                        else:
                            #Miss
                            to_log = m.name + " misses " + p.name + "."
                            self.log.append(to_log)
                            
                    else:
                        #monsters dead
                        to_log = m.name + " takes " + str(damage) + " from " + p.name + "'s attack and dies!"
                        self.log.append(to_log)
                        to_log = p.name + " gained: " + str(m.experience) + " xp!"
                        self.log.append(to_log)
                        p.gain_xp(m.experience)
                        m.alive = False
                else:
                    #miss
                    to_log = p.name + " misses " + m.name + "."
                    self.log.append(to_log)
            else:
                #monster won init
                #player won init
                #chance to hit
                monster_roll = roll_d_20()
                to_log = m.name + " rolled a " + str(monster_roll) + " +" + str(m.get_level())
                self.log.append(to_log)
                monster_chance_to_hit = monster_roll + m.get_level()
                if monster_roll == 1:
                    to_log = m.name + " critically misses " + p.name + "!"
                    self.log.append(to_log)
                    #critical miss
                elif monster_chance_to_hit > p.get_defense_bonus() or monster_roll == 20:
                    #hit
                    damage = roll_damage(m.job.damage) + m.get_attack_bonus()
                    if monster_roll == 20:
                        #crit
                        to_log = m.name + " scored a critical hit on " + p.name + "!"
                        self.log.append(to_log)
                        damage = damage * 2 # crit mutliplier won't be hard coded at some point
                    if p.take_damage(damage): 
                        #player still has hp left after the hit
                        to_log = p.name + " takes " + str(damage) + " from " + m.name + "!"
                        self.log.append(to_log)
                        player_roll = roll_d_20()
                        player_hit_chance = player_roll + p.get_attack_bonus()
                        to_log = p.name + " tries to counter-attack with a roll of " + str(player_roll) + " +" + str(p.get_attack_bonus())
                        self.log.append(to_log)
                        if player_roll == 1:
                            to_log = p.name + " critically misses " + m.name + "!"
                            self.log.append(to_log)
                            #crit miss
                            
                        elif player_hit_chance > m.get_defense_bonus() or player_roll == 20:
                            #hit
                            damage = roll_damage(p.job.damage) + p.get_attack_bonus()
                            if player_roll == 20:
                                #crit
                                to_log = p.name + " scored a critical hit on " + m.name + "!"
                                self.log.append(to_log)
                                damage = damage * 2 # crit mult
                            if m.take_damage  (damage):
                                to_log = m.name + " takes " + str(damage) + " from " + p.name + "'s attack!"
                                self.log.append(to_log)
                                #mob still alive
                            else:
                                #mob dead
                                to_log = m.name + " takes " + str(damage) + " from " + p.name + "'s attack and dies!"
                                self.log.append(to_log)
                                to_log = p.name + " gained: " + str(m.experience) + " xp!"
                                self.log.append(to_log)
                                p.gain_xp(m.experience)
                                m.alive = False
                        else:
                            #Miss
                            to_log = p.name + " misses " + m.name + "."
                            self.log.append(to_log)
                            
                    else:
                        #players dead
                        to_log = p.name + " takes " + str(damage) + " from " + m.name + "'s attack and dies!"
                        self.log.append(to_log)
                        p.alive = False
                else:
                    #miss
                    to_log = m.name + " misses " + p.name + "."
                    self.log.append(to_log)
                    
    def remove_dead_stuff(self):
        """ remove dead players / monsters from their respective lists """    
        for p in self.players[:]:
            if p.alive:
                #alive check
                pass
            else:
                self.dead_players.append((p.x, p.y, p.z))
                self.players.remove(p)
                
        for m in self.mobs[:]:
            if m.alive:
                #mobs alive
                pass
            else:
                self.dead_mobs.append(m)
                self.mobs.remove(m)
            
    def draw_stats(self):
        """ Draw the stats window """
        if self.selected_player != None:
            p = self.lookup_player_by_uuid(self.selected_player)
            self.stats.update_stats(p)
            self.screen.blit(self.stats, self.stat_box_offset)
            return
        elif self.selected_mob != None:
            m = self.lookup_mob_by_uuid(self.selected_mob)
            self.stats.update_stats(m)
            self.screen.blit(self.stats, self.stat_box_offset)
        
    def draw_players_and_mobs(self):
        """ draws the players and monsters if they are within the viewport """
        for p in self.players:
            if (p.x, p.y, p.z) in self.view_port:
                self.screen.blit(p.image, self.vp_render_offset, (self.view_port_coord[0] - (p.x * TILE_WIDTH), (self.view_port_coord[1] - (p.y * TILE_WIDTH))) + self.vp_dimensions)
                self.screen.blit(self.arial_font.render(str(p.hp), True, (255, 0, 0)), ((p.x - self.start_x_tile) * TILE_WIDTH + TILE_WIDTH, (p.y - self.start_y_tile) * TILE_WIDTH + TILE_WIDTH) )
                if p.selected :
                    green = (0, 255, 0)
                    rect = pygame.Rect(((p.x * TILE_WIDTH) - self.view_port_coord[0]) + TILE_WIDTH, ((p.y * TILE_WIDTH) - self.view_port_coord[1]) + TILE_WIDTH , TILE_WIDTH, TILE_WIDTH)
                    pygame.draw.rect(self.screen, green, rect, 3)
        for m in self.mobs:
            if (m.x, m.y, m.z) in self.view_port and self.is_foggy(m.x, m.y, m.z) == False:
                self.screen.blit(self.arial_font.render(str(m.hp), True, (255, 0, 0)), ((m.x - self.start_x_tile) * TILE_WIDTH + TILE_WIDTH, (m.y - self.start_y_tile) * TILE_WIDTH + TILE_WIDTH) )
                self.screen.blit(m.image, self.vp_render_offset, (self.view_port_coord[0] - (m.x * TILE_WIDTH), (self.view_port_coord[1] - (m.y * TILE_WIDTH))) + self.vp_dimensions)
                if m.selected :
                    red = (255, 0, 0)
                    rect = pygame.Rect(((m.x * TILE_WIDTH) - self.view_port_coord[0]) + TILE_WIDTH, ((m.y * TILE_WIDTH) - self.view_port_coord[1]) + TILE_WIDTH , TILE_WIDTH, TILE_WIDTH)
                    pygame.draw.rect(self.screen, red, rect, 3)
        for (x, y, z) in self.dead_players:
            if (x, y, z) in self.view_port:
                self.screen.blit(self.dead_images[0], self.vp_render_offset, (self.view_port_coord[0] - (x * TILE_WIDTH), (self.view_port_coord[1] - (y * TILE_WIDTH))) + self.vp_dimensions)
        for m in self.dead_mobs:
            if (m.x, m.y, m.z) in self.view_port:
                self.screen.blit(m.dead_image, self.vp_render_offset, (self.view_port_coord[0] - (m.x * TILE_WIDTH), (self.view_port_coord[1] - (m.y * TILE_WIDTH))) + self.vp_dimensions)
    
    def draw_map(self):
        """ draws the portion of the map thats in the viewport onto the screen """
        for x in range(self.mapw):
            for y in range(self.maph):
                if (x, y, self.current_z) in self.view_port:
                    if self.is_foggy(x, y, self.current_z): # fog
                        templist = self.get_fog_neighbors_values(x, y, self.current_z)
                        value = pick_wall_tile(templist)
                        self.tiled_bg.blit(self.fog_images[value], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
                    elif self.mapdata[self.current_z][x][y].blocked: # wall
                        templist = self.get_neighbors_values(x, y, self.current_z)
                        value = pick_wall_tile(templist)
                        self.tiled_bg.blit(self.wall_images[value], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
                    else: # floor
                        self.tiled_bg.blit(self.floor_images[0], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
                #draw items on the tiles
                for item in self.mapdata[self.current_z][x][y].content:
                    if self.is_foggy(x, y, self.current_z):
                        # tile is foggy don't draw items
                        pass
                    else:
                        self.tiled_bg.blit(item.image, ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))

    def draw_click_map(self):
        """ draw the click map, used for debugging """
        for x in range(self.mapw):
            for y in range(self.maph):
                if (x, y, self.current_z) in self.view_port:
                    if self.clickdata[self.current_z][x][y] != 0:
                        self.tiled_bg.blit(self.images[self.clickdata[self.current_z][x][y]], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))

    def draw_path_lines(self):
        """ Draw the players pathes using their colors """
        rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_WIDTH)
        line_width = 5
        for p in self.players:
            if p.pathlines:
                for l in p.pathlines:
                    for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
                        for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
                            if l[0] == x and l[1] == y and l[2] == self.current_z:
                                rect.topleft = ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH)
                                pygame.draw.rect(self.tiled_bg, p.color, rect, line_width)
            line_width = line_width - 1

    def draw_char_box(self):
        """ draw the box at the bottom with the char / mob portraits """ 
        rectangle = pygame.Rect(int(self.char_box_left + TILE_WIDTH), int(self.char_box_top + TILE_WIDTH), int(self.char_box_width), int(self.char_box_height))
        gray = (115, 115, 115)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        self.screen.fill(gray, rectangle)
        count = 0
        for p in self.players:
            p.portrait_rect.topleft = rectangle.topleft
            p.portrait_rect.left = p.portrait_rect.left + p.portrait_rect.width * count#(p.portrait_rect.width * count, ry )
            self.screen.blit(p.portrait, p.portrait_rect ) 
            self.screen.blit(self.arial_font.render(str(count+1), True, white), p.portrait_rect.topleft  )
            self.screen.blit(self.arial_font.render("HP: " + str(p.hp), True, white), (p.portrait_rect.left, p.portrait_rect.centery)  )
            if p.selected == True:
                pygame.draw.rect(self.screen, green, p.portrait_rect, 5)
            count = count + 1
        count = 0
        for m in self.mobs:
            if m.z == self.current_z:
                if self.is_foggy(m.x, m.y, m.z) == False:
                    m.portrait_rect.topleft = rectangle.topleft
                    m.portrait_rect.top = m.portrait_rect.top + m.portrait_rect.height
                    m.portrait_rect.left = m.portrait_rect.left + m.portrait_rect.width * count#(p.portrait_rect.width * count, ry )
                    self.screen.blit(m.portrait, m.portrait_rect ) # 
                    self.screen.blit(self.arial_font.render("HP: " + str(m.hp), True, white), (m.portrait_rect.left, m.portrait_rect.centery)  )
                    if m.selected == True:
                        pygame.draw.rect(self.screen, red, m.portrait_rect, 5)
                    count = count + 1
            
    def draw_possible_moves(self):
        """ draw's all the possible moves """
        for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
            for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
                if (x, y, self.current_z) in self.moves:
                    self.tiled_bg.blit(self.images[3], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
    
    def draw_mouse_box(self):
        """ Draw the box that follows the mouse around in the viewport """
        blue = (0, 0, 255)
        if self.mouse_box == True:
            pygame.draw.rect(self.screen, blue, self.mouse_box_rect, 3)
            
    def find_up_stairs_on(self, z):
        """ return the location of some up stairs on a given zlevel """
        for x in range(self.mapw):
            for y in range(self.maph):
                for i in self.mapdata[z][x][y].content:
                    if i.name == "StairsUp":
                        return (x, y, z)
        return None

    def find_down_stairs_on(self, z):
        """ returns the location of some downstairs given a zlevel"""
        for x in range(self.mapw):
            for y in range(self.maph):
                for i in self.mapdata[z][x][y].content:
                    if i.name == "StairsDown":
                        return (x, y, z)
        return None

    def get_possible_moves(self, x, y, z):
        """ return a list of all the possible moves for a particular coord """
        successors_list = self.find_moves(x, y, z, 2)
        new_set = Set()
        new_set.update(successors_list)
        return new_set 
    
    def get_center_of_vp(self):
        """ return the center of the viewport """
        return self.num_x_tiles /2, self.num_y_tiles /2
    
    def get_fog_neighbors_values(self, x, y, z):
        """ check if its foggy near the given coord, used to pick which tiles to display on fog bordering unfogged locations"""
        templist = [[ 0 for i in range(3)] for j in range(3)]  #IGNORE:W0612
        xx = 0
        for drow in (-1, 0, 1):
            yy = 0
            for dcol in (-1, 0, 1):
                newrow = x + drow
                newcol = y + dcol
                if (newrow, newcol, z) in self.view_port:
                    if drow == 0 and dcol == 0:
                        #print "center"
                        pass
                    elif newrow > self.mapw - 1:
                        pass
                    elif newcol > self.maph - 1:
                        pass
                    elif self.is_foggy(newrow, newcol, z):
                        #print "Blocked or foggy"
                        pass
                    else:
                        #print "Floor"
                        templist[xx][yy] = 1
                yy = yy + 1
            xx = xx + 1
        return templist
    
    def get_tile_items(self, x, y, z):
        """ get list of items on a particular tile """
        return self.mapdata[z][x][y].content
    
    def get_neighbors_values(self, x, y, z):
        """ return a list of the adjacent tiles values """
        templist = [[ 0 for i in range(3)] for j in range(3)]  #IGNORE:W0612
        xx = 0
        for drow in (-1, 0, 1):
            yy = 0
            for dcol in (-1, 0, 1):
                newrow = x + drow
                newcol = y + dcol
                if (newrow, newcol, z) in self.view_port:
                    if drow == 0 and dcol == 0:
                        #print "center"
                        pass
                    elif newrow > self.mapw - 1:
                        pass
                    elif newcol > self.maph - 1:
                        pass
                    elif self.is_blocked(newrow, newcol, z) or self.is_foggy(newrow, newcol, z):
                        #print "Blocked or foggy"
                        pass
                    else:
                        #print "Floor"
                        templist[xx][yy] = 1
                yy = yy + 1
            xx = xx + 1
        return templist

    def get_open_spot_around(self, x, y, z):
        """ get the first open spot around the coords provided """
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                newrow = x + drow
                newcol = y + dcol
                if drow == 0 and dcol == 0:
                    #print "center"
                    continue
                elif self.is_blocked(newrow, newcol, z):
                    #print "Blocked or foggy"
                    continue
                else:
                    #print "Floor"
                    return (newrow, newcol, z)
        return None
    
    def get_open_spots_around(self, x, y, z):
        """ get a list of the open spots around a given coord """
        temp_list = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                newrow = x + drow
                newcol = y + dcol
                if drow == 0 and dcol == 0:
                    #print "center"
                    continue
                elif self.is_blocked(newrow, newcol, z):
                    #print "Blocked or foggy"
                    continue
                else:
                    #print "Floor"
                    temp_list.append((newrow, newcol, z))
        return temp_list
        
    def handle_viewport(self):
        """ manage the viewport v / h scroll bounds """
        # view port reset, don't scroll past the h / v bounds
        if self.view_port_coord[0] < 0:
            self.view_port_coord[0] = 0
        if self.view_port_coord[0] + self.vp_dimensions[0] > self.max_h_scroll_bound:
            self.view_port_coord[0] = self.max_h_scroll_bound - self.vp_dimensions[0]
        if self.view_port_coord[1] < 0:
            self.view_port_coord[1] = 0
        if self.view_port_coord[1] + self.vp_dimensions[1] > self.max_v_scroll_bound:
            self.view_port_coord[1] = self.max_v_scroll_bound - self.vp_dimensions[1]
        if self.current_z >= self.zlevels:
            self.current_z = self.zlevels -1
        if self.current_z <= 0:
            self.current_z = 0
        self.recalc_vp()
    
    def handle_fog_of_war(self):
        """ unfog tiles around the players within their view ranges """
        for p in self.players:
            for (x, y, z) in p.fov:
                self.un_fog(x, y, z)
    
    def handle_events(self):
        """ run through the pygame events and give them to the proper functions """
        for event in pygame.event.get():
            self.app.event(event)
            if event.type == QUIT:
                self.running = False
                return
            elif event.type == KEYDOWN:
                self.handle_keyboard(event)
                
            elif event.type == MOUSEMOTION:
                self.motion = event
                mx = self.motion.pos[0]
                my = self.motion.pos[1]
                if self.click_in_viewport(mx, my):
                    x, y, z = self.view_port_click_to_coords(mx, my, self.current_z)
                    if self.mouse_box == True and self.click_state == "MoveSelect":
                        self.mouse_box_rect.topleft = ((x - self.start_x_tile) * TILE_WIDTH + TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH + TILE_WIDTH)
                if self.click_state == "MoveSelect":
                    self.mouse_box = True
                else: 
                    self.mouse_box = False
            elif event.type == MOUSEBUTTONUP:
                self.buttons[event.button] = event.pos
                if 1 in self.buttons: # left click
                    mx = self.motion.pos[0]
                    my = self.motion.pos[1]
                    if self.click_in_viewport(mx, my) and self.click_state == "MoveSelect":
                        x, y, z = self.view_port_click_to_coords(mx, my, self.current_z)
                        self.pick_dest(x, y, z)
                        self.click_state = None
                        self.selected_player = None
                    elif self.click_in_viewport(mx, my):
                        x, y, z = self.view_port_click_to_coords(mx, my, self.current_z)
                        player_uuid = self.check_map_for_player(x, y, z)
                        mob_uuid = self.check_map_for_mob(x, y, z)
                        if player_uuid:
                            self.center_vp_on(x, y, z)
                            self.selected_player = player_uuid
                            self.click_state = "MoveSelect"
                        elif mob_uuid:
                            self.center_vp_on(x, y, z)
                            self.selected_mob = mob_uuid
                            # Add a panel that will show the mob details / stats
                            self.update_clicked_mob()
                    elif self.check_player_portrait_clicks(mx, my):
                        pass
                    elif self.check_mob_portrait_clicks(mx, my):
                        pass
                elif 3 in self.buttons: # right click
                    mx = self.motion.pos[0]
                    my = self.motion.pos[1]
                    if self.click_in_viewport(mx, my):
                        x, y, z = self.view_port_click_to_coords(mx, my, self.current_z)
                        self.check_map(x, y, z)
                        self.update_click_map(x, y, z, 0)
                
                self.buttons = {}
            elif event.type == MOUSEBUTTONDOWN:
                self.app.event(event)
            elif event.type == VIDEORESIZE:
                # allow for the window to be resized manually.
                w, h = event.w, event.h
                self.screen_resize(w, h)
            # send the events to the gui
            #self.app.event(event)
            
    def handle_win_condition(self):
        """ basic win condition """
        if len(self.mobs) == 0:
            self.win = True
        elif len(self.players) == 0:
            self.win = False
        else:
            self.win = None
        
    def handle_mouse_cursor(self):
        """ handle mouse actions """
        if self.click_state == "MoveSelect":
            size, hotspot, cursor, mask = make_cursor(self.cursors.move)
            pygame.mouse.set_cursor(size, hotspot, cursor, mask)
        else:
            size, hotspot, cursor, mask = make_cursor(self.cursors.arrow)
            pygame.mouse.set_cursor(size, hotspot, cursor, mask)
    
    def handle_keyboard(self, event):
        """ handle the keyboard events """
        keymods = pygame.key.get_mods()
        if event.key == K_ESCAPE:
            if self.player_info:
                self.PI.close
                self.player_info = False
            else:
                self.show_quit_diag = True 
            
        #View port Movement        
        elif event.key == K_1:
            if len(self.players) >= 1:
                self.selected_player = self.players[0].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_2:
            if len(self.players) >= 2:
                self.selected_player = self.players[1].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_3:
            if len(self.players) >= 3:
                self.selected_player = self.players[2].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_4:
            if len(self.players) >= 4:
                self.selected_player = self.players[3].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_5:
            if len(self.players) >= 5:
                self.selected_player = self.players[4].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_6:
            if len(self.players) >= 6:
                self.selected_player = self.players[5].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_7:
            if len(self.players) >= 7:
                self.selected_player = self.players[6].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_8:
            if len(self.players) >= 8:
                self.selected_player = self.players[7].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_9:
            if len(self.players) >= 9:
                self.selected_player = self.players[8].uuid
                p = self.lookup_player_by_uuid(self.selected_player)
                self.center_vp_on(p.x, p.y, p.z)
                self.click_state = "MoveSelect"
                for p in self.players:
                    if self.selected_player == p.uuid:
                        p.selected = True
                    else:
                        p.selected = False
        elif event.key == K_i: # i for inventory
            if self.selected_player:
                self.show_inventory = True
        elif event.key == K_c: # i for inventory
            if self.selected_player:
                self.player_info = True
                
        elif event.key == K_LEFT:
            if keymods & pygame.KMOD_LSHIFT:
                self.view_port_coord[0] = self.view_port_coord[0] - self.view_port_shift_step
            else:
                self.view_port_coord[0] = self.view_port_coord[0] - self.view_port_step
        elif event.key == K_RIGHT:
            if keymods & pygame.KMOD_LSHIFT:
                self.view_port_coord[0] = self.view_port_coord[0] + self.view_port_shift_step
            else:
                self.view_port_coord[0] = self.view_port_coord[0] + self.view_port_step
        elif event.key == K_UP:
            if keymods & pygame.KMOD_LSHIFT:
                self.view_port_coord[1] = self.view_port_coord[1] - self.view_port_shift_step
            elif keymods & pygame.KMOD_CTRL:
                self.current_z = self.current_z + 1
            else:
                self.view_port_coord[1] = self.view_port_coord[1] - self.view_port_step
        elif event.key == K_DOWN:
            if keymods & pygame.KMOD_LSHIFT:
                self.view_port_coord[1] = self.view_port_coord[1] + self.view_port_shift_step
            elif keymods & pygame.KMOD_CTRL:
                self.current_z = self.current_z - 1
            else:
                self.view_port_coord[1] = self.view_port_coord[1] + self.view_port_step
        elif event.key == K_SPACE:
            self.advance_turn()
        elif event.key == K_F5:
            # save the game
            print "Saving game"
            self.save_game()
        elif event.key == K_F6:
            # load the previous game
            self.load_game()
        #reset viewport 
        elif event.key == K_F11 :
            if self.fullscreen == False:
                self.set_fullscreen()
                self.fullscreen = True
            elif self.fullscreen == True:
                pygame.display.set_mode((self.window_width, self.window_height), RESIZABLE)
                self.set_not_fullscreen()
                self.fullscreen = False

    def is_blocked(self, x, y, z):
        """ check if a tile is blocked """
        return self.mapdata[z][x][y].blocked

    def is_foggy(self, x, y, z):
        """ check if its foggy """
        return self.mapdata[z][x][y].fog
    
    def is_sight_blocked(self, x, y, z):
        """ check if you can see past this block """
        return self.mapdata[z][x][y].blocked_sight

    def in_vp(self, x, y, z):
        """ is the coords given within the viewport set? """
        if (x, y, z) in self.view_port:
            return True
        else:
            return False

    def lookup_player_by_uuid(self, uuid):
        """ lookup a player via uuid, returns the player or None """
        for p in self.players:
            if p.uuid == uuid:
                return p
        return None

    def lookup_mob_by_uuid(self, uuid):
        """ lookup a monster via the uuid, returns the monster or None """
        for m in self.mobs:
            if m.uuid == uuid:
                return m
        return None

    def pick_dest(self, x, y, z):
        """ pick a destination as long as it isn't blocked or foggy """
        if self.is_blocked(int(x), int(y), z) or self.is_foggy(int(x), int(y), z):
            pass
        elif self.selected_player:
            p = self.lookup_player_by_uuid(self.selected_player)
            if p:
                start = (p.x, p.y, p.z) # start position
                end = (x, y, z) #destination
                path = self.compute_path(start, end)
                if path:
                    p.pathlines = path
                    p.selected = False

    def successors_and_center(self, x, y, z):
        """ get a list of the possible moves """
        slist = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                newrow = x + drow
                newcol = y + dcol
                if drow == 0 and dcol == 0:
                    slist.append((newrow, newcol, z))
                    continue 
                if newrow > self.mapw - 1:
                    continue
                if newcol > self.maph - 1:
                    continue
                if (0 <= newrow <= self.mapw - 1 and 0 <= newcol <= self.maph - 1):
                    if self.is_blocked(x, y, z) or self.is_foggy(x, y, z):
                        continue
                    else:
                        slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist

    def successors(self, x, y, z):
        """ get a list of the possible moves """
        slist = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue 
                newrow = x + drow
                newcol = y + dcol
                if newrow > self.mapw - 1:
                    continue
                if newcol > self.maph - 1:
                    continue
                if (0 <= newrow <= self.mapw - 1 and 0 <= newcol <= self.maph - 1):
                    if self.is_blocked(x, y, z) or self.is_foggy(x, y, z):
                        continue
                    else:
                        slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist
    
    def successors_for_mobs(self, x, y, z): #ignores foggy tiles
        """ get a list of the possible moves """
        slist = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue 
                newrow = x + drow
                newcol = y + dcol
                if newrow > self.mapw - 1:
                    continue
                if newcol > self.maph - 1:
                    continue
                if (0 <= newrow <= self.mapw - 1 and 0 <= newcol <= self.maph - 1):
                    if self.is_blocked(x, y, z):
                        continue
                    else:
                        slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist

    def find_moves(self, x, y, z, movement):
        """ find moves within a movement range """
        slist = []
        movement_range = range(-movement, movement+1)
        for drow in movement_range:
            for dcol in movement_range:
                if drow == 0 and dcol == 0:
                    continue 
                newrow = x + drow
                newcol = y + dcol
                if newrow > self.mapw - 1:
                    continue
                if newcol > self.maph - 1:
                    continue
                if (0 <= newrow <= self.mapw - 1 and 0 <= newcol <= self.maph - 1):
                    if self.is_blocked(newrow, newcol, z):
                        pass
                    else:
                        slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist

    def find_fov(self, x, y, z, size):
        """ return a list of spots within a given FOV area """ 
        slist = []
        size_range = range(-size, size+1)
        for drow in size_range:
            for dcol in size_range:
                newrow = x + drow
                newcol = y + dcol
                if newrow > self.mapw - 1:
                    continue
                if newcol > self.maph - 1:
                    continue
                if (0 <= newrow <= self.mapw - 1 and 0 <= newcol <= self.maph - 1):
                    slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist

    def player_movement(self):
        """ handle the player movement, pop a move off their pathlines and move them there """
        for p in self.players:
            if p.pathlines:
                move = p.pathlines.pop(0)
                if (p.x, p.y, p.z) == move:
                    if p.pathlines:
                        move = p.pathlines.pop(0) 
                p.x, p.y, p.z = move
                p.fov.update(self.find_fov(p.x, p.y, p.z, p.get_view_range()))
            #manage players running into items ie: stairs
            item_list = self.get_tile_items(p.x, p.y, p.z)
            for item in item_list:
                if item.name == "StairsUp":
                    # attempt to move the player to the new z level
                    spot = self.find_down_stairs_on(p.z+1)
                    if spot != None:
                        x, y, z = spot 
                    open_spot = self.get_open_spot_around(x, y, z)
                    if open_spot != None:
                        p.x, p.y, p.z = open_spot
                        p.pathlines = []
                        text = p.name + " has walked up some stairs."
                        self.log.append(text)
                        p.fov.update(self.find_fov(p.x, p.y, p.z, p.get_view_range()))
                        self.center_vp_on(p.x, p.y, p.z)
                elif item.name == "StairsDown":
                    # attempt to move the player to the new z level
                    spot = self.find_up_stairs_on(p.z-1)
                    if spot != None:
                        x, y, z = spot 
                        open_spot = self.get_open_spot_around(x, y, z)
                        if open_spot != None:
                            p.x, p.y, p.z = open_spot
                            p.pathlines = []
                            text = p.name + " has walked down some stairs."
                            self.log.append(text)
                            p.fov.update(self.find_fov(p.x, p.y, p.z, p.get_view_range()))
                            self.center_vp_on(p.x, p.y, p.z)
                else:
                    text = p.name + " picks up a " + item.name
                    p.backpack.append(item)
                    self.log.append(text)
                    self.mapdata[p.z][p.x][p.y].content.remove(item)

    def mob_movement(self):
        """ handle mob movement, pops a pathline off and moves them there. """
        for m in self.mobs: #IGNORE:C0103
            if m.pathlines:
                move = m.pathlines.pop(0)
                if (m.x, m.y, m.z) == move:
                    if m.pathlines:
                        move = m.pathlines.pop(0)
                m.x, m.y, m.z = move
            m.fov.update(self.find_fov(m.x, m.y, m.z, m.get_view_range()))
    
    def update_map(self, x, y, z, value):
        """ set a value to the map, not currently used I don't think """
        self.mapdata[z][int(x)][int(y)].value = value
        
    def un_fog(self, x, y, z):
        """ unfog this location """
        if self.mapdata[z][x][y].fog:
            self.mapdata[z][x][y].fog= False

    def update_click_map(self, x, y, z, value):
        """ update the click map with the specified value """
        self.clickdata[z][int(x)][int(y)] = value
        self.moves = self.get_possible_moves(int(x), int(y), z)

    def recalc_vp(self):
        """ recalculate the viewport if the screen moved around """
        vpset = Set()
        for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
            for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
                vpset.add((x, y, self.current_z))
        self.view_port = vpset

    def set_not_fullscreen(self):
        """ gets called when we revert back from fullscreen mode """
        newwidth = math.floor(int(0.8 * self.window_width) / TILE_WIDTH)
        newheight = math.floor(int(0.8 * self.window_height) / TILE_WIDTH)
        self.stats_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH)
        self.click_state_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 2)
        self.stat_box_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 5)
        self.vp_dimensions = (newwidth * TILE_WIDTH, newheight * TILE_WIDTH) # resolution of the view port
        self.num_x_tiles = int(math.ceil(int(self.vp_dimensions[0]) / TILE_WIDTH)) # tiles to be shown at one time for X
        self.num_y_tiles = int(math.ceil(int(self.vp_dimensions[1]) / TILE_WIDTH)) # tiles to be shown at one time for y
        self.char_box_top = math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH  # rectangle for the char box
        self.char_box_left = 0
        self.char_box_width = math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH
        self.char_box_height = math.floor(int(0.2 * self.window_height) / TILE_WIDTH) * TILE_WIDTH
        self.combat_log_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = self.window_width - self.combat_log_offset[0]
        self.combat_log_height = self.window_height - self.combat_log_offset[1]
        self.end_turn_button_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.z_up_button_offset = (math.floor(int(0.5 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.z_down_button_offset = (math.floor(int(0.6 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.up_button_offset = (math.floor(int(0.4 * self.window_width) / TILE_WIDTH) * TILE_WIDTH , TILE_WIDTH / 4)
        self.down_button_offset = (math.floor(int(0.4 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.left_button_offset = (TILE_WIDTH / 8, math.floor(int(0.4 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.right_button_offset = (self.combat_log_offset[0], math.floor(int(0.4 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.z_up_button, self.z_up_button_offset[0], self.z_up_button_offset[1])
        self.gui_container.add(self.z_down_button, self.z_down_button_offset[0], self.z_down_button_offset[1])
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.gui_container.add(self.end_turn_button, self.end_turn_button_offset[0], self.end_turn_button_offset[1])
        self.gui_container.add(self.up_button, self.up_button_offset[0], self.up_button_offset[1])
        self.gui_container.add(self.down_button, self.down_button_offset[0], self.down_button_offset[1])
        self.gui_container.add(self.left_button, self.left_button_offset[0], self.left_button_offset[1])
        self.gui_container.add(self.right_button, self.right_button_offset[0], self.right_button_offset[1])
        self.app.init(self.gui_container)
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.recalc_vp()
    
    def set_fullscreen(self):
        """ gets called when we go fullscreen, recalc all the offsets """
        pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), FULLSCREEN, 32)
        newwidth = math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH)
        newheight = math.floor(int(0.8 * FULLSCREEN_HEIGHT) / TILE_WIDTH)
        self.stats_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH)
        self.click_state_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 2)
        self.stat_box_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 5)
        self.vp_dimensions = (newwidth * TILE_WIDTH, newheight * TILE_WIDTH) # resolution of the view port
        self.num_x_tiles = int(math.ceil(int(self.vp_dimensions[0]) / TILE_WIDTH)) # tiles to be shown at one time for X
        self.num_y_tiles = int(math.ceil(int(self.vp_dimensions[1]) / TILE_WIDTH)) # tiles to be shown at one time for y
        self.char_box_top = math.floor(int(0.8 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH  # rectangle for the char box
        self.char_box_left = 0
        self.combat_log_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = FULLSCREEN_WIDTH - self.combat_log_offset[0]
        self.combat_log_height = FULLSCREEN_HEIGHT - self.combat_log_offset[1]
        self.char_box_width = math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH
        self.char_box_height = math.floor(int(0.2 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH
        self.end_turn_button_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.z_up_button_offset = (math.floor(int(0.5 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.z_down_button_offset = (math.floor(int(0.6 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.up_button_offset = (math.floor(int(0.4 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH , TILE_WIDTH / 4)
        self.down_button_offset = (math.floor(int(0.4 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.left_button_offset = (TILE_WIDTH / 8, math.floor(int(0.4 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH)
        self.right_button_offset = (self.combat_log_offset[0], math.floor(int(0.4 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH)
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.z_up_button, self.z_up_button_offset[0], self.z_up_button_offset[1])
        self.gui_container.add(self.z_down_button, self.z_down_button_offset[0], self.z_down_button_offset[1])
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.gui_container.add(self.end_turn_button, self.end_turn_button_offset[0], self.end_turn_button_offset[1])
        self.gui_container.add(self.up_button, self.up_button_offset[0], self.up_button_offset[1])
        self.gui_container.add(self.down_button, self.down_button_offset[0], self.down_button_offset[1])
        self.gui_container.add(self.left_button, self.left_button_offset[0], self.left_button_offset[1])
        self.gui_container.add(self.right_button, self.right_button_offset[0], self.right_button_offset[1])
        self.app.init(self.gui_container) 
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.recalc_vp()
        
    def screen_resize(self, w, h):
        """ gets called when the screen is resized either by the min / max buttons or draging the borders """
        self.window_width = w
        self.window_height = h
        pygame.display.set_mode((w, h), RESIZABLE)
        newwidth = math.floor(int(0.8 * w) / TILE_WIDTH)
        newheight = math.floor(int(0.8 * h) / TILE_WIDTH)
        self.stats_offset = (math.floor(int(0.8 * w) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH)
        self.click_state_offset = (math.floor(int(0.8 * w) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 2)
        self.stat_box_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 5)
        self.vp_dimensions = (newwidth * TILE_WIDTH, newheight * TILE_WIDTH) # resolution of the view port
        self.num_x_tiles = int(math.ceil(int(self.vp_dimensions[0]) / TILE_WIDTH)) # the number of tiles to be shown at one time for X
        self.num_y_tiles = int(math.ceil(int(self.vp_dimensions[1]) / TILE_WIDTH)) # the number of tiles to be shown at one time for y
        self.char_box_top = math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH  # rectangle for the char box
        self.char_box_left = 0
        self.char_box_width = math.floor(int(0.8 * w) / TILE_WIDTH) * TILE_WIDTH
        self.char_box_height = math.floor(int(0.2 * h) / TILE_WIDTH) * TILE_WIDTH
        self.combat_log_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = self.window_width - self.combat_log_offset[0]
        self.combat_log_height = self.window_height - self.combat_log_offset[1]
        self.end_turn_button_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.z_up_button_offset = (math.floor(int(0.5 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.z_down_button_offset = (math.floor(int(0.6 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.up_button_offset = (math.floor(int(0.4 * self.window_width) / TILE_WIDTH) * TILE_WIDTH , TILE_WIDTH / 4)
        self.down_button_offset = (math.floor(int(0.4 * self.window_width) / TILE_WIDTH) * TILE_WIDTH, math.floor(int(0.8 * self.window_height) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH)
        self.left_button_offset = (TILE_WIDTH / 8, math.floor(int(0.4 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.right_button_offset = (self.combat_log_offset[0], math.floor(int(0.4 * self.window_height) / TILE_WIDTH) * TILE_WIDTH)
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.z_up_button, self.z_up_button_offset[0], self.z_up_button_offset[1])
        self.gui_container.add(self.z_down_button, self.z_down_button_offset[0], self.z_down_button_offset[1])
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.gui_container.add(self.end_turn_button, self.end_turn_button_offset[0], self.end_turn_button_offset[1])
        self.gui_container.add(self.up_button, self.up_button_offset[0], self.up_button_offset[1])
        self.gui_container.add(self.down_button, self.down_button_offset[0], self.down_button_offset[1])
        self.gui_container.add(self.left_button, self.left_button_offset[0], self.left_button_offset[1])
        self.gui_container.add(self.right_button, self.right_button_offset[0], self.right_button_offset[1])
        self.app.init(self.gui_container)
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.fullscreen = False
        self.recalc_vp()
    
    def save_game(self):
        """ Saves the game to disk """
        self.log.append("Saving Game")
        turn_file = file("turn.dat", "wb")
        pickle.dump(self.turn, turn_file, 2)
        turn_file.close()
        map_file = file("./map.dat", "wb")
        pickle.dump(self.mapdata, map_file, 2)
        map_file.close()
        player_file = file("./players.dat", "wb")
        pickle.dump(self.players, player_file, 2)
        player_file.close()
        dead_players_file = file("./dead_players.dat", "wb")
        pickle.dump(self.dead_players, dead_players_file, 2)
        dead_players_file.close()
        mob_file = file("./mobs.dat", "wb")
        pickle.dump(self.mobs, mob_file, 2)
        mob_file.close()
        dead_mob_file = file("./dead_mobs.dat", "wb")
        pickle.dump(self.dead_mobs, dead_mob_file, 2)
        dead_mob_file.close()

    def load_game(self):
        """ Load the last savegame """
        self.log.append("Loading Previous Save")
        turn_file = file("./turn.dat", "rb")
        self.turn = pickle.load(turn_file)
        turn_file.close()
        map_file = file("./map.dat", "rb")
        self.mapdata = pickle.load(map_file)
        map_file.close()
        player_file = file("./players.dat", "rb")
        self.players = pickle.load(player_file)
        player_file.close()
        # reload the player images
        for p in self.players:
            p.re_init_images()
        dead_players_file = file("dead_players.dat", "rb")
        self.dead_players = pickle.load(dead_players_file)
        dead_players_file.close()
        # reload the dead player images
        for p in self.dead_players:
            p.re_init_images()
        mob_file = file("./mobs.dat", "rb")
        self.mobs = pickle.load(mob_file)
        mob_file.close()
        # reload the monster images
        for m in self.mobs:
            m.re_init_images()
        dead_mob_file = file("./dead_mobs.dat", "rb")
        self.dead_mobs = pickle.load(dead_mob_file)
        dead_mob_file.close()
        # reload dead monster images
        for m in self.dead_mobs:
            m.re_init_images()
        # reload item images
        items = self.get_item_list()
        for item in items:
            item.re_init_images()

    def get_item_list(self):
        """ Get the list of items that are scattered about for when we reload a savegame """
        temp_item_list = []
        for z in range(self.zlevels):
            for x in range(self.mapw):
                for y in range(self.maph):
                    for item in self.mapdata[z][x][y].content:
                        temp_item_list.append(item)
        for p in self.players:
            for item in p.backpack:
                temp_item_list.append(item)
        return temp_item_list

    def make_map(self):
        """ generate the map """
        max_rooms = 35
        min_size = 5
        max_size = 15
        starting_floor = True
        for z in range(self.zlevels):
            num_rooms = 0
            rooms = []
            upstairs_flag = False
            #for r in range(max_rooms): #IGNORE:W0612
            iteration = 0
            while num_rooms != max_rooms:
                iteration = iteration + 1
                #random width and height
                w = randrange(min_size, max_size)
                h = randrange(min_size, max_size)
                #random position without going out of the boundaries of the map
                x = randrange(0, self.mapw - w - 1)
                y = randrange(0, self.maph - h - 1)
                new_room = Room(x, y, w, h)
                #run through the other rooms and see if they intersect with this one
                failed = False
                for other_room in rooms:
                    #if new_room.intersect(other_room):
                    if new_room.intersect(other_room):
                        failed = True
                        break
                if not failed:
                    IG = ItemGenerator()
                    #this means there are no intersections, so this room is valid
                    self.create_room(new_room, z)
                    #add some contents to this room, such as monsters
                    #center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()
                    if num_rooms == 0:
                        if z != 0:
                            stairs_down = IG.generate_specific_item("StairsDown")        
                            self.mapdata[z][new_x+1][new_y-1].content.append(stairs_down)
                        if starting_floor:
                            starting_floor = False
                            xx, yy, zz = self.get_open_spot_around(new_x, new_y, z)
                            for p in self.players:
                                xx, yy, zz = self.get_open_spot_around(xx, yy, zz)
                                p.x, p.y, p.z = (xx, yy, zz)
                                p.fov.update(self.find_fov(p.x, p.y, p.z, p.get_view_range()))
                                
                    elif z != max(range(self.zlevels)) and num_rooms >= (max_rooms - 2) and upstairs_flag == False:
                        upstairs_flag = True
                        stairs_up = IG.generate_specific_item("StairsUp")        
                        self.mapdata[z][new_x][new_y].content.append(stairs_up)       
                    else:
                        if roll_d_10() > 3:
                            mob_generator = MonsterGenerator()
                            for j in range(choice(MOBS_PER_ROOM)):
                                spot_list = self.get_open_spots_around(new_x, new_y, z)
                                mob = mob_generator.generate_monster(z+1 )
                                mob.x, mob.y, mob.z = choice(spot_list)
                                self.mobs.append(mob)
                            for m in self.mobs:
                                m.fov.update(self.find_fov(m.x, m.y, m.z, m.get_view_range()))
                        else:
                            IG = ItemGenerator()
                            random_item = IG.generate_random_item() 
                            self.mapdata[z][new_x][new_y].content.append(random_item)    
                    #center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms-1].center()
                        if randrange(0, 1) == 1:
                            #first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y, z)
                            self.create_v_tunnel(prev_y, new_y, new_x, z)
                        else:
                            #first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x, z)
                            self.create_h_tunnel(prev_x, new_x, new_y, z)
         
                    #finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

    def update_clicked_mob(self):
        """ toggle selected mob status """
        for m in self.mobs:
            if self.selected_mob == m.uuid:
                m.selected = True
            else:
                m.selected = False
                    
    def update_combat_log(self):
        """ update the combat log """
        max_size = 500
        if len(self.log) > max_size:
            self.log = []
        s = '\n'.join(self.log)
        self.combat_log.value = s
            
    def view_port_click_to_coords(self, x, y, z):
        """ get the clicked tiles coord value """
        return (int((x - self.vp_render_offset[0] + self.view_port_coord[0]) / TILE_WIDTH)), int(((y - self.vp_render_offset[1] + self.view_port_coord[1]) / TILE_WIDTH)), z      
    
    def logic(self):
        """ main logic happens here """
        self.start_x_tile = math.floor(float(self.view_port_coord[0]) / TILE_WIDTH)
        self.start_y_tile = math.floor(float(self.view_port_coord[1]) / TILE_WIDTH)
        self.update_combat_log()
        self.handle_events()
        self.handle_fog_of_war()
        self.handle_mouse_cursor()
        self.handle_viewport()
        self.handle_win_condition()
        
    def render(self):
        """ rendering stuffs to the screen happens here """
        self.screen.fill((0, 0, 0))
        self.draw_map()
        self.draw_click_map()
        self.draw_possible_moves()
        self.draw_path_lines()
        self.screen.blit(self.tiled_bg, self.vp_render_offset, (self.view_port_coord[0] - (self.start_x_tile * TILE_WIDTH), (self.view_port_coord[1] - (self.start_y_tile * TILE_WIDTH))) + self.vp_dimensions)
        self.draw_mouse_box()
        self.draw_players_and_mobs()
        self.screen.blit(self.arial_font.render('coordinates: ' + str(self.view_port_coord[0]/TILE_WIDTH) + ", " + str(self.view_port_coord[1]/TILE_WIDTH) + " Z: " + str(self.current_z), True, (255, 255, 255)), self.stats_offset)
        self.screen.blit(self.arial_font.render('State: ' + str(self.click_state), True, (255, 255, 255)), self.click_state_offset)
        self.draw_char_box()
        self.app.paint()
        self.draw_stats()
        if self.win:
            self.screen.blit(self.arial_font.render('You Win!', True, (255, 255, 255)), (self.window_width/2, self.window_height/2))
        elif self.win == False:
            self.screen.blit(self.arial_font.render('You Lose!', True, (255, 255, 255)), (self.window_width/2, self.window_height/2))
        self.mainclock.tick(FPS)
        pygame.display.flip()
    
    def run(self):
        """ This is the main function """
        while self.running:
            if self.create_chars: #char creator
                CC = CharCreator()
                exit_game = CC.run(self.screen)
                if exit_game: # allow quitting from the char creator
                    self.running = False
                    quit_game()
                else:
                    self.players = CC.fetch_player_list()
                    if self.players == None: #loading a game
                        self.load_game()
                    else:
                        self.make_map()
                    self.center_vp_on_player()
                    self.recalc_vp()
                    self.create_chars = False
            elif self.show_inventory:
                player = self.lookup_player_by_uuid(self.selected_player)
                INV = Inventory(player)
                dropped_items = INV.run(self.screen)
                for i in dropped_items:
                    self.mapdata[player.z][player.x][player.y].content.append(i)
                self.show_inventory = False
            elif self.player_info:
                player = self.lookup_player_by_uuid(self.selected_player)
                self.PI = PlayerInfo(player)
                self.PI.connect(gui.QUIT, self.PI.close, None)
                self.app.open(self.PI)
                self.player_info = False
            elif self.show_quit_diag:
                QD = QuitDialogue()
                cancel = QD.run(self.screen)
                if cancel:
                    # they hit cancel
                    self.show_quit_diag = False
                else:
                    self.running = False
            self.logic()   
            self.render()
        quit_game()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    # fire up the game
    TB = Game()
    TB.run()