import Tkinter as tk
from Themes import Colours, Relief
from Patient import PatientList

class PatientBase(tk.Toplevel):
    # root:
    #     -no space needed
    #     -variable "patients"" can be set to None
    
    def __init__(self,root):
        # Variables
        self.colour = Colours.patientbase
        self.relief = Relief.patientbase
        self.root = root
        
        # Build Window
        tk.Toplevel.__init__(self, root, bg=self.colour['frame'])
        self.title('Patient List')
        self.protocol('WM_DELETE_WINDOW', self.Close)
        # Configure Window
        for i in range(6): self.grid_columnconfigure(i, weight=1)

        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)

        # Declare Widgets
        self.searchentry = tk.Entry(self,
                                    bg=self.colour['entry'],
                                    relief=self.relief['entry'])

        self.searchby = tk.Menubutton(self,
                                      text='Search By',
                                      bg=self.colour['button'],
                                      relief=self.relief['button'],
                                      activebackground=self.colour['buttonactive'])

        self.sortby = tk.Menubutton(self,
                                    text='Sort',
                                    bg=self.colour['button'],
                                    relief=self.relief['button'],
                                    activebackground=self.colour['buttonactive'])
        
        self.doctormenu = tk.Menubutton(self,
                                        text='Doctor',
                                        bg=self.colour['button'],
                                        relief=self.relief['button'],
                                        activebackground=self.colour['buttonactive'])
        
        self.newpatient = tk.Button(self,
                                    text='New',
                                    bg=self.colour['button'],
                                    relief=self.relief['button'],
                                    highlightthickness=0,
                                    activebackground=self.colour['buttonactive'])
        
        self.printbutton = tk.Button(self,
                                     text='Print',
                                     bg=self.colour['button'],
                                     relief=self.relief['button'],
                                     highlightthickness=0,
                                     activebackground=self.colour['buttonactive'])
        
        self.refreshbutton = tk.Button(self,
                                       text='Refresh',
                                       bg=self.colour['button'],
                                       relief=self.relief['button'],
                                       highlightthickness=0,
                                       activebackground=self.colour['buttonactive'],
                                       command=self.Refresh)

        self.patientlist = PatientList(self)
        
        # Menu Configure
        self.searchby.menu = tk.Menu(self.searchby, tearoff=0)
        self.searchby['menu'] = self.searchby.menu
        self.searchby.menu.add_command(label='Name')
        self.searchby.menu.add_command(label='Healthcard #')
        self.searchby.menu.add_command(label='Phone #')
        self.searchby.menu.add_command(label='Notes')

        self.sortby.menu = tk.Menu(self.sortby, tearoff=0)
        self.sortby['menu'] = self.sortby.menu
        self.sortby.menu.add_command(label='Name')
        self.sortby.menu.add_command(label='Appointment')
        self.sortby.menu.add_command(label='Recall')

        self.doctormenu.menu = tk.Menu(self.doctormenu, tearoff=0)
        self.doctormenu['menu'] = self.doctormenu.menu
        self.doctormenu.menu.add_command(label='Jessica')        

        # Place Widgets
        self.searchentry.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.searchby.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.sortby.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.doctormenu.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
        self.newpatient.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)
        self.printbutton.grid(row=0,column=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.refreshbutton.grid(row=0, column=6, sticky=tk.N+tk.S+tk.E+tk.W)

        self.patientlist.grid(row=1,column=0,columnspan=7, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        

    def Refresh(self):
        try:
            self.patientlist.destroy()
        except:
            pass
        self.patientlist = PatientList(self)
        self.patientlist.grid(row=1,column=0,columnspan=7, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        
        
    def Close(self):
        self.root.patients = None
        self.destroy()
