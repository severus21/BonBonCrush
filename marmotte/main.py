import sys 
import logging

from engine import Engine
from config import *

logging.basicConfig(
    stream= sys.stdout,
    format='%(asctime)s  %(levelname)s  %(filename)s %(funcName)s %(lineno)d %(message)s',
    level=logging.INFO)

engine = Engine()
engine.title("BonBonCrush")
engine.mainloop()
