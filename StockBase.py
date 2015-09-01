import Tkinter as tk
from Themes import Colours, Relief

class StockBase(tk.Toplevel):
    # root:
    #     no space needed

    isopen = False
    
    def __init__(self,root):
        StockBase.isopen = True

        # Variables
        self.colour = Colours.stockbase
        self.relief = Relief.stockbase

        # Build Window
        tk.Toplevel.__init__(self,root,bg=self.colour['frame'])
        self.title('Stock')
        self.protocol('WM_DELETE_WINDOW',self.Close)

    def Close(self):
        StockBase.isopen = False
        self.destroy()
