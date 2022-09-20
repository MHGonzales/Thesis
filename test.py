""" servo pyfirmata"""

from pyfirmata import Arduino, util
from time import sleep

port = 'COM11'
board = Arduino(port)

sleep(1)

it = util.Iterator(board)
it.start()