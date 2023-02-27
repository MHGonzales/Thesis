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
table = ws.range("A1:C6").value


#this is for delta movement
def robot(y:int = 0 ,z:int =0):
    
    #move in delta
    print("y: ",y,"z: ",z)


#create function rotate knob.
    #move to knob 2 servos (1st and 2nd servo)
    # grab knob( 1 servo last )
    #rotate knob(1 servo middle)




#this is for delta calculation
def delta(oy,oz,ny,nz):
    global i
    dy = ny-oy
    dz = nz - oz
    print("Delat y: ",dy ," Delta z: ",dz )
    #new values
    #subtract from old
    #call robot(y,z)
    #new values becomes old values
    return

def left():
    global i
    i=0
    while True:
        if kb.read_key() == "a":
            oy,oz = table[i][1],table[i][2]
            i-=2
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

def right():
    global i
    while True:
        if kb.read_key() == "d":
            oy,oz = table[i][1],table[i][2]
            i+=2
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

def up():
    global i
    while True:
        if kb.read_key() == "w":
            oy,oz = table[i][1],table[i][2]
            i-=1
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

def down():
    global i
    while True:
        if kb.read_key() == "s":
            oy,oz = table[i][1],table[i][2]
            i+=1
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

if __name__ == "__main__":
    t1 = Thread(target=left)
    t2 = Thread(target=right)
    t3 = Thread(target=up)
    t4 = Thread(target=down)


    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
 

    t1.start()
    t2.start()
    t3.start()
    t4.start()


    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    exit
