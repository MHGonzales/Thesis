import xlwings as xw
import keyboard as kb
from threading import Thread
import time as tm

"""
# Specifying a sheet
ws = xw.Book("coordinates_py.xlsx").sheets['Middle Lower Load']
  
y:float = 0
z:float = 0
# Selecting a 2D
# range of data
table = ws.range("A1:I2").value
i =1
j =2
h =0

if __name__ == "__main__":
    y = table[h][i]
    z = table[h][j]
    while True:
            if keyboard.read_key() == "a":
                i=i-3
                j=j-3
            elif keyboard.read_key() == "w":
                h=h+1
            elif keyboard.read_key() == "s":
                h=h-1
            elif keyboard.read_key() == "d":   
                i=i+3
                j=j+3 
            elif keyboard.read_key() == 'esc':
                break
            else:
                print("No data received")
                continue
            y = table[h][i]
            z = table[h][j]
            print("y:",y," z:",z)
"""
#specify sheets
#read data range from
#define keyboard funcions
#calculate delta
#move robot using delta
#activate threads for keyboard

ws = xw.Book("coordinates_py.xlsx").sheets['Middle Lower Load']
table = ws.range("A1:I2").value
i =1
j =2
h =0

yold:float = table[h][i]
zold:float = table[h][j]
ynew:float = table[h][i]
znew:float = table[h][j]
ydelta:float = 0
zdelta:float = 0

def delta():
    ydelta = yold - ynew
    zdelta = zold - znew
    yold = ynew
    zold = znew


def moverobot():
    while True:
        continue
        #print("Moving robot in y delta:" ,ydelta, "z delta: ",zdelta)

def left():
    while True:
        if kb.read_key() == "a":
            i=i-3
            j=j-3
            ynew = table[h][i]
            znew = table[h][j]
            print(ynew," ",znew)
            delta()
        tm.sleep(0.25)

def right():
    while True:
        if kb.read_key() == "d":
            i=i+3
            j=j+3 
            ynew = table[h][i]
            znew = table[h][j]
            print(ynew," ",znew)
            delta()
        tm.sleep(0.25)

def up():
    while True:
        if kb.read_key() == "w":
            h=h+1
            ynew = table[h][i]
            znew = table[h][j]
            print(ynew," ",znew)
            delta()
        tm.sleep(0.25)

def down():
    while True:
        if kb.read_key() == "s":
            h=h-1
            ynew = table[h][i]
            znew = table[h][j]
            print(ynew," ",znew)
            delta()
        tm.sleep(0.25)

if __name__ == "__main__":
    t1 = Thread(target=left)
    t2 = Thread(target=right)
    t3 = Thread(target=up)
    t4 = Thread(target=down)
    t5 = Thread(target = moverobot)

    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    #t5.setDaemon(True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    #t5.start()

    print(ynew," ",znew)
    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    exit
