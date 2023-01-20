import xlwings as xw
import keyboard
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
  
