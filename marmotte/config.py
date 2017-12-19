from enum import IntEnum

## ENGINE config 
'''
Delay, in ms, of one tick of the gravity event.
'''
DELAY_GRAVITY = 50

'''
Delay, in ms, of one tick of the system in order to increase time,
to check to handle the termination of the game.
'''
DELAY_TICK = 100

### Game mod config
class Mod(IntEnum):
    EASY = 0
    NORMAL = 1
    HARDCORE = 2

DEFAULT_MOD = Mod.NORMAL

'''
Number of candies per line.
(ex) N = 5

Number of lines of candies.
(ex) M = 5

Minimal number of candies linked together( neighbourhood relationship)
in order to allow the destruction by the user.
(ex) THRESHOLD_DESTRUCT = 3


Duration of the one round of the game in ms.
(ex) DELAY_ROUND = 30000 

Minimal number of points needed in order to win a round.
(ex) THRESHOLD_ROUND = 2000
'''

mods_config = {
    Mod.EASY:{
        'N' : 5,
        'M' : 5,
        'THRESHOLD_DESTRUCT' : 3,
        'DELAY_ROUND' : 30000, 
        'THRESHOLD_ROUND' : 2000,
        },
    Mod.NORMAL:{
        'N' : 8,
        'M' : 8,
        'THRESHOLD_DESTRUCT' : 3,
        'DELAY_ROUND' : 30000, 
        'THRESHOLD_ROUND' : 2000,
        },
    Mod.HARDCORE:{
        'N' : 10,
        'M' : 10,
        'THRESHOLD_DESTRUCT' : 3,
        'DELAY_ROUND' : 30000, 
        'THRESHOLD_ROUND' : 2000,
        },
}




### GUI config 

'''
With of a tile, in px,  a tile is the GUI component displaying a candy.
'''
TILE_WIDTH = 150

'''
Height of a tile, in px,  a tile is the GUI component displaying a candy.
'''
TILE_HEIGHT = 150

'''
Half of the space, in px,  between to candies in the GUI panel.
'''
TILE_BORDER = 10

'''
Default font for texts in the GUI.
'''
DEFAULT_FONT = ("Helvetica", 14) 

'''
Font used when displaying alerts, ex 'Game over...'.
'''
ALERT_FONT = ("Helvetica", 30) 


