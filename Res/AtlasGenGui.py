from Tkinter import *

root = Tk()

l = Label(root, text="LUI Atlas Generator")
l.pack()

b = Button(root, text="Add File", width=20)
b.pack(side=LEFT)

b = Button(root, text="Add Frame", width=20)
b.pack(side=RIGHT)



root.mainloop()