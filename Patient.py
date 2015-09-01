import Tkinter as tk
from Themes import Colours, Relief
import logging


#------------------------------------------------------------------------------
class PatientList(tk.Frame):

    def __init__(self,root):
        # Variables
        self.colour = Colours.patient
        self.relief = Relief.patient
        self.log = logging.getLogger('op.patient.list')
        self.patients = []
        self.sortby = 'name'
        
        # Build Window
        tk.Frame.__init__(self,root, bg=self.colour['frame'])

        # Configure Window
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Label
        self.listlabel = tk.Label(self,text='Sorted by: Name, Doctor: Jessica', bg=self.colour['label'], relief=self.relief['label'])
        self.listlabel.grid(row=0,column=0,columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # List box with scroll bar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.patientlistbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.patientlistbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar['command'] = self.patientlistbox.yview

        # Bind Double Click to switch to day view
        self.patientlistbox.bind('<Double-Button-1>', self.saynumber)

        self.Fill()


    def Fill(self):#deleteme
        for i in range(100):
            self.patientlistbox.insert(tk.END, 'this person, %d' % i)

    def saynumber(self, event):#deleteme
        selection = self.patientlistbox.curselection()
        value = self.patientlistbox.get(selection[0])
        print 'at %d we have this string: \"%s\"' % (selection[0], value)

