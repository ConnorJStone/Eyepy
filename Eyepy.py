from CalendarBase import CalendarBase
from PatientBase import PatientBase
from StockBase import StockBase
from Themes import Colours, Relief
import Tkinter as tk

class RootMenu(tk.Tk):
    # this is root
    
    def __init__(self):
        # Variables
        self.calendar = None
        self.patients = None
        self.stock = None
        
        # Build Window
        tk.Tk.__init__(self)
        self.title('Eyepy home')

        # Configure Window
        for i in range(3): self.grid_columnconfigure(i,weight=1)

        self.grid_rowconfigure(0,weight=1)
        
        # Widgets
        self.calendarbutton = tk.Button(self,
                                        text='Calendar',
                                        bg=Colours.calendarbase['button'],
                                        activebackground=Colours.calendarbase['buttonactive'],
                                        command=self.StartCalendar,
                                        relief=Relief.calendarbase['button'])
        self.calendarbutton.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)

        self.patientsbutton = tk.Button(self,
                                        text='Patients',
                                        bg=Colours.patientbase['button'],
                                        activebackground=Colours.patientbase['buttonactive'],
                                        relief=Relief.patientbase['button'],
                                        command=self.StartPatients)
        self.patientsbutton.grid(row=0,column=1,sticky=tk.N+tk.S+tk.E+tk.W)

        self.stockbutton = tk.Button(self,
                                     text='Stock',
                                     bg=Colours.stockbase['button'],
                                     activebackground=Colours.stockbase['buttonactive'],
                                     relief=Relief.stockbase['button'],
                                     command=self.StartStock)        
        self.stockbutton.grid(row=0,column=2,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.mainloop()

    def StartCalendar(self, event=None):
        if not CalendarBase.isopen:
            self.calendar = CalendarBase(self)

    def StartPatients(self, event=None):
        if not PatientBase.isopen:
            self.patients = PatientBase(self)

    def StartStock(self, event=None):
        if not StockBase.isopen:
            self.stock = StockBase(self)

root = RootMenu()

