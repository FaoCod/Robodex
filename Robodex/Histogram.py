import tkinter as tk


class Histogram(tk.Canvas):
    def __init__(self, master=None, values=[1,2,3,4,5,6,7,8,9,10,11,12]):
        tk.Canvas.__init__(self, master)
        self.pack()
        self.config(height=100)
        self.create_graph(values)
        
    def create_graph(self, val):
    	offSetX1 = 0
    	offSetX2 = 15
    	height = 0
    	for h in val:
    		height = 100 - (10 * h)
    		self.create_rectangle(offSetX1, height, offSetX2, 100, fill='#39ff14')
    		offSetX1 += 15
    		offSetX2 += 15
    	self.config(width=offSetX2 - 15)
    	
#Code below used for testing without robodex
#root = tk.Tk()
#canvas = Histogram(root)
#canvas.pack(anchor=tk.NW)
