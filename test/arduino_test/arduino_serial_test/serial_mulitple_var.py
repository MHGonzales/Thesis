from serial import Serial as sr
import keyboard
from dobject import Dobot
from numpy import pi
from spatialmath import SE3
import time as tm
ad = sr('COM6',9600)

rb = Dobot()
tm.sleep(5)
Tf = SE3.Trans((140+90)/1000 ,62/1000 ,12/1000) *SE3.OA([0,  0, 1], [1, 0, 0])
sol = rb.ikine_LMS(Tf,rb.qz)
qn =sol.q*180/pi
j4 = str(0)
print(j4)
j5 = str(qn[5])
print(j5)
j6 = str(qn[6])
print(j6)
pos = str(j4 +',' + j5 +','+ j6 +',')
print(pos.encode())
ad.write(pos.encode())
"""  
reachedPos = str(ad.readline().decode('ascii'))          # read serial port for arduino echo
print  (reachedPos) 
reachedPos = str(ad.readline().decode('ascii'))  
print  (reachedPos)  
pos = str(j4 +',' + j5 +','+ j6 +',')
print(pos.encode())
ad.write(pos.encode())

if __name__ == "__main__":
    while True:
        j1:int = input ("J1 position: ") 
        j2:int = input ("J2 position: ") 
        j3:int = input ("J3 position: ")   
            # query servo position
        pos = str(j1 +',' + j2+','+ j3+',')

        ad.write(pos.encode())                          # write position to serial port
                   # read serial port for arduino echo

        if keyboard.read_key() == 'esc':
            break
"""