import random
import logging
import time
from math import sqrt
from collections import defaultdict

from tkinter import Tk
from PIL import Image
from PIL import ImageTk
 

from uf import UF
from gui import MainPanel, HeaderPanel, MenuBar
from config import *

def load_mod(mod):
    for k,v in mods_config[mod].items():
        globals()[k]=v

class Candy:
    thumbnail = None
    number = 0 #number of the chocoFrogCard
    metal = 1 #bronze : 1, silver : 2, gold : 3
    def __init__(self):
        if not self.thumbnail:
            self.thumbnail = ImageTk.PhotoImage(Image.open(
            "data/candies/%s.png" % self.__class__.__name__).resize(
                (TILE_WIDTH, TILE_HEIGHT), Image.ANTIALIAS))
            logging.debug("thumbnail instantciated for %s ", self.__class__)        

    def thumb(self):
        return self.thumbnail

    def reward(self, n, m, k):
        print( self.__class__.__name__, self.number, self.metal)
        '''Class method that calculate the reward, in points, when k candies of the current class are destroyed by the users'''
        return self.number * pow(1+self.metal/(n+m), k)

class NoCard(Candy):
    pass

class AlbericGrunnion(Candy):
    number = 97

class AlbusDumbledore(Candy):
    number = 101

class GlendaChittock(Candy):
    number = 23

class HonoriaNutcombe(Candy):
    number = 55 

class LeopoldinaSmethwyck(Candy):
    number = 70

class MertonGraves(Candy):
    number = 94

class MirandaGoshawk(Candy):
    number = 40

class MyronWagtail(Candy):
    number = 70

class NewtScamander(Candy):
    number = 19

class PerpetuaFancourt(Candy):
    number = 25 

class Engine(Tk):
    candies_class = [AlbericGrunnion, AlbusDumbledore, GlendaChittock,
            HonoriaNutcombe, LeopoldinaSmethwyck,MertonGraves, MirandaGoshawk,
            MirandaGoshawk, MyronWagtail, NewtScamander, PerpetuaFancourt]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_mod(DEFAULT_MOD)

        self.menuBar = MenuBar(self)
        self.configure(menu=self.menuBar)
        
        self.mainPanel = None

        self.headerPanel = HeaderPanel(self, self)
        self.headerPanel.show()

       

        self.new_game()

    def prepare(self):
        self.grid = [[None for j in range(self.m)] for i in range(self.n)] 

        #compute the number of card in order to have enough chance of playing
        c = min(2*round(pow( 6/(self.n*self.m), -(1/3))), len(self.candies_class))
        self.candies_class=self.candies_class[0:c]
        logging.info('Number of class card : %d' % c)

        self.candies_gr = {} 
        self.candies_uf = UF(self.n*self.m)

        self.empty_cells = [set() for i in range(self.n)]   
        self.exists_empty_cells = True 

        #Gui link
        self.timer, self.points = 0, 0
        
        
        #Flag in order to disable user interaction, mainly use during gravity 
        self.user_can_act = True
        
        self.init_grid()
        self.reset_if_needed()
        
        #Start of the game
        self.after(DELAY_TICK, self.tick)

    #TODO ensure that there is at least one destruct allowed
    def init_grid(self):
        for i in range(self.n):
            for j in range(self.m):
                self.grid[i][j]= random.choice(self.candies_class)() 
                self.mainPanel.set(i,j,self.grid[i][j])
        self.exists_empty_cells = False
        self.make_groups() 

    def new_game(self, mod=DEFAULT_MOD):
        load_mod(mod)
        self.n= N
        self.m = M

        if self.mainPanel:
            self.mainPanel.hide()
        self.mainPanel = MainPanel(self, self, self.n, self.m)
        self.mainPanel.show()
        
        self.prepare()

        self.headerPanel.reset_()


    def reset_if_needed(self):
        while True:
            if self.candies_uf.count() < (self.n*self.m) / THRESHOLD_DESTRUCT:
                return True
            
            for gr in self.candies_gr.values():
                if len(gr) > THRESHOLD_DESTRUCT:
                    return True
            
            self.init_grid()
            logging.info('No solutions left : grid has been reset')     

    def gravity_os(self):
        """ 
            One shot implementation of the gravity
            @return the list of cell that have change due to the gravity     
        """
        cells_updated = []


        if not self.exists_empty_cells:
            return cells_updated
        
        self.exists_empty_cells = False

        #row : empty cell at line i
        for (i,row) in enumerate(self.empty_cells) :
            #new empty cells at line i after the current iteration
            n_row = set()

            #self.grid[i][j] is a NoCard instance
            for j in row:
                if i != self.n-1:
                    #cell above falls into the empty cell (i,j)
                    self.grid[i][j]=self.grid[i+1][j]
                    #cell above is now empty
                    self.grid[i+1][j] = NoCard()
                   
                    #we add the new empty cells in order to process then later
                    self.empty_cells[i+1].add(j)
                    if isinstance(self.grid[i][j], NoCard):
                        n_row.add(j)
                    
                    #we update the cells_updated in order to tell the gui which cell to redraw 
                    cells_updated.extend([(i,j),(i+1,j)])
                else: 
                    self.grid[i][j]= random.choice(self.candies_class)()
                    
                    #we update the cells_updated in order to tell the gui which cell to redraw 
                    cells_updated.append((i,j))
            
            #we commit the new empty cells
            self.empty_cells[i] = n_row
            
            #we update the empty cells flag
            if n_row:
                self.exists_empty_cells = True
                        
        return cells_updated            
    
    def is_in_grid(self, z):
        x,y = z
        return 0<=x and x<self.n and 0<=y and y<self.m

    def neighbourgs(self, i, j):
        xs, ys = [i-1, i+1], [j-1,j+1]
        return filter(lambda z: self.is_in_grid(z), 
                [(i-1,j),(i,j-1),(i+1,j),(i,j+1)] )
    
    def make_groups(self):
        self.candies_uf = UF(self.n*self.m)
        self.candies_gr = defaultdict(list)

        for i in range(self.n):
            for j in range(self.m):
                for (x,y) in self.neighbourgs(i,j):
                    if self.grid[i][j].__class__.__name__ == self.grid[x][y].__class__.__name__:
                        self.candies_uf.union(i*self.n+j, x*self.n+y)
                        
        for i in range(self.n):
            for j in range(self.m):
                self.candies_gr[self.candies_uf.find(i*self.n+j)].append((i,j))

    def to_destruct(self, i, j):
        ''' Output the set of candies that can be destruct during 
        a stroke at (i,j)'''
        gr_id = self.candies_uf.find(i*self.n+j)
        return self.candies_gr[gr_id]
    
    def points_of(self, to_destruct):
        if not to_destruct:
            return 0
        
        k = len(to_destruct)
        i,j = to_destruct[0]
        return self.grid[i][j].reward(self.n, self.m, k)

    #refinement do the destruction in star order
    def _destruct(self, i, j):
        '''Try to destruct the (i,j) candy in the grid, 
        if it succeeds it returns the number of points won'''
        to_destruct = self.to_destruct(i,j)
        points = self.points_of(to_destruct) 

        if len(to_destruct) < THRESHOLD_DESTRUCT:
            self.exists_empty_cells = True    
            return 0 
        
        logging.info("destruct")
        for (x,y) in to_destruct:
            self.grid[x][y] = NoCard()     
            self.mainPanel.set(x,y,self.grid[x][y])

            #we update the empty cells in order to apply gravity
            self.empty_cells[x].add(y)

        self.exists_empty_cells = True    
        return points
    
    def gravity(self):
        for (x,y) in self.gravity_os():
            self.mainPanel.set(x,y, self.grid[x][y])
        
        if self.exists_empty_cells:    
            self.after(DELAY_GRAVITY, self.gravity)
        else:
            self.make_groups()
            self.user_can_act = True 

    def destruct(self, i, j):
        self.tick(0)
        if not self.user_can_act:
            return False
         
        self.user_can_act = False
        tmp_points = self._destruct(i,j)
        if self.exists_empty_cells:    
            self.after(DELAY_GRAVITY, self.gravity)
        
        #update of the points 
        self.points += tmp_points 
        self.headerPanel.set_points(self.points, THRESHOLD_ROUND)
        
        self.reset_if_needed()

    def tick(self, delay=DELAY_TICK):
        if delay :
            self.timer += DELAY_TICK
            self.headerPanel.set_timer(self.timer, DELAY_ROUND)
        
        if self.timer >= DELAY_ROUND:
            self.user_can_act = False
            if self.points < THRESHOLD_ROUND:
                self.headerPanel.end_lost()
                logging.info('Game over!')
            else:
                self.headerPanel.end_won()
                logging.info('Congratulations : you win !')
            return False

        if delay: 
            self.after(DELAY_TICK, self.tick)

        
