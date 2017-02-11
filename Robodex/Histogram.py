import tkinter as tk

#
class Histogram(tk.Canvas):
    def __init__(self, master=None, title="Default", values=[1,2,3,4,0,0,0,0,0,0,0,0,0], buckets=[0,1,2,3,4,5,6,7,8,9,10,11,12]):
        tk.Canvas.__init__(self, master)
        self.pack()
        self.config(height=175)
        self.create_graph(title, values, buckets)
        
        
    def create_graph(self, title, val, buckets):
    	offSetX1 = 0
    	offSetX2 = 30
    	index = 0
    	for h in val:
    		height = 100 - (10 * h)
    		self.create_rectangle(offSetX1, height+50, offSetX2, 150, fill='#39ff14')
    		
    		self.create_text(15+offSetX1,159, fill="darkblue", font="Times", text=buckets[index])
    		
    		offSetX1 += 30
    		offSetX2 += 30
    		index += 1

    		
    	self.config(width=offSetX2 - 30)
    	
    	self.create_text((offSetX2 - 15)/2,15, fill="darkblue",font="Times 20 bold", text=title)
    	
    	
    	
#Code below used for testing without robodex
#root = tk.Tk()
#canvas = Histogram(root)
#canvas.pack(anchor=tk.NW)

