from pyfirmata import Arduino, SERVO
from time import sleep

port = ''
pin = 10
board = Arduino(port)
board.digital(pin).mode = SERVO
def rotateSERVO(pin, angle):
   board.digital[pin].write(angle)
   sleep(0.015)

def move_servo(angle):
    pin10.write(angle)
    
def main():
    global pin10
    
    board=pyfirmata.Arduino('COM11')

    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    pin10 = board.get_pin('d:10:s')
    
    root = Tk()
    scale = Scale(root, command = move_servo, to = 175, 
                  orient = HORIZONTAL, length = 400, label = 'Angle')
    scale.pack(anchor = CENTER)

    root.mainloop()

main()
while True:
    for i in range (0,180):
        rotateSERVO(pin,i)
    for i in range(180,1,-1):
        rotateSERVO(pin, i)
