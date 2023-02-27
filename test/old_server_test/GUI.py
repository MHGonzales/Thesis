from tkinter import *
root = Tk()
root.title("RIAL-3-2021-4")

name = Label(root, text = "Enter Your Name: ")
name.pack()

e = Entry(root, width = 50, borderwidth = 5)
e.pack()

def myClick():
    Welcome = "Welcome, " + e.get() +"!"
    myLabel = Label(root, text = Welcome)
    myLabel.pack()

myButton = Button(root, text = "Register", command = myClick)
myButton.pack()


root.mainloop()


### exit button
# exit = Button (root, text = "Exit Program", command = root.quit)
# exit.pack()
