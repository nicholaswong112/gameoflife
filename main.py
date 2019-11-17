import tkinter as tk

window = tk.Tk()
window.title("The Game of Life")

canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()

line1 = canvas.create_line(25, 25, 250, 150)
line2 = canvas.create_line(25, 250, 250, 150, fill='red')

rect = canvas.create_rectangle(500, 25, 175, 75, fill='green')

window.mainloop()
