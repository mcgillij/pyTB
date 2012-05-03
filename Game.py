try:
    from Room import Room
    from pgu import gui
    from sets import Set
    import pygame
    import sys
    import math
    from math import sqrt
    import os
    from pprint import pprint
    from pygame.locals import FULLSCREEN, K_DOWN, K_ESCAPE, K_F11, K_LEFT, K_RIGHT, KEYDOWN, K_UP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, RESIZABLE, VIDEORESIZE, K_SPACE, KMOD_CTRL
    from MapTile import MapTile
    from Player import Player
    from Mob import Mob
    from Button import Button
    from pathfinder import PathFinder
    import time
    from random import randint, randrange
    from Cursors import Cursors
    from CombatLog import CombatLog
except ImportError, err:
    print "couldn't load module, %s" % (err)
    sys.exit(2)

class Game:
    def __init__(self):
        self.running = True # set the game loop good to go
        self.fsw = 1920
        self.fsh = 1200
        self.ww = 1650
        self.wh = 1050
        self.tw = 32
        self.mapw = 100
        self.maph = 100
        self.fullscreen = False
        self.currentZlevel = 0
        self.buttons = {}
        self.motion = None
        self.turn = 0
        self.pressedButton = None
        self.moves = Set()
        self.win = None
        self.pathlines = []
        self.clickState = None
        self.floor_images = [pygame.image.load(os.path.join('images', 'floor.png')),
                             pygame.image.load(os.path.join('images', 'stairs.png')),
                             pygame.image.load(os.path.join('images', 'fog.png'))
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
        self.FPS = 60
        pygame.init()
        #setup the default screen size
        if self.fullscreen == True:
            self.screen = pygame.display.set_mode((self.fsw, self.fsh), FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.ww, self.wh), RESIZABLE)

        pygame.display.set_caption('pyTB')
        #Intro's on by default, will need to add a config file entry for this.
        self.mainclock = pygame.time.Clock()
        # various rendering offsets
        self.vpRenderOffset = (self.tw, self.tw)
        self.statsOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw)
        self.clickStateOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 2)
        self.endTurnButton = Button()
        self.button_offset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 3)
        self.endTurnButton.setCords(self.button_offset[0], self.button_offset[1])
        self.vpCoordinate = [0, 0] # Starting coordinates for the view port
        self.vpDimensions = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw, math.floor(int(0.8 * self.wh) / self.tw) * self.tw) # resolution of the view port
       
        self.charBoxTop = math.floor(int(0.8 * self.wh) / self.tw) * self.tw + self.tw  # rectangle for the char box
        self.charBoxLeft = 0
        self.charBoxWidth = math.floor(int(0.8 * self.ww) / self.tw) * self.tw
        self.charBoxHeight = math.floor(int(0.2 * self.wh) / self.tw) * self.tw
        self.combatLogOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 20)
        self.combatLogWidth = self.ww - self.combatLogOffset[0]
        self.combatLogHeight = self.wh - self.combatLogOffset[1] 
        self.app = gui.App()
        self.CombatLog = CombatLog("",self.combatLogWidth,self.combatLogHeight)
        self.log = []
        self.log.append("Welcome to the game")
       
        #game_gui = GameGui()
        self.gui_container = gui.Container(align=-1,valign=-1)
        # c.add(game_gui,0,0)
        self.gui_container.add(self.CombatLog,self.combatLogOffset[0],self.combatLogOffset[1])
        self.app.init(self.gui_container)
        
        
        self.vpStep = self.tw # move 1 tile over.
        self.vpShiftStep = self.tw * 10 # move 10 tile over.
        self.minHorizScrollBound = 0
        self.minVertScrollBound = 0
        self.maxHorizScrollBound = self.mapw * self.tw
        self.maxVertScrollBound = self.maph * self.tw
        self.numXTiles = int(math.ceil(int(self.vpDimensions[0]) / self.tw)) # the number of tiles to be shown at one time for X
        self.numYTiles = int(math.ceil(int(self.vpDimensions[1]) / self.tw)) # the number of tiles to be shown at one time for y
        self.startXTile = math.floor(int(self.vpCoordinate[0]) / self.tw)
        self.startYTile = math.floor(int(self.vpCoordinate[1]) / self.tw)
        self.selectedPlayer = None
        self.selectedMob = None
        self.deadMobs = []
        self.deadPlayers = []
        self.vp = Set()
        
        if not pygame.font.get_init():
            pygame.font.init()
        self.arial_font = pygame.font.SysFont('Arial', 16)
        self.zlevels = 2
        self.mapdata = [[[ MapTile(1) for cols in range(self.maph)] for rows in range(self.mapw)] for z in range(self.zlevels)] #         
        self.clickdata = [[[ 0 for cols in range(self.maph)] for rows in range(self.mapw)] for z in range(self.zlevels)] #          
        self.tiledBG = pygame.Surface((self.numXTiles * self.tw, self.numYTiles * self.tw)).convert()
        #self.tiledBG = pygame.Surface((self.numXTiles * self.tw, self.numYTiles * self.tw)).convert()
        self.players = []
        self.mobs = []
        
        self.Cursors = Cursors()
        self.make_map()
        self.center_vp_on_player()
        self.recalc_vp()
        
        
    def recalc_vp(self):
        vpset = Set()
        #pprint(self.startXTile)
        for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
            for y in range(int(self.startYTile), int(self.startYTile + self.numYTiles)):
                vpset.add((x,y,self.currentZlevel))
        self.vp = vpset
        
    def center_vp_on(self,x,y,z):
        center_x, center_y = self.get_center_of_vp()
        offset_x = center_x * -self.tw
        offset_y = center_y * -self.tw
        self.vpCoordinate[0] = offset_x + x * self.tw 
        self.vpCoordinate[1] = offset_y + y * self.tw
        self.currentZlevel = z
        return
        
    def center_vp_on_player(self):
        for p in self.players:
            x,y,z = p.x,p.y,p.z
            center_x, center_y = self.get_center_of_vp()
            #print str(center_x)
            offset_x = center_x * -self.tw
            offset_y = center_y * -self.tw
            self.vpCoordinate[0] = offset_x + x * self.tw 
            self.vpCoordinate[1] = offset_y + y * self.tw
            self.currentZlevel = z
            return
            
    def get_center_of_vp(self):
        return self.numXTiles /2, self.numYTiles /2
        
    def handle_viewport(self):
        # view port reset, don't scroll past the h / v bounds
        #pprint(self.vp)
        #self.recalc_vp()
        if self.vpCoordinate[0] < 0:
            self.vpCoordinate[0] = 0
        if self.vpCoordinate[0] + self.vpDimensions[0] > self.maxHorizScrollBound:
            self.vpCoordinate[0] = self.maxHorizScrollBound - self.vpDimensions[0]
        if self.vpCoordinate[1] < 0:
            self.vpCoordinate[1] = 0
        if self.vpCoordinate[1] + self.vpDimensions[1] > self.maxVertScrollBound:
            self.vpCoordinate[1] = self.maxVertScrollBound - self.vpDimensions[1]
            
        if self.currentZlevel >= self.zlevels:
            self.currentZlevel = self.zlevels -1
        if self.currentZlevel <= 0:
            self.currentZlevel = 0
                
        self.recalc_vp()
        #pprint(self.vpCoordinate)
    
    def updateCombatLog(self):
        s = '\n'.join(self.log)
        self.CombatLog.value = s
    
    def move_cost(self, c1, c2):
        """ Calculate the cost of moving between spots on the map (Euclidean) """
        return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
    
    def compute_path(self,start, end):
        pf = PathFinder(self.successors, self.move_cost, self.move_cost)
        #pprint(self.move_cost)
        #t = time.clock()
        pathlines = list(pf.compute_path(start, end))

        #dt = time.clock() - t
        if pathlines == []:
            #print "No path found" 
            return pathlines
        else:
            #print "Found path (length %d)" % len(pathlines)
            return pathlines
        #print "Took :" + str(dt) + "To compute path"
    
    def hithere(self):
        pass
    def handle_keyboard(self, event):
        keymods = pygame.key.get_mods()
        if event.key == K_ESCAPE: 
            self.running = False
        
        #View port Movement        
        elif event.key == K_LEFT:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[0] = self.vpCoordinate[0] - self.vpShiftStep
            else:
                self.vpCoordinate[0] = self.vpCoordinate[0] - self.vpStep

        elif event.key == K_RIGHT:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[0] = self.vpCoordinate[0] + self.vpShiftStep
            else:
                self.vpCoordinate[0] = self.vpCoordinate[0] + self.vpStep

        elif event.key == K_UP:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[1] = self.vpCoordinate[1] - self.vpShiftStep
            elif keymods & pygame.KMOD_CTRL:
                self.currentZlevel = self.currentZlevel + 1
            else:
                self.vpCoordinate[1] = self.vpCoordinate[1] - self.vpStep
        elif event.key == K_DOWN:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[1] = self.vpCoordinate[1] + self.vpShiftStep
            elif keymods & pygame.KMOD_CTRL:
                self.currentZlevel = self.currentZlevel - 1
            else:
                self.vpCoordinate[1] = self.vpCoordinate[1] + self.vpStep
        elif event.key == K_SPACE:
            self.advanceTurn()
        #reset viewport 
        elif event.key == K_F11 :
            if self.fullscreen == False:
                self.set_fullscreen()
                self.fullscreen = True
            elif self.fullscreen == True:
                pygame.display.set_mode((self.ww, self.wh), RESIZABLE)
                self.set_not_fullscreen()
                self.fullscreen = False
                
    def click_in_viewport(self,x,y):
        if x < self.numXTiles * self.tw + self.vpRenderOffset[0] and x > self.vpRenderOffset[0] and y < self.numYTiles * self.tw + self.vpRenderOffset[1] and y > self.vpRenderOffset[1]: #within the map viewport
            return True
        else:
            return False
    
    def vpClickToCoords(self,x,y,z):
        return (int((x - self.vpRenderOffset[0] + self.vpCoordinate[0]) / self.tw)), int(((y - self.vpRenderOffset[1] + self.vpCoordinate[1]) / self.tw)), z      
    
    def checkPlayerPortraitClicks(self,mx,my):
        uuid = ""
        for p in self.players:
            if p.pressed_portrait(mx,my):
                uuid = p.uuid
                self.center_vp_on(p.x, p.y, p.z)
                self.selectedPlayer = p.uuid
                self.clickState = "MoveSelect"
        
        for p in self.players:
            if uuid == p.uuid:
                p.selected = True
            else:
                p.selected = False
                
        if uuid is not "":
            return True        
                
        return False
    
    def checkMobPortraitClicks(self,mx,my):
        for m in self.mobs:
            if m.pressed_portrait(mx,my):
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
            elif event.type == MOUSEBUTTONUP:
                self.buttons[event.button] = event.pos
                if 1 in self.buttons: # left click
                    mx = self.motion.pos[0]
                    my = self.motion.pos[1]
                    if self.click_in_viewport(mx,my) and self.clickState == "MoveSelect":
                        x,y,z = self.vpClickToCoords(mx, my, self.currentZlevel)
                        self.pickDestination(x,y,z)
                        self.clickState = None
                        self.selectedPlayer = None
                    elif self.click_in_viewport(mx,my):
                        x,y,z = self.vpClickToCoords(mx, my, self.currentZlevel)
                        player_uuid = self.checkMapForPlayer(x,y,z)
                        mob_uuid = self.checkMapForMob(x, y, z)
                        if player_uuid:
                            self.center_vp_on(x, y, z)
                            #print "You clicked on a player"
                            self.selectedPlayer = player_uuid
                            self.clickState = "MoveSelect"
                        elif mob_uuid:
                            #print "You CLICKED ON A MOB"
                            self.center_vp_on(x, y, z)
                            self.selectedMob = mob_uuid
                            # Add a panel that will show the mob details / stats
                            self.updateClickedMob()
                                                     
                        #self.checkMap(x,y,z)
                        #self.updateClickMap(x, y, z, 2)
                    elif self.endTurnButton.pressed(mx, my):
                        self.pressedButton = "End Turn"
                    elif self.checkPlayerPortraitClicks(mx, my):
                        pass
                    elif self.checkMobPortraitClicks(mx, my):
                        pass
                    
                        
                elif 3 in self.buttons: # right click
                    mx = self.motion.pos[0]
                    my = self.motion.pos[1]
                    if self.click_in_viewport(mx,my):
                        x,y,z = self.vpClickToCoords(mx, my, self.currentZlevel)
                        self.checkMap(x,y,z)
                        self.updateClickMap(x, y, z, 0)
                
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
                
    def lookupPlayerByUUID(self,uuid):
        for p in self.players:
            if p.uuid == uuid:
                #print "Matching player found with the same uuid"
                return p
        return None
    
    def lookupMobByUUID(self,uuid):
        for m in self.mobs:
            if m.uuid == uuid:
                #print "Matching mob found with the same uuid"
                return m
        return None
    
    
    
    def pickDestination(self,x,y,z):
        if self.is_blocked(int(x), int(y), z) or self.is_foggy(int(x), int(y), z):
            pass
        elif self.selectedPlayer:
            p = self.lookupPlayerByUUID(self.selectedPlayer)
            if p:
                start = (p.x,p.y,p.z) # start position
                end = (x,y,z) #destination
                path = self.compute_path(start, end)
                if path:
                    p.pathlines = path
                    p.selected = False
         
    def updateClickedMob(self):
        for m in self.mobs:
            if self.selectedMob == m.uuid:
                m.selected = True
            else:
                m.selected = False
    
    def checkMapForPlayer(self,x,y,z):
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
     
    def checkMapForMob(self,x,y,z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
        for m in self.mobs:
            if m.x == x and m.y == y and m.z == z:
                m.selected = True
                return m.uuid
        return None
    
    def logic(self):
        self.startXTile = math.floor(float(self.vpCoordinate[0]) / self.tw)
        self.startYTile = math.floor(float(self.vpCoordinate[1]) / self.tw)
        self.updateCombatLog()
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
        if self.clickState == "MoveSelect":
            size, hotspot, cursor, mask = self.Cursors.SetCursor(self.Cursors.move)
            pygame.mouse.set_cursor(size, hotspot, cursor, mask)
        else:
            size, hotspot, cursor, mask = self.Cursors.SetCursor(self.Cursors.arrow)
            pygame.mouse.set_cursor(size, hotspot, cursor, mask)
        
    def successors(self, x,y,z):
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
                    if self.is_blocked(x,y,z) or self.is_foggy(x, y, z):
                        continue
                    else:
                        slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist
    
    def pick_wall_tile(self, tiles):
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
    
    def get_neighbors_values(self, x,y,z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
        templist = [[ 0 for i in range(3)] for j in range(3)]  #
        xx = 0
        for drow in (-1, 0, 1):
            yy = 0
            for dcol in (-1, 0, 1):
                newrow = x + drow
                newcol = y + dcol
                
                if (newrow, newcol, z) in self.vp:
                    if drow == 0 and dcol == 0:
                        #print "center"
                        pass
                    elif self.is_blocked(newrow,newcol,z) or self.is_foggy(newrow, newcol, z):
                        #print "Blocked or foggy"
                        pass
                    else:
                        #print "Floor"
                        templist[xx][yy] = 1
                yy = yy + 1
            xx = xx + 1
        #pprint(templist)
        return templist
    
    def find_moves(self, x,y,z,movement):
        slist = []
        movement_range = range(-movement,movement+1)
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
                    if self.is_blocked(newrow,newcol,z):
                        pass
                    else:
                        slist.append((newrow, newcol, z)) # fire the move in the queue
        return slist
    
    def find_fov(self, x,y,z,size):
        slist = []
        size_range = range(-size,size+1)
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
    
    def advanceTurn(self):
        # process the players moves, will have to base this on initiative at some point.
        self.turn = self.turn + 1
        self.log.append("Advancing to turn " + str(self.turn))
        #print str(self.turn)
        for p in self.players:
            #print p.name
            p.fov.update(self.find_fov(p.x,p.y,p.z, 5))
            if p.pathlines:
                #print p.name + "is processing a move"
                move = p.pathlines.pop(0)
                if (p.x, p.y, p.z) == move:
                    if p.pathlines:
                        move = p.pathlines.pop(0) 
                p.x, p.y, p.z = move
                p.fov.update(self.find_fov(p.x,p.y,p.z, 5))
            #manage players running into items ie: stairs
            item_list = self.getTileItems(p.x,p.y,p.z)
            for item in item_list:
                if item == "Stairs":
                    
                    # attempt to move the player to the new z level
                    x,y,z = self.find_stairs_on(p.z+1)
                    p.x, p.y, p.z = (x-1, y-1, p.z+1)
                    print "Player is on some stairs."
                    text = p.name + " has walked up some stairs."
                    self.log.append(text)
                    p.fov.update(self.find_fov(p.x,p.y,p.z, 5))
                    self.center_vp_on(p.x, p.y, p.z)
                
        # mob movement
        self.MobAIMove()    
        for m in self.mobs:
            #print m.name
            if m.pathlines:
                m.fov.update(self.find_fov(m.x,m.y,m.z,5))
                #print m.name + "is processing a move"
                move = m.pathlines.pop(0)
                if (m.x, m.y, m.z) == move:
                    if m.pathlines:
                        move = m.pathlines.pop(0)
                m.x, m.y, m.z = move
                m.fov.update(self.find_fov(m.x,m.y,m.z, 5))
                
        
        
    def getTileItems(self,x,y,z):
            return self.mapdata[z][x][y].content
                    
    def checkMobCollision(self,x,y,z):
        for p in self.players:
            area = self.successors(p.x, p.y, p.z)
            for a in area:
                if a == (x,y,z):
                    return True
        return False
    
    def MobAIMove(self):
        for m in self.mobs:
            for p in self.players:
                if self.is_in_FOV(m, p):
                    if self.checkMobCollision(m.x,m.y,m.z):
                        self.log.append("Combat Started Rolling Initiative:")
                        p.pathlines = []
                        m.pathlines = []
                        # Combat 
                        #print "COLLISION FOUND"
                        player_initiative = rollD20()
                        mob_initiative = rollD20()
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
                                    pass
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
                                    pass
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
                            start = (m.x,m.y,m.z) # start position
                            end = (p.x, p.y, p.z)
                            templist = self.compute_path(start, end)
                            if templist:
                                m.pathlines = templist
                
        for p in self.players[:]:
            if p.alive:
                #alive check
                pass
            else:
                self.deadPlayers.append((p.x,p.y,p.z))
                self.players.remove(p)
        for m in self.mobs[:]:
            if m.alive:
                #mobs alive
                pass
            else:
                self.deadMobs.append((m.x,m.y,m.z))
                self.mobs.remove(m)
                
    def handle_buttons(self):
        if self.pressedButton != None:
            if self.pressedButton == "End Turn":
                self.advanceTurn()
                self.pressedButton = None
    
    def handle_fog_of_war(self):
        for p in self.players:
            for (x,y,z) in p.fov:
                self.unFog(x, y, z)
        
    def drawMap(self):
        for x in range(self.mapw):
        #for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
            #for y in range(int(self.startYTile), int(self.startYTile + self.numYTiles)):
            for y in range(self.maph):
                if (x,y,self.currentZlevel) in self.vp:
                    if self.is_foggy(x, y, self.currentZlevel): # fog
                        self.tiledBG.blit(self.floor_images[2], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
                    elif self.mapdata[self.currentZlevel][x][y].blocked: # wall
                        templist = self.get_neighbors_values(x,y,self.currentZlevel)
                        value = self.pick_wall_tile(templist)
                        self.tiledBG.blit(self.wall_images[value], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
                    else: # floor
                        self.tiledBG.blit(self.floor_images[0], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
                #draw items on the tiles
                for item in self.mapdata[self.currentZlevel][x][y].content:
                    if item == "Stairs":
                        self.tiledBG.blit(self.floor_images[1], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
    
    def drawClickMap(self):
        for x in range(self.mapw):
            for y in range(self.maph):
                if (x,y,self.currentZlevel) in self.vp:
                        if self.clickdata[self.currentZlevel][x][y] != 0:
                            self.tiledBG.blit(self.images[self.clickdata[self.currentZlevel][x][y]], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
                
    def drawPathLines(self):
        for p in self.players:
            if p.pathlines:
                for l in p.pathlines:
                    for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
                        for y in range(int(self.startYTile), int(self.startYTile + self.numYTiles)):
                            if l[0] == x and l[1] == y and l[2] == self.currentZlevel:
                                #print "Haulin ass getting paid"
                                self.tiledBG.blit(self.images[4], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
    
    def drawCharBox(self):
        rectangle = pygame.Rect(int(self.charBoxLeft + self.tw) ,int(self.charBoxTop + self.tw),int(self.charBoxWidth),int(self.charBoxHeight))
        gray = (115,115,115)
        green = (0,255,0)
        red = (255,0,0)
        self.screen.fill(gray, rectangle)
        count = 0
        for p in self.players:
            p.portrait_rect.topleft = rectangle.topleft
            p.portrait_rect.left = p.portrait_rect.left + p.portrait_rect.width * count#(p.portrait_rect.width * count, ry )
            self.screen.blit(p.portrait, p.portrait_rect ) # (self.vpCoordinate[0] - (p.x * self.tw), (self.vpCoordinate[1] - (p.y * self.tw))) + self.vpDimensions)
            if p.selected == True:
                pygame.draw.rect(self.screen, green, p.portrait_rect, 5)
            count = count + 1
        
        count = 0
        for m in self.mobs:
            m.portrait_rect.topleft = rectangle.topleft
            m.portrait_rect.top = m.portrait_rect.top + m.portrait_rect.height
            m.portrait_rect.left = m.portrait_rect.left + m.portrait_rect.width * count#(p.portrait_rect.width * count, ry )
            self.screen.blit(m.portrait, m.portrait_rect ) # (self.vpCoordinate[0] - (p.x * self.tw), (self.vpCoordinate[1] - (p.y * self.tw))) + self.vpDimensions)
            if m.selected == True:
                pygame.draw.rect(self.screen, red, m.portrait_rect, 5)
            count = count + 1
            
    def drawPossibleMoves(self):
        #print "MOVES:"
        #pprint(self.moves)
        for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
            for y in range(int(self.startYTile), int(self.startYTile + self.numYTiles)):
                if (x,y,self.currentZlevel) in self.moves:
                    #print "x,y are in the set"
                    self.tiledBG.blit(self.images[3], ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw))
    
    def getPossibleMoves(self,x,y,z):
        successors_list = self.find_moves(x, y, z,2)
        new_set = Set()
        new_set.update(successors_list)
        return new_set    
        
    def render(self):
        self.screen.fill((0, 0, 0))
        self.drawMap()
        self.drawClickMap()
        self.drawPossibleMoves()
        self.drawPathLines()
        self.screen.blit(self.tiledBG, self.vpRenderOffset, (self.vpCoordinate[0] - (self.startXTile * self.tw), (self.vpCoordinate[1] - (self.startYTile * self.tw))) + self.vpDimensions)
        
        self.drawPlayersAndMobs()
        self.screen.blit(self.endTurnButton.image, self.endTurnButton.rect)
        self.screen.blit(self.arial_font.render('coordinates: ' + str(self.vpCoordinate[0]/self.tw) + ", " + str(self.vpCoordinate[1]/self.tw) + " Z: " + str(self.currentZlevel), True, (255,255,255)), self.statsOffset)
        self.screen.blit(self.arial_font.render('State: ' + str(self.clickState), True, (255,255,255)), self.clickStateOffset)
        self.drawCharBox()
        self.app.paint()
        if self.win:
            self.screen.blit(self.arial_font.render('You Win!', True, (255,255,255)), (self.ww/2,self.wh/2))
        elif self.win == False:
            self.screen.blit(self.arial_font.render('You Lose!', True, (255,255,255)), (self.ww/2,self.wh/2))
        self.mainclock.tick(self.FPS)
        pygame.display.flip()
    
    def in_vp(self,x,y,z):
        #coord to vp
        #pprint((x,y,z))
        if (x,y,z) in self.vp:
            return True
        else:
            return False
    
    def drawPlayersAndMobs(self):
        for p in self.players:
            if (p.x, p.y, p.z) in self.vp:
                self.screen.blit(p.image, self.vpRenderOffset, (self.vpCoordinate[0] - (p.x * self.tw), (self.vpCoordinate[1] - (p.y * self.tw))) + self.vpDimensions)
                self.screen.blit(self.arial_font.render(str(p.hp), True, (255,0,0)), ((p.x - self.startXTile) * self.tw + self.tw, (p.y - self.startYTile) * self.tw + self.tw) )
                if p.selected :
                    green = (0,255,0)
                    rect = pygame.Rect(((p.x * self.tw) - self.vpCoordinate[0]) + self.tw, ((p.y * self.tw) - self.vpCoordinate[1]) + self.tw , self.tw, self.tw)
                    pygame.draw.rect(self.screen, green, rect, 3)
                    
        
        for m in self.mobs:
            if (m.x, m.y, m.z) in self.vp and self.is_foggy(m.x, m.y, m.z) == False:
                self.screen.blit(self.arial_font.render(str(m.hp), True, (255,0,0)), ((m.x - self.startXTile) * self.tw + self.tw, (m.y - self.startYTile) * self.tw + self.tw) )
                self.screen.blit(m.image, self.vpRenderOffset, (self.vpCoordinate[0] - (m.x * self.tw), (self.vpCoordinate[1] - (m.y * self.tw))) + self.vpDimensions)
                if m.selected :
                    red = (255,0,0)
                    rect = pygame.Rect(((m.x * self.tw) - self.vpCoordinate[0]) + self.tw, ((m.y * self.tw) - self.vpCoordinate[1]) + self.tw , self.tw, self.tw)
                    pygame.draw.rect(self.screen, red, rect, 3)
                    
        for (x,y,z) in self.deadPlayers:
            if (x,y,z) in self.vp:
                self.screen.blit(self.dead_images[0], self.vpRenderOffset, (self.vpCoordinate[0] - (x * self.tw), (self.vpCoordinate[1] - (y * self.tw))) + self.vpDimensions)
    
        for (x,y,z) in self.deadMobs:
            if (x,y,z) in self.vp:
                self.screen.blit(self.dead_images[2], self.vpRenderOffset, (self.vpCoordinate[0] - (x * self.tw), (self.vpCoordinate[1] - (y * self.tw))) + self.vpDimensions)
                
        
    def is_in_FOV(self, mob, player):
        if (player.x, player.y, player.z) in mob.fov:
            #print "Player is in movement range"
            return True
        return False
                    
    def checkMap(self, x, y, zlevel):
        #print "x:", str(x) + "y:", str(y) + "z:", str(zlevel)
        return self.mapdata[zlevel][int(x)][int(y)].value
    
    def checkClickMap(self, x, y, z):
        #print "x:", str(x) + "y:", str(y) + "z:", str(z)
        return self.mapdata[z][int(x)][int(y)]
    
    def updateMap(self, x,y,z,value):
        self.mapdata[z][int(x)][int(y)].value = value
        
    def unFog(self, x,y,z):
        self.mapdata[z][x][y].fog = False
        
    def updateClickMap(self,x,y,z,value):
        self.clickdata[z][int(x)][int(y)] = value
        self.moves = self.getPossibleMoves(int(x),int(y), z)
        
    def set_not_fullscreen(self):
        newwidth = math.floor(int(0.8 * self.ww) / self.tw)
        newheight = math.floor(int(0.8 * self.wh) / self.tw)
        self.statsOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw)
        self.clickStateOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 2)
        self.vpDimensions = (newwidth * self.tw, newheight * self.tw) # resolution of the view port
        self.numXTiles = int(math.ceil(int(self.vpDimensions[0]) / self.tw)) # tiles to be shown at one time for X
        self.numYTiles = int(math.ceil(int(self.vpDimensions[1]) / self.tw)) # tiles to be shown at one time for y
        self.charBoxTop = math.floor(int(0.8 * self.wh) / self.tw) * self.tw + self.tw  # rectangle for the char box
        self.charBoxLeft = 0
        self.charBoxWidth = math.floor(int(0.8 * self.ww) / self.tw) * self.tw
        self.charBoxHeight = math.floor(int(0.2 * self.wh) / self.tw) * self.tw
        self.button_offset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 3)
        self.endTurnButton.setCords(self.button_offset[0], self.button_offset[1])
        self.combatLogOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 20)
        self.combatLogWidth = self.ww - self.combatLogOffset[0]
        self.combatLogHeight = self.wh - self.combatLogOffset[1]
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1,valign=-1)
        self.gui_container.add(self.CombatLog,self.combatLogOffset[0],self.combatLogOffset[1])
        self.app.init(self.gui_container)
        self.tiledBG = pygame.Surface((self.numXTiles * self.tw, self.numYTiles * self.tw)).convert()
        self.recalc_vp()
    
    def set_fullscreen(self):
        pygame.display.set_mode((self.fsw, self.fsh), FULLSCREEN, 32)
        newwidth = math.floor(int(0.8 * self.fsw) / self.tw)
        newheight = math.floor(int(0.8 * self.fsh) / self.tw)
        self.statsOffset = (math.floor(int(0.8 * self.fsw) / self.tw) * self.tw + self.tw, self.tw)
        self.clickStateOffset = (math.floor(int(0.8 * self.fsw) / self.tw) * self.tw + self.tw, self.tw * 2)
        self.vpDimensions = (newwidth * self.tw, newheight * self.tw) # resolution of the view port
        self.numXTiles = int(math.ceil(int(self.vpDimensions[0]) / self.tw)) # tiles to be shown at one time for X
        self.numYTiles = int(math.ceil(int(self.vpDimensions[1]) / self.tw)) # tiles to be shown at one time for y
        self.charBoxTop = math.floor(int(0.8 * self.fsh) / self.tw) * self.tw + self.tw  # rectangle for the char box
        self.charBoxLeft = 0
        self.charBoxWidth = math.floor(int(0.8 * self.fsw) / self.tw) * self.tw
        self.charBoxHeight = math.floor(int(0.2 * self.fsh) / self.tw) * self.tw
        self.button_offset = (math.floor(int(0.8 * self.fsw) / self.tw) * self.tw + self.tw, self.tw * 3)
        self.endTurnButton.setCords(self.button_offset[0], self.button_offset[1])
        self.combatLogOffset = (math.floor(int(0.8 * self.fsw) / self.tw) * self.tw + self.tw, self.tw * 20)
        self.combatLogWidth = self.fsw - self.combatLogOffset[0]
        self.combatLogHeight = self.fsh - self.combatLogOffset[1]
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1,valign=-1)
        self.gui_container.add(self.CombatLog,self.combatLogOffset[0],self.combatLogOffset[1])
        self.app.init(self.gui_container)
        self.tiledBG = pygame.Surface((self.numXTiles * self.tw, self.numYTiles * self.tw)).convert()
        self.recalc_vp()
    def screen_resize(self, w,h):
        self.ww = w
        self.wh = h
        pygame.display.set_mode((w, h), RESIZABLE)
        newwidth = math.floor(int(0.8 * w) / self.tw)
        newheight = math.floor(int(0.8 * h) / self.tw)
        self.statsOffset = (math.floor(int(0.8 * w) / self.tw) * self.tw + self.tw, self.tw)
        self.clickStateOffset = (math.floor(int(0.8 * w) / self.tw) * self.tw + self.tw, self.tw * 2)
        self.vpDimensions = (newwidth * self.tw, newheight * self.tw) # resolution of the view port
        self.numXTiles = int(math.ceil(int(self.vpDimensions[0]) / self.tw)) # the number of tiles to be shown at one time for X
        self.numYTiles = int(math.ceil(int(self.vpDimensions[1]) / self.tw)) # the number of tiles to be shown at one time for y
        self.charBoxTop = math.floor(int(0.8 * self.wh) / self.tw) * self.tw + self.tw  # rectangle for the char box
        self.charBoxLeft = 0
        self.charBoxWidth = math.floor(int(0.8 * w) / self.tw) * self.tw
        self.charBoxHeight = math.floor(int(0.2 * h) / self.tw) * self.tw
        self.button_offset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 3)
        self.endTurnButton.setCords(self.button_offset[0], self.button_offset[1])
        self.combatLogOffset = (math.floor(int(0.8 * self.ww) / self.tw) * self.tw + self.tw, self.tw * 20)
        self.combatLogWidth = self.ww - self.combatLogOffset[0]
        self.combatLogHeight = self.wh - self.combatLogOffset[1]
        self.app = gui.App()
        self.gui_container = gui.Container(align=-1,valign=-1)
        self.gui_container.add(self.CombatLog,self.combatLogOffset[0],self.combatLogOffset[1])
        self.app.init(self.gui_container)
        self.tiledBG = pygame.Surface((self.numXTiles * self.tw, self.numYTiles * self.tw)).convert()
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
        MAX_ROOMS = 13
        ROOM_MIN_SIZE = 5
        ROOM_MAX_SIZE = 15
        starting_floor = True
        
        for z in range(self.zlevels):
            num_rooms = 0
            rooms = []
            for r in range(MAX_ROOMS):
                #random width and height
                w = randrange(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                h = randrange(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
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
                        stairs = "Stairs"        
                        self.mapdata[z][new_x-1][new_y-1].content.append(stairs)
                        if starting_floor:
                            starting_floor = False
                            self.players.append(Player("Jason", "Coder", new_x,new_y,z))
                            self.players.append(Player("Steve", "Civilian", new_x+1,new_y+1,z))
                            for p in self.players:
                                p.fov.update(self.find_fov(p.x,p.y,p.z,5))
                            
                            
                        #this is the first room, where the player starts at
                    #    player.x = new_x
                    #    player.y = new_y
                    else:
                        self.mobs.append(Mob("Dave", "Neuromancer", new_x,new_y,z))
                        self.mobs.append(Mob("Gimpy", "Pest", new_x+1,new_y+1,z))
                        for m in self.mobs:
                            m.fov.update(self.find_fov(m.x,m.y,m.z,5))
                    #center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms-1].center()
         
                        #draw a coin (random number that is either 0 or 1)
                        if randrange(0, 1) == 1:
                            #first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y,z)
                            self.create_v_tunnel(prev_y, new_y, new_x,z)
                        else:
                            #first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x,z)
                            self.create_h_tunnel(prev_x, new_x, new_y,z)
         
                    #finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1
                    
    def find_stairs_on(self,z):
        for x in range(self.mapw):
            for y in range(self.maph):
                for i in self.mapdata[z][x][y].content:
                    if i == "Stairs":
                        return (x,y,z)
        return None
            
    def is_blocked(self, x, y, z):
        #first test the map tile
        #print "x: ", str(x) + " y:", str(y) + " z:", str(z)
        return self.mapdata[z][x][y].blocked
    
    def is_foggy(self, x, y, z):
        #pprint((x,y,z))
        return self.mapdata[z][x][y].fog
    
    def is_sight_blocked(self,x,y,z):
        return self.mapdata[z][x][y].blocked_sight
    def run(self):
        """ This is the main function """
        while self.running:
            self.logic()
            self.render()
            
        pygame.quit()
        sys.exit()

def rollD20():
    return randint(1,20) 
       
if __name__ == '__main__':
    TB = Game()
    TB.run()