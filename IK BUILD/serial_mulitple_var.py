from serial import Serial as sr
import keyboard
ad = sr('COM6',9600)

if __name__ == "__main__":
    while True:
        j1:int = input ("J1 position: ") 
        j2:int = input ("J2 position: ") 
        j3:int = input ("J3 position: ")   
            # query servo position
        pos = str(j1+','+j2+','+j3+',')

        ad.write(pos.encode())                          # write position to serial port
                   # read serial port for arduino echo
        reachedPos = str(ad.readline().decode('ascii'))          # read serial port for arduino echo
        print  (reachedPos) 

        if keyboard.read_key() == 'esc':
            break
    