import Tkinter as tk
from Themes import Colours, Relief
from Patient import PatientList
import logging

class PatientBase(tk.Toplevel):
    # root:
    #     no space needed

    isopen = False
    def __init__(self,root):
        PatientBase.isopen = True
        # Variables
        self.log = logging.getLogger(__name__)
        self.colour = Colours.patientbase
        self.relief = Relief.patientbase
        self.root = root
        self.sortby = tk.StringVar()
        self.searchby = {'name':tk.BooleanVar(),
                         'healthcardnumber':tk.BooleanVar(),
                         'phonenumber':tk.BooleanVar(),
                         'notes':tk.BooleanVar()}
        self.doctor = tk.StringVar()
        self.patientlist = None
        
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

        self.searchbymenu = tk.Menubutton(self,
                                      text='Search By',
                                      bg=self.colour['button'],
                                      relief=self.relief['button'],
                                      activebackground=self.colour['buttonactive'])

        self.sortbymenu = tk.Menubutton(self,
                                    text='Sort',
                                    bg=self.colour['button'],
                                    relief=self.relief['button'],
                                    activebackground=self.colour['buttonactive'])
        
        self.doctormenu = tk.Menubutton(self,
                                        text='Doctor',
                                        bg=self.colour['button'],
                                        relief=self.relief['button'],
                                        activebackground=self.colour['buttonactive'])
        
        self.newpatientbutton = tk.Button(self,
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
        self.searchbymenu.menu = tk.Menu(self.searchbymenu, tearoff=0)
        self.searchbymenu['menu'] = self.searchbymenu.menu
        self.searchbymenu.menu.add_checkbutton(label='Name', onvalue=True, offvalue=False, variable=self.searchby['name'])
        self.searchbymenu.menu.add_checkbutton(label='Healthcard #', onvalue=True, offvalue=False, variable=self.searchby['healthcardnumber'])
        self.searchbymenu.menu.add_checkbutton(label='Phone #', onvalue=True, offvalue=False, variable=self.searchby['phonenumber'])
        self.searchbymenu.menu.add_checkbutton(label='Notes', onvalue=True, offvalue=False, variable=self.searchby['notes'])
        self.searchby['name'].set(True)

        self.sortbymenu.menu = tk.Menu(self.sortbymenu, tearoff=0)
        self.sortbymenu['menu'] = self.sortbymenu.menu
        self.sortbymenu.menu.add_radiobutton(label='Name', value='name', variable=self.sortby)
        self.sortbymenu.menu.add_radiobutton(label='Appointment', value='appointment', variable=self.sortby)
        self.sortbymenu.menu.add_radiobutton(label='Recall', value='recall', variable=self.sortby)
        self.sortby.set('name')

        self.doctormenu.menu = tk.Menu(self.doctormenu, tearoff=0)
        self.doctormenu['menu'] = self.doctormenu.menu
        self.doctormenu.menu.add_radiobutton(label='Jessica', value='jessica', variable=self.doctor)
        self.doctormenu.menu.add_radiobutton(label='Connor', value='connor', variable=self.doctor)
        self.doctor.set('jessica')
        
        # Place Widgets
        self.searchentry.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.searchbymenu.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.sortbymenu.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.doctormenu.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
        self.newpatientbutton.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)
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
        PatientBase.isopen = False
        self.root.patients = None
        if self.patientlist != None:
            self.patientlist.Close()
        self.destroy()
