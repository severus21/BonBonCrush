from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

from config import *

class Panel(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        
    def hide(self):
        self.grid_forget()
        
    def show(self):
        self.grid()

class Tile(Panel):
    candies_thumbs = {
    }

    def __init__(self, app, master, n, m, i, j, *args, **kwargs):
        super().__init__(master, width=TILE_WIDTH+TILE_BORDER, 
        height=TILE_HEIGHT+TILE_BORDER, *args, **kwargs)
        
        self.app = app
        self.n = n
        self.m = m
        self.i = i
        self.j = j

        self.candy_thumb = None
        
        self.thumbnail = Canvas(self, bg="white", width=TILE_WIDTH, 
                height=TILE_HEIGHT)
        self.thumbnail.pack()
        self.thumbnail.bind('<Button-1>', lambda x: 
                self.app.destruct(self.n-i-1, self.m-j-1) ) 
            
    def show(self):
        self.thumbnail.pack(padx=TILE_BORDER/2, pady = TILE_BORDER/2)
    
    def hide(self):
        self.configure(bg="white")
        self.thumbnail.pack_forget()
        
    
    def set(self, candy):
        if self.candy_thumb == candy.thumb():
            return True
        

        self.candy_thumb = candy.thumb() 

        offset_width = (TILE_WIDTH - self.candy_thumb.width()) / 2
        offset_height = (TILE_HEIGHT- self.candy_thumb.height()) / 2
            
        self.thumbnail.delete("all")
        self.thumbnail.create_image(offset_width, offset_height, anchor=NW, image=self.candy_thumb) 
        self.thumbnail.pack(padx=TILE_BORDER/2, pady = TILE_BORDER/2)

        return None
       
class MainPanel(Panel):
    def __init__(self, app, master, n, m, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        
        self.tiles=[[Tile(app, self, n, m, i, j) for j in range(m)] for i in range(n)]
        self.n=n
        self.m=m

        for i in range(n):
            for j in range(m):
                self.tiles[i][j].grid(row=i, column=j)
                self.tiles[i][j].show()

    def set(self, i,j, candy):
        self.tiles[self.n-i-1][self.m-j-1].set(candy)

class HeaderPanel(Panel):
    def __init__(self, app, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        

        self.status = Frame(self)
        self.status.pack()

        self.timer = 0
        self.label_timer = Label(self.status)
        self.label_timer.configure(text='Time 0', font=DEFAULT_FONT)
        self.label_timer.grid(row=0, column=0)
        
        self.points = 0
        self.label_points = Label(self.status)
        self.label_points.configure(text='Points 0', font=DEFAULT_FONT)
        self.label_points.grid(row=0, column=1)
        
        self.label_alert = Label(self)
        self.label_alert.configure(text='', font=ALERT_FONT)
        
        self.reset = Frame(self)
        self.label_reset = Label(self)
    
    def reset_(self):
        self.timer = 0
        self.label_timer.configure(text='Time 0', font=DEFAULT_FONT)

        self.points = 0
        self.label_points.configure(text='Points 0', font=DEFAULT_FONT)

    def set_timer(self, timer, delay):
        '''
        timer - time in ms
        '''
        if self.timer == timer:
            return True
        
        self.label_timer.configure(text='Time %d/%d' % ((timer/1000),(delay/1000)) )
        self.timer = timer
   
    def set_points(self, points, treshold):
       if self.points == points:
           return True

       self.label_points.configure(text='Points %d/%d' % (points,treshold))
       self.points = points
       

    def end_won(self):
        self.label_alert.configure(text='Congratulations : you win!')
        self.label_alert.pack()

    def end_lost(self):
        self.label_alert.configure(text='Game over...')
        self.label_alert.pack()

class MenuBar(Menu):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, font=DEFAULT_FONT, *args, **kwargs)
        self.app = app

        game_menu = Menu(self, font=DEFAULT_FONT)
        game_menu.add_command(label='New Game - Easy', command=lambda: self.app.new_game(Mod.EASY) )
        game_menu.add_command(label='New Game - Normal', command=lambda: self.app.new_game(Mod.NORMAL) )
        game_menu.add_command(label='New Game - Hard', command=lambda: self.app.new_game(Mod.HARDCORE) )
        self.add_cascade(label='Game', menu=game_menu)



