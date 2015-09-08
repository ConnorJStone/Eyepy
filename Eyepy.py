from CalendarBase import CalendarBase
from PatientBase import PatientBase
from StockBase import StockBase
from Themes import Colours, Relief, Dates
from datetime import datetime
import Tkinter as tk
import logging

"""
The starting point for eyepy, all resources can be accessed from here.

From here each of the base windows can be created. They are: the Calendar window, the Patients window, the Stock window, fixme. From the Calendar window one can view anything to do with scheduling and create new appointments. From the Patients window one can view anything to do with the patients, and all create appointments for them. From the Stock window one can view anything to do with equipment that is bought or sold.
"""
class RootMenu(tk.Tk):
    # this is root
    
    def __init__(self):
        # Variables
        today = datetime.today()
        self.log = logging.getLogger(__name__)
        logging.basicConfig(filename='database/log/%s.log' % today.strftime('%Y-%m-%d'), level=logging.INFO)
        self.calendar = None
        self.patients = None
        self.stock = None
        
        # Build Window
        tk.Tk.__init__(self)
        self.title('Eyepy home')
        self.protocol('WM_DELETE_WINDOW', self.Close)

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

        self.patientsbutton = tk.Button(self,
                                        text='Patients',
                                        bg=Colours.patientbase['button'],
                                        activebackground=Colours.patientbase['buttonactive'],
                                        relief=Relief.patientbase['button'],
                                        command=self.StartPatients)

        self.stockbutton = tk.Button(self,
                                     text='Stock',
                                     bg=Colours.stockbase['button'],
                                     activebackground=Colours.stockbase['buttonactive'],
                                     relief=Relief.stockbase['button'],
                                     command=self.StartStock)        

        # Place Widgets
        self.calendarbutton.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.patientsbutton.grid(row=0,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
        self.stockbutton.grid(row=0,column=2,sticky=tk.N+tk.S+tk.E+tk.W)

        # Put first message in log
        self.log.info('eyepy initialized at: %s' % today.strftime(Dates.dateformats['dashdate_colontime']))

        # Start main loop, runs the interface
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

    def Close(self):
        if self.calendar != None:
            self.calendar.Close()
        if self.patients != None:
            self.patients.Close()
        if self.stock != None:
            self.stock.Close()

        today = datetime.today()
        self.log.info('Closing eyepy at: %s'  % today.strftime('%Y-%m-%d %H:%M:%S'))
        self.destroy()

root = RootMenu()

