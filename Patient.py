import Tkinter as tk
from Themes import Colours, Relief
import logging

from AppointmentBase import AppointmentBase
from PatientViewBase import PatientViewBase

#------------------------------------------------------------------------------
# A list of all patients that can be organized and accessed in useful ways
class PatientList(tk.Frame):
    # root:
    #     space for frame
    #     variable "sortby" has a string
    #     variable "searchby" has a dictionary indexed by strings with boolean values
    #     variable "doctor" has a string
    
    def __init__(self,root):
        # Variables
        self.colour = Colours.patient
        self.relief = Relief.patient
        self.log = logging.getLogger(__name__)
        self.patients = []
        self.root = root
        self.patientview = None
        
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
        self.patientlistbox.bind('<Double-Button-1>', self.Patient_View)

        self.Fill()


    # fixme
    def Fill(self):#deleteme
        for i in range(100):
            self.patientlistbox.insert(tk.END, 'this person, %d' % i)

    # Opens a view for a single patient
    def Patient_View(self, event=None):
        if not PatientViewBase.isopen:
            self.patientview = PatientViewBase(self, '000g')

    def Close(self):
        if self.patientview != None:
            self.patientview.Close()
