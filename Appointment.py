import Tkinter as tk
from Themes import Colours, Relief

class AppointmentBase(tk.Toplevel):
    # root:
    #     no space needed
    
    isopen = False
    
    def __init__(self,root):
        AppointmentBase.isopen = True
        
        # Variables
        self.colour = Colours.calendarbase
        self.relief = Relief.calendarbase
        self.root = root
        
        # Build Window
        tk.Toplevel.__init__(self,root,bg=self.colour['frame'])
        self.title('Appointment')
        self.protocol('WM_DELETE_WINDOW', self.Close)

        # Configure Window
        for i in range(4): self.grid_columnconfigure(i,weight=1)
        
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
        # Widgets
        self.checkbutton = tk.Button(self, text='Check', bg=self.colour['button'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        self.seepatientbutton = tk.Button(self, text='See Patient', bg=self.colour['button'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        self.typemenu = tk.Menubutton(self, text='Type', bg=self.colour['button'], relief=self.relief['button'])
        self.printbutton = tk.Button(self, text='Print', bg=self.colour['button'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        self.savebutton = tk.Button(self, text='Save', bg=self.colour['savebutton'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        
        # Place Widgets
        self.checkbutton.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W)
        self.seepatientbutton.grid(row=0,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
        self.typemenu.grid(row=0,column=2,sticky=tk.N+tk.E+tk.S+tk.W)
        self.printbutton.grid(row=0,column=3,sticky=tk.N+tk.E+tk.S+tk.W)
        self.savebutton.grid(row=0,column=4,sticky=tk.N+tk.E+tk.S+tk.W)

    def Close(self):
        AppointmentBase.isopen = False
        self.destroy()