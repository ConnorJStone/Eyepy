import Tkinter as tk
import logging
from Themes import Colours, Relief

#------------------------------------------------------------------------------
# Holds all stock information
class StockBase(tk.Toplevel):
    # root:
    #     no space needed

    isopen = False
    
    def __init__(self, root):
        StockBase.isopen = True

        # Variables
        self.log = logging.getLogger(__name__)
        self.colour = Colours.stockbase
        self.relief = Relief.stockbase
        self.root = root

        # Build Window
        tk.Toplevel.__init__(self,root,bg=self.colour['frame'])
        self.title('Stock')
        self.protocol('WM_DELETE_WINDOW',self.Close)

    def Close(self):
        StockBase.isopen = False
        self.root.stock = None
        self.destroy()
