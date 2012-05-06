# pylint: disable-msg=C0111
# pylint: disable-msg=C0301
""" Main file for the project till I have time to refactor the code to something more managable """
try:
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
    from Player import Player
    from Mob import Mob
    from Button import Button
    from pathfinder import PathFinder
    from random import randint, randrange
    from Cursors import Cursors
    from CombatLog import CombatLog
    from Stats import Stats
except ImportError, err:
    print "couldn't load module, %s" % (err)
    sys.exit(2)
#Constants
FPS = 60
FULLSCREEN_WIDTH = 1920
FULLSCREEN_HEIGHT = 1200
TILE_WIDTH = 32

class Game:
    """Main game object"""
    def __init__(self):
        self.running = True # set the game loop good to go
        self.window_width = 1650
        self.window_height = 1050
        self.mapw = 100
        self.maph = 100
        self.fullscreen = False
        self.current_z = 0
        self.buttons = {}
        self.motion = None
        self.turn = 0
        self.pressed_button = None
        self.moves = Set()
        self.win = None
        self.pathlines = []
        self.click_state = None
        self.floor_images = [pygame.image.load(os.path.join('images', 'floor.png')),
                             pygame.image.load(os.path.join('images', 'stairs.png')),
                             pygame.image.load(os.path.join('images', 'fog.png')),
                             pygame.image.load(os.path.join('images', 'stairsdown.png'))
                             ]
        
        self.item_images = [pygame.image.load(os.path.join('images', 'tuRKEYHEART.png'))]
        
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
                            pygame.image.load(os.path.join('images', 'fog_b_r_corner.png')) # 18
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
                            pygame.image.load(os.path.join('images', 'wall_b_r_corner.png')) # 18
                            ]
        
        self.images = [pygame.image.load(os.path.join('images',"grass.png")), 
                       pygame.image.load(os.path.join('images',"wall.png")), 
                       pygame.image.load(os.path.join('images',"water.png")), 
                       pygame.image.load(os.path.join('images',"dig.png")), 
                       pygame.image.load(os.path.join('images',"grass4.png"))]
        
        self.dead_images = [pygame.image.load(os.path.join('images', "deddorf.png")),
                            pygame.image.load(os.path.join('images', "dedmob.png")),
                            pygame.image.load(os.path.join('images', "stompdedmob.png")),
                            ]
        
        pygame.init()
        self.stats = Stats(200, 200)
        #setup the default screen size
        if self.fullscreen == True:
            self.screen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.window_width, self.window_height), RESIZABLE)

        pygame.display.set_caption('SPACEBAR to advance a turn')
        #Intro's on by default, will need to add a config file entry for this.
        self.mouse_box = False
        self.mouse_box_rect = pygame.Rect((0, 0), (TILE_WIDTH, TILE_WIDTH))
        self.mainclock = pygame.time.Clock()
        # various rendering offsets
        self.vp_render_offset = (TILE_WIDTH, TILE_WIDTH)
        self.stats_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH)
        self.click_state_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 2)
        self.end_turn_button = Button()
        self.button_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.end_turn_button.set_coords(self.button_offset[0], self.button_offset[1])
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
        self.app = gui.App()
        self.combat_log = CombatLog("", self.combat_log_width, self.combat_log_height)
        self.log = []
        self.log.append("Welcome to the game")
       
        #game_gui = GameGui()
        self.gui_container = gui.Container(align=-1, valign=-1)
        # c.add(game_gui,0,0)
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
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
        self.make_map()
        self.center_vp_on_player()
        self.recalc_vp()
        
    def recalc_vp(self):
        vpset = Set()
        #pprint(self.start_x_tile)
        for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
            for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
                vpset.add((x, y, self.current_z))
        self.view_port = vpset
        
    def center_vp_on(self, x, y, z):
        center_x, center_y = self.get_center_of_vp()
        offset_x = center_x * -TILE_WIDTH
        offset_y = center_y * -TILE_WIDTH
        self.view_port_coord[0] = offset_x + x * TILE_WIDTH 
        self.view_port_coord[1] = offset_y + y * TILE_WIDTH
        self.current_z = z
        return
        
    def center_vp_on_player(self):
        for p in self.players:
            x, y, z = p.x, p.y, p.z
            center_x, center_y = self.get_center_of_vp()
            #print str(center_x)
            offset_x = center_x * -TILE_WIDTH
            offset_y = center_y * -TILE_WIDTH
            self.view_port_coord[0] = offset_x + x * TILE_WIDTH 
            self.view_port_coord[1] = offset_y + y * TILE_WIDTH
            self.current_z = z
            return
    
    def draw_stats(self):
        if self.selected_player != None:
            p = self.lookup_player_by_uuid(self.selected_player)
            self.stats.update_stats(p)
            self.screen.blit(self.stats, self.stat_box_offset)
            return
        elif self.selected_mob != None:
            m = self.lookup_mob_by_uuid(self.selected_mob)
            self.stats.update_stats(m)
            self.screen.blit(self.stats, self.stat_box_offset)
            
    def get_center_of_vp(self):
        return self.num_x_tiles /2, self.num_y_tiles /2
        
    def handle_viewport(self):
        # view port reset, don't scroll past the h / v bounds
        #pprint(self.view_port)
        #self.recalc_vp()
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
        #pprint(self.view_port_coord)
    
    def update_combat_log(self):
        s = '\n'.join(self.log)
        self.combat_log.value = s
    
    def compute_path(self, start, end):
        pf = PathFinder(self.successors, move_cost, move_cost)
        #pprint(self.move_cost)
        #t = time.clock()
        pathlines = list(pf.compute_path(start, end))

        if pathlines == []:
            #print "No path found" 
            return pathlines
        else:
            #print "Found path (length %d)" % len(pathlines)
            return pathlines
    
    def handle_keyboard(self, event):
        keymods = pygame.key.get_mods()
        if event.key == K_ESCAPE: 
            self.running = False
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
        #reset viewport 
        elif event.key == K_F11 :
            if self.fullscreen == False:
                self.set_fullscreen()
                self.fullscreen = True
            elif self.fullscreen == True:
                pygame.display.set_mode((self.window_width, self.window_height), RESIZABLE)
                self.set_not_fullscreen()
                self.fullscreen = False
                
    def click_in_viewport(self, x, y):
        if x < self.num_x_tiles * TILE_WIDTH + self.vp_render_offset[0] and x > self.vp_render_offset[0] and y < self.num_y_tiles * TILE_WIDTH + self.vp_render_offset[1] and y > self.vp_render_offset[1]: #within the map viewport
            return True
        else:
            return False
    
    def view_port_click_to_coords(self, x, y, z):
        return (int((x - self.vp_render_offset[0] + self.view_port_coord[0]) / TILE_WIDTH)), int(((y - self.vp_render_offset[1] + self.view_port_coord[1]) / TILE_WIDTH)), z      
    
    def check_player_portrait_clicks(self, mx, my):
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
        for m in self.mobs:
            if m.pressed_portrait(mx, my):
                if m.selected == True:
                    m.selected = False
                else:
                    m.selected = True
                    self.center_vp_on(m.x, m.y, m.z)
                return True
            
        return False
       
    def handle_events(self):
        for event in pygame.event.get():
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
                            #print "You clicked on a player"
                            self.selected_player = player_uuid
                            self.click_state = "MoveSelect"
                        elif mob_uuid:
                            #print "You CLICKED ON A MOB"
                            self.center_vp_on(x, y, z)
                            self.selected_mob = mob_uuid
                            # Add a panel that will show the mob details / stats
                            self.update_clicked_mob()
                                                     
                        #self.check_map(x,y,z)
                        #self.update_click_map(x, y, z, 2)
                    elif self.end_turn_button.pressed(mx, my):
                        self.pressed_button = "End Turn"
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
                else:
                    # UI stuffs
                    self.app.event(event)
                self.buttons = {}
            elif event.type == MOUSEBUTTONDOWN:
                self.app.event(event)
            
                #del self.buttons[event.button]
            elif event.type == VIDEORESIZE:
                # allow for the window to be resized manually.
                w, h = event.w, event.h
                self.screen_resize(w, h)
                
    def lookup_player_by_uuid(self, uuid):
        for p in self.players:
            if p.uuid == uuid:
                #print "Matching player found with the same uuid"
                return p
        return None
    
    def lookup_mob_by_uuid(self, uuid):
        for m in self.mobs:
            if m.uuid == uuid:
                #print "Matching mob found with the same uuid"
                return m
        return None
    
    def pick_dest(self, x, y, z):
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
         
    def update_clicked_mob(self):
        for m in self.mobs:
            if self.selected_mob == m.uuid:
                m.selected = True
            else:
                m.selected = False
    
    def check_map_for_player(self, x, y, z):
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
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
        for m in self.mobs:
            if m.x == x and m.y == y and m.z == z:
                m.selected = True
                return m.uuid
        return None
    
    def logic(self):
        self.start_x_tile = math.floor(float(self.view_port_coord[0]) / TILE_WIDTH)
        self.start_y_tile = math.floor(float(self.view_port_coord[1]) / TILE_WIDTH)
        self.update_combat_log()
        self.handle_events()
        self.handle_fog_of_war()
        self.handle_buttons()
        self.handle_mouse_cursor()
        self.handle_viewport()
        self.handle_win_condition()
        
    def handle_win_condition(self):
        if len(self.mobs) == 0:
            self.win = True
        if len(self.players) == 0:
            self.win = False
        
    def handle_mouse_cursor(self):
        if self.click_state == "MoveSelect":
            size, hotspot, cursor, mask = make_cursor(self.cursors.move)
            pygame.mouse.set_cursor(size, hotspot, cursor, mask)
        else:
            size, hotspot, cursor, mask = make_cursor(self.cursors.arrow)
            pygame.mouse.set_cursor(size, hotspot, cursor, mask)
        
    def successors(self, x, y, z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
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
    
    def get_fog_neighbors_values(self, x, y, z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
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
        #pprint(templist)
        return templist

    
    def get_neighbors_values(self, x, y, z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
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
        #pprint(templist)
        return templist

    def get_open_spot_around(self, x, y, z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
        
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
    
    def find_moves(self, x, y, z, movement):
        slist = []
        movement_range = range(-movement, movement+1)
        #pprint(movement_range)
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
        slist = []
        size_range = range(-size, size+1)
        #pprint(size)
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
    
    def advance_turn(self):
        """ Advance one turn in game time """
        # process the players moves, will have to base this on initiative at some point.
        self.turn = self.turn + 1
        self.log.append("Advancing to turn " + str(self.turn))
        #print str(self.turn)
        for p in self.players:
            #print p.name
            #p.fov.update(self.find_fov(p.x, p.y, p.z, p.view_range))
            if p.pathlines:
                #print p.name + "is processing a move"
                move = p.pathlines.pop(0)
                if (p.x, p.y, p.z) == move:
                    if p.pathlines:
                        move = p.pathlines.pop(0) 
                p.x, p.y, p.z = move
                p.fov.update(self.find_fov(p.x, p.y, p.z, p.view_range))
            #manage players running into items ie: stairs
            item_list = self.get_tile_items(p.x, p.y, p.z)
            for item in item_list:
                if item == "StairsUp":
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
                        p.fov.update(self.find_fov(p.x, p.y, p.z, p.view_range))
                        self.center_vp_on(p.x, p.y, p.z)
                elif item == "StairsDown":
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
                            p.fov.update(self.find_fov(p.x, p.y, p.z, p.view_range))
                            self.center_vp_on(p.x, p.y, p.z)
                elif item == "HealingPotion":
                    p.heal(15)
                    text = p.name + " heals for 15."
                    self.log.append(text)
                    self.mapdata[p.z][p.x][p.y].content.remove(item)
                
        # mob movement
        self.mob_ai_move()    
        for m in self.mobs: #IGNORE:C0103
            #print m.name
            if m.pathlines:
                #m.fov.update(self.find_fov(m.x, m.y, m.z, m.view_range))
                #print m.name + "is processing a move"
                move = m.pathlines.pop(0)
                if (m.x, m.y, m.z) == move:
                    if m.pathlines:
                        move = m.pathlines.pop(0)
                m.x, m.y, m.z = move
            m.fov.update(self.find_fov(m.x, m.y, m.z, m.view_range))
        
    def get_tile_items(self, x, y, z):
        return self.mapdata[z][x][y].content
                    
    def check_mob_collision(self, x, y, z):
        for p in self.players:
            area = self.successors(p.x, p.y, p.z)
            for a in area:
                if a == (x, y, z):
                    return True
        return False
    
    def mob_ai_move(self):
        for m in self.mobs:
            for p in self.players:
                if is_in_fov(m, p):
                    if self.check_mob_collision(m.x, m.y, m.z):
                        self.log.append("Combat Started Rolling Initiative:")
                        p.pathlines = []
                        m.pathlines = []
                        # Combat 
                        #print "COLLISION FOUND"
                        player_initiative = roll_d_20()
                        mob_initiative = roll_d_20()
                        log_message = p.name + ": " + str(player_initiative) + " / " + m.name + ": " + str(mob_initiative) + "."
                        self.log.append(log_message)
                        #print "Players Roll: ", player_initiative
                        #print "Monster roll: ", mob_initiative
                        if player_initiative > mob_initiative:
                            log_message = p.name + " wins initiative, resolving damage"
                            self.log.append(log_message)
                            damage = p.str - m.defense
                            if m.take_damage(damage):
                                log_message = m.name + " takes " + str(damage) + " from " + p.name + "."
                                self.log.append(log_message)
                                #still alive attack the player back
                                if p.take_damage(damage):
                                    #player still alive
                                    log_message = p.name + " takes " + str(damage) + " from " + m.name + "."
                                    self.log.append(log_message)
                                else: 
                                    #player is dead
                                    p.alive = False
                                    log_message = p.name + " takes " + str(damage) + " from " + m.name + " and dies!"
                                    self.log.append(log_message)
                                    
                            else:
                                #mobs dead remove it
                                m.alive = False
                                log_message = m.name + " takes " + str(damage) + " from " + p.name + " and dies!"
                                self.log.append(log_message)
                        else: #mob won the initiative check
                            log_message = m.name + " wins initiative, resolving damage"
                            self.log.append(log_message)
                            damage = m.str - p.defense
                            if p.take_damage(damage):
                                damage = p.str - m.defense
                                log_message = p.name + " takes " + str(damage) + " from " + m.name + "."
                                self.log.append(log_message)
                                #still alive attack the mob back
                                if m.take_damage(damage):
                                    #mobs still alive
                                    log_message = m.name + " takes " + str(damage) + " from " + p.name + "."
                                    self.log.append(log_message)
                                else: 
                                    #mob is dead
                                    m.alive = False
                                    log_message = m.name + " takes " + str(damage) + " from " + p.name + " and dies!"
                                    self.log.append(log_message)
                                
                            else:
                                #mobs dead remove it
                                p.alive = False
                                log_message = p.name + " takes " + str(damage) + " from " + m.name + " and dies!"
                                self.log.append(log_message)
                    else:
                        if m.pathlines:
                            pass
                        else:
                            # pick a player to go after.
                            start = (m.x, m.y, m.z) # start position
                            end = (p.x, p.y, p.z)
                            templist = self.compute_path(start, end)
                            if templist:
                                m.pathlines = templist
                
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
                self.dead_mobs.append((m.x, m.y, m.z))
                self.mobs.remove(m)
                
    def handle_buttons(self):
        if self.pressed_button != None:
            if self.pressed_button == "End Turn":
                self.advance_turn()
                self.pressed_button = None
    
    def handle_fog_of_war(self):
        for p in self.players:
            for (x, y, z) in p.fov:
                self.un_fog(x, y, z)
        
    def draw_map(self):
        for x in range(self.mapw):
        #for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
            #for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
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
                        # TODO make an item object so I'm not searching over strings
                        if item == "StairsUp":
                            self.tiled_bg.blit(self.floor_images[1], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
                        elif item == "StairsDown":
                            self.tiled_bg.blit(self.floor_images[3], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
                        elif item == "HealingPotion":
                            self.tiled_bg.blit(self.item_images[0], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
    
    def draw_click_map(self):
        for x in range(self.mapw):
            for y in range(self.maph):
                if (x, y, self.current_z) in self.view_port:
                    if self.clickdata[self.current_z][x][y] != 0:
                        self.tiled_bg.blit(self.images[self.clickdata[self.current_z][x][y]], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
                
    def draw_path_lines(self):
        gray = (115, 115, 115)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        colors = [gray, green, red, white]
        rect = pygame.Rect(0, 0, TILE_WIDTH, TILE_WIDTH)
        color_count = 0
        line_width = 5
        
        for p in self.players:
            if p.pathlines:
                for l in p.pathlines:
                    for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
                        for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
                            if l[0] == x and l[1] == y and l[2] == self.current_z:
                                #print "Haulin ass getting paid"
                                rect.topleft = ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH)
                                pygame.draw.rect(self.tiled_bg, colors[color_count], rect, line_width)
                                #self.tiled_bg.blit(self.images[4], )
            color_count = color_count + 1
            line_width = line_width - 1
    
    def draw_char_box(self):
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
                    if m.selected == True:
                        pygame.draw.rect(self.screen, red, m.portrait_rect, 5)
                    count = count + 1
            
    def draw_possible_moves(self):
        #print "MOVES:"
        #pprint(self.moves)
        for x in range(int(self.start_x_tile), int(self.start_x_tile + self.num_x_tiles)):
            for y in range(int(self.start_y_tile), int(self.start_y_tile + self.num_y_tiles)):
                if (x, y, self.current_z) in self.moves:
                    #print "x,y are in the set"
                    self.tiled_bg.blit(self.images[3], ((x - self.start_x_tile) * TILE_WIDTH, (y - self.start_y_tile) * TILE_WIDTH))
    
    def get_possible_moves(self, x, y, z):
        successors_list = self.find_moves(x, y, z, 2)
        new_set = Set()
        new_set.update(successors_list)
        return new_set    
    
    def draw_mouse_box(self):
        blue = (0, 0, 255)
        if self.mouse_box == True:
            pygame.draw.rect(self.screen, blue, self.mouse_box_rect, 3)
            
    def render(self):
        self.screen.fill((0, 0, 0))
        self.draw_map()
        self.draw_click_map()
        self.draw_possible_moves()
        self.draw_path_lines()
        self.screen.blit(self.tiled_bg, self.vp_render_offset, (self.view_port_coord[0] - (self.start_x_tile * TILE_WIDTH), (self.view_port_coord[1] - (self.start_y_tile * TILE_WIDTH))) + self.vp_dimensions)
        self.draw_mouse_box()
        
        self.draw_players_and_mobs()
        self.screen.blit(self.end_turn_button.image, self.end_turn_button.rect)
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
    
    def in_vp(self, x, y, z):
        #coord to vp
        #pprint((x,y,z))
        if (x, y, z) in self.view_port:
            return True
        else:
            return False
    
    def draw_players_and_mobs(self):
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
        for (x, y, z) in self.dead_mobs:
            if (x, y, z) in self.view_port:
                self.screen.blit(self.dead_images[2], self.vp_render_offset, (self.view_port_coord[0] - (x * TILE_WIDTH), (self.view_port_coord[1] - (y * TILE_WIDTH))) + self.vp_dimensions)
                    
    def check_map(self, x, y, zlevel):
        #print "x:", str(x) + "y:", str(y) + "z:", str(zlevel)
        return self.mapdata[zlevel][int(x)][int(y)].value
    
    def check_click_map(self, x, y, z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
        return self.mapdata[z][int(x)][int(y)]
    
    def update_map(self, x, y, z, value):
        self.mapdata[z][int(x)][int(y)].value = value
        
    def un_fog(self, x, y, z):
        self.mapdata[z][x][y].fog = False
        
    def update_click_map(self, x, y, z, value):
        self.clickdata[z][int(x)][int(y)] = value
        self.moves = self.get_possible_moves(int(x), int(y), z)
        
    def set_not_fullscreen(self):
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
        self.button_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.end_turn_button.set_coords(self.button_offset[0], self.button_offset[1])
        self.combat_log_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = self.window_width - self.combat_log_offset[0]
        self.combat_log_height = self.window_height - self.combat_log_offset[1]
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.app.init(self.gui_container)
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.recalc_vp()
    
    def set_fullscreen(self):
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
        self.char_box_width = math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH
        self.char_box_height = math.floor(int(0.2 * FULLSCREEN_HEIGHT) / TILE_WIDTH) * TILE_WIDTH
        self.button_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.end_turn_button.set_coords(self.button_offset[0], self.button_offset[1])
        self.combat_log_offset = (math.floor(int(0.8 * FULLSCREEN_WIDTH) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = FULLSCREEN_WIDTH - self.combat_log_offset[0]
        self.combat_log_height = FULLSCREEN_HEIGHT - self.combat_log_offset[1]
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.app.init(self.gui_container) 
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.recalc_vp()
        
    def screen_resize(self, w, h):
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
        self.button_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 3)
        self.end_turn_button.set_coords(self.button_offset[0], self.button_offset[1])
        self.combat_log_offset = (math.floor(int(0.8 * self.window_width) / TILE_WIDTH) * TILE_WIDTH + TILE_WIDTH, TILE_WIDTH * 20)
        self.combat_log_width = self.window_width - self.combat_log_offset[0]
        self.combat_log_height = self.window_height - self.combat_log_offset[1]
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1, valign=-1)
        self.gui_container.add(self.combat_log, self.combat_log_offset[0], self.combat_log_offset[1])
        self.app.init(self.gui_container)
        self.tiled_bg = pygame.Surface((self.num_x_tiles * TILE_WIDTH, self.num_y_tiles * TILE_WIDTH)).convert() #IGNORE:E1121
        self.fullscreen = False
        self.recalc_vp()
        
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
 
    def make_map(self):
        max_rooms = 13
        min_size = 5
        max_size = 15
        starting_floor = True
        
        for z in range(self.zlevels):
            num_rooms = 0
            rooms = []
            upstairs_flag = False
            for r in range(max_rooms): #IGNORE:W0612
                #random width and height
                w = randrange(min_size, max_size)
                h = randrange(min_size, max_size)
                #random position without going out of the boundaries of the map
                x = randrange(0, self.mapw - w - 1)
                y = randrange(0, self.maph - h - 1)
         
                #"Rect" class makes rectangles easier to work with
                new_room = Room(x, y, w, h)
         
                #run through the other rooms and see if they intersect with this one
                failed = False
                for other_room in rooms:
                    #if new_room.intersect(other_room):
                    if new_room.intersect(other_room):
                        failed = True
                        break
         
                if not failed:
                    #this means there are no intersections, so this room is valid
         
                    #"paint" it to the map's tiles
                    self.create_room(new_room, z)
         
                    #add some contents to this room, such as monsters
                    #place_objects(new_room)
         
                    #center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()
                    if num_rooms == 0:
                        if z != 0:
                            stairs = "StairsDown"        
                            self.mapdata[z][new_x+1][new_y-1].content.append(stairs)
                            
                        if starting_floor:
                            starting_floor = False
                            self.players.append(Player("Jason", "Coder", new_x, new_y, z))
                            xx, yy, zz = self.get_open_spot_around(new_x, new_y, z)
                            self.players.append(Player("Steve", "Civilian", xx,  yy, zz))
                            xx, yy, zz = self.get_open_spot_around(xx, yy, zz)
                            self.players.append(Player("Mitch", "KiteFlyer", xx, yy, zz))
                            xx, yy, zz = self.get_open_spot_around(xx, yy, zz)
                            self.players.append(Player("Roni", "Hilarmoose", xx,  yy, zz))
                            for p in self.players:
                                p.fov.update(self.find_fov(p.x, p.y, p.z, p.view_range))
                    elif z != max(range(self.zlevels)) and num_rooms >= 6 and upstairs_flag == False:
                        upstairs_flag = True
                        stairs = "StairsUp"        
                        self.mapdata[z][new_x-1][new_y-1].content.append(stairs)       
                            
                        #this is the first room, where the player starts at
                    #    player.x = new_x
                    #    player.y = new_y
                    else:
                        
                        if roll_d_10() > 3:
                            self.mobs.append(Mob("Dave", "Neuromancer", new_x, new_y, z))
                            self.mobs.append(Mob("Gimpy", "Pest", new_x+1, new_y+1, z))
                            for m in self.mobs:
                                m.fov.update(self.find_fov(m.x, m.y, m.z, m.view_range))
                        else: 
                            self.mapdata[z][new_x][new_y].content.append("HealingPotion")    
                    #center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms-1].center()
         
                        #draw a coin (random number that is either 0 or 1)
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
                    
    def find_up_stairs_on(self, z):
        for x in range(self.mapw):
            for y in range(self.maph):
                for i in self.mapdata[z][x][y].content:
                    if i == "StairsUp":
                        return (x, y, z)
        return None

    def find_down_stairs_on(self, z):
        for x in range(self.mapw):
            for y in range(self.maph):
                for i in self.mapdata[z][x][y].content:
                    if i == "StairsDown":
                        return (x, y, z)
        return None
            
    def is_blocked(self, x, y, z):
        #first test the map tile
        #print "x: ", str(x) + " y:", str(y) + " z:", str(z)
        return self.mapdata[z][x][y].blocked
    
    def is_foggy(self, x, y, z):
        #pprint((x,y,z))
        return self.mapdata[z][x][y].fog
    
    def is_sight_blocked(self, x, y, z):
        return self.mapdata[z][x][y].blocked_sight
    def run(self):
        """ This is the main function """
        while self.running:
            self.logic()
            self.render()
            
        pygame.quit()
        sys.exit()

def roll_d_20():
    return randint(1, 20)

def roll_d_10():
    return randint(1, 10)

def is_in_fov(mob, player):
    if (player.x, player.y, player.z) in mob.fov:
        #print "Player is in movement range"
        return True
    return False

def move_cost(c1, c2):
    """ Calculate the cost of moving between spots on the map (Euclidean) """
    return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

def pick_wall_tile(tiles):
    tl_corner = False
    tr_corner = False
    bl_corner = False
    br_corner = False
    left = False
    right = False
    top = False
    bottom = False
    if tiles[1][0] == 1: 
        top = True
    if tiles[2][1] == 1:
        right = True
    if tiles[1][2] == 1:
        bottom = True
    if tiles[0][1] == 1:
        left = True
    if tiles[0][0] == 1:
        tl_corner = True
    if tiles[2][0] == 1:
        tr_corner = True
    if tiles[0][2] == 1:
        bl_corner = True
    if tiles[2][2] == 1:
        br_corner = True
        
        
    if left == False and right == False and top == False and bottom == False and tl_corner == False and tr_corner == False and bl_corner == False and br_corner == False:
        # no floors around normal black tile
        return 0
    elif left == False and right == False and top == False and bottom:
        # bottom has a floor
        return 1
    elif left and right == False and top == False and bottom:
        # bottom and left have floors
        return 2
    elif left and right and top == False and bottom:
        # bottom left and right have floors
        return 3
    elif left == False and right and top == False and bottom:
        # bottom and right have floors
        return 4
    elif left and right == False and top and bottom:
        # bottom, top and left have floors
        return 5
    elif left == False and right and top and bottom:
        # bottom, top and right have floors
        return 6
    elif left and right == False and top == False and bottom == False:
        # left has a floor
        return 7
    elif left and right and top == False and bottom == False:
        # left and right have floors
        return 8
    elif left == False and right and top == False and bottom == False:
        # right has a floor
        return 9
    elif left == False and right == False and top and bottom == False:
        # top has a floor 
        return 10
    elif left == False and right == False and top and bottom:
        # top and bottom have a floor
        return 11
    elif left and right == False and top and bottom == False:
        # top and left have floors
        return 12
    elif left and right and top and bottom == False:
        # top, left and right have floors
        return 13
    elif left == False and right and top and bottom == False:
        return 14
        # top and right have floors
    elif left == False and right == False and top == False and bottom == False and tl_corner == True:
        return 15
    elif left == False and right == False and top == False and bottom == False and tr_corner == True:
        return 16
    elif left == False and right == False and top == False and bottom == False and bl_corner == True:
        return 17
    elif left == False and right == False and top == False and bottom == False and br_corner == True:
        return 18
    else:
        # Catch all go for black for now
        return 0 
    

    
def make_cursor(arrow):
    hotspot = None
    for y in range(len(arrow)):
        for x in range(len(arrow[y])):
            if arrow[y][x] in ['x', ',', 'O']:
                hotspot = x, y
                break
        if hotspot != None:
            break
    if hotspot == None:
        raise Exception("No hotspot specified for cursor!" )
    s2 = []
    for line in arrow:
        s2.append(line.replace('x', 'X').replace(',', '.').replace('O', 'o'))
    cursor, mask = pygame.cursors.compile(s2, 'X', '.', 'o')
    size = len(arrow[0]), len(arrow)
    return size, hotspot, cursor, mask
       
if __name__ == '__main__':
    TB = Game()
    TB.run()