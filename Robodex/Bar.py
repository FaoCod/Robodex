import tkinter as tk

class DisplayBar(tk.Canvas):
    def __init__(self, master=None, value=50, number=0):
        tk.Canvas.__init__(self, master)
        self.pack()
        self.config(width=40, height=100)
        self['bg'] = 'red'
        self.create_image(value, number)
        
    def create_image(self, val, num):
        self.create_rectangle(0, val, 45, 110, fill='#39ff14')

        self.create_text(20, 80, text=num, font=('Helvetica', 41, 'bold'))


#root = tk.Tk()
#canvas = DisplayBar(root, 20, 8)
#canvas.pack(anchor=tk.NW)
