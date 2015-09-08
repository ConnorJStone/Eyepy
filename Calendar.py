import Tkinter as tk
import logging
from Themes import Colours, Relief, Dates
from datetime import datetime, timedelta

from Patient import PatientView
from Appointment import AppointmentBase

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

"""
for the booked appointments, the order of information should be as follows: TIME (hour, minute, pm/am) LAST NAME, FIRST NAME, HEALTHCARD, PHONE NUMBER, CODE
for the available appointments the order of information should be: TIME (hour, minute)
"""

#------------------------------------------------------------------------------
class Day(tk.Frame):#+' '+weekdays[self.day.weekday()]
    # root:
    #     space for paned window needed

    # Day view base
    # -root: parent window/object to give space for the day
    # -day: datetime object with the day to be displayed
    def __init__(self, root, doctor, day):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.log = logging.getLogger(__name__)
        self.root = root
        self.available = None
        self.scheduled = None
        self.doctor = doctor
        self.day = day
        
        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Configure Window
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Widgets
        self.daylabel = tk.Label(self, text=weekdays[self.day.weekday()], bg=self.colour['label'], relief=self.relief['label'])
        self.panedwindow = tk.PanedWindow(self, bg=self.colour['frame'], orient=tk.HORIZONTAL)
        self.available = Day_Available(self, self.doctor, self.day)        
        self.scheduled = Day_Scheduled(self, self.doctor, self.day)

        # Place Widgets
        self.daylabel.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.panedwindow.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.panedwindow.add(self.available)
        self.panedwindow.add(self.scheduled)

    def Close(self):
        if self.available != None:
            self.available.Close()

        if self.scheduled != None:
            self.scheduled.Close()
        
# Shows the spaces available for new appointments
class Day_Available(tk.Frame):
    # root:
    #     space for frame needed
    
    def __init__(self, root, doctor, day):
        #  Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.daystr = Dates.dateformats
        self.doctor = doctor
        self.day = day
        self.log = logging.getLogger(__name__)
        self.root = root
        self.appointment = None

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Window Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Top row Configure
        self.available = tk.Label(self, text=self.day.strftime(self.daystr['slashdate']), bg=self.colour['label'], relief=self.relief['label'])
        self.available.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # List box with scroll bar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.scheduledlistbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scheduledlistbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar['command'] = self.scheduledlistbox.yview

        # Bind Double Click to switch to day view
        self.scheduledlistbox.bind('<Double-Button-1>', self.NewAppointment)

        self.Fill()

    def Fill(self):#deleteme
        for i in range(100):
            self.scheduledlistbox.insert(tk.END, 'time available here, %d' % i)

    def NewAppointment(self, event=None):
        if not AppointmentBase.isopen:
            self.appointment = AppointmentBase(self)#fixme, have it send info to the appointment

    def Close(self):
        if self.appointment != None:
            self.appointment.Close()
            
        
# Shows the currently scheduled appointments
class Day_Scheduled(tk.Frame):
    # root:
    #     space for frame needed
    
    def __init__(self, root, doctor, day, simplified=False):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.daystr = Dates.dateformats
        self.doctor = doctor
        self.day = day
        self.log = logging.getLogger(__name__)
        self.root = root
        self.patientview = None

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])
        
        # Window Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Top Label
        self.scheduled = tk.Label(self, text=self.day.strftime(self.daystr['slashdate']), bg=self.colour['label'], relief=self.relief['label'])
        self.scheduled.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        if simplified: self.scheduled.bind('<Button-1>', self.View_Day)
        
        # List box with scroll bar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.scheduledlistbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scheduledlistbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar['command'] = self.scheduledlistbox.yview

        # Bind Double Click to switch to day view
        self.scheduledlistbox.bind('<Double-Button-1>', self.Patient_View)

        self.Fill()

    def Fill(self):#deleteme
        for i in range(100):
            self.scheduledlistbox.insert(tk.END, 'person info here, %d' % i)

    def View_Day(self, event=None):
        self.root.View_Day(event, self.day)

    def Patient_View(self, event=None):
        if not PatientView.isopen:
            self.patientview = PatientView(self)

    def Close(self):
        if self.patientview != None:
            self.patientview.Close()
                    
# To be used for the week and month views
class Day_Simple(tk.Frame):
    # root:
    #     space for frame needed
    #     method "View_Day" must be callable
    
    def __init__(self, root, doctor, day):
        values  = [8,5,8] # fixme deleteme
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.daystr = Dates.dateformats
        self.doctor = doctor
        self.day = day
        self.log = logging.getLogger(__name__)
        self.root = root

        # Build Window
        tk.Frame.__init__(self, root)

        # Configure Window
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create Info Labels
        self.daylabel = tk.Label(self, text=self.day.strftime(self.daystr['slashdate']), bg=self.colour['label'], relief=self.relief['label'])
        self.startlabel = tk.Label(self, text='start: %d' % values[0], bg=self.colour['frame'], relief=self.relief['label'])
        self.endlabel = tk.Label(self, text='end: %d' % values[1], bg=self.colour['frame'], relief=self.relief['label'])
        self.nappointments = tk.Label(self, text='appointments: %d' % values[2], bg=self.colour['frame'], relief=self.relief['label'])

        # Place Info Labels
        self.daylabel.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.startlabel.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.endlabel.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.nappointments.grid(row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # Click to jump to day view
        self.daylabel.bind('<Button-1>', self.View_Day)

    def View_Day(self, event=None):
        self.root.View_Day(event, self.day)

    def Close(self):
        pass

#------------------------------------------------------------------------------
class Week(tk.Frame):
    # root:
    #     space for frame needed
    #     method "View_Day" must be callable
    
    def __init__(self, root, doctor, day, simplified=False):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.doctor = doctor
        self.day = day - timedelta(days=day.weekday()) # always start week on monday
        self.root = root
        self.log = logging.getLogger(__name__)
        self.daylabel = []

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Configure Window
        for i in range(7):
            self.grid_columnconfigure(i, weight=1, uniform='a')

        if simplified:
            self.grid_rowconfigure(0, weight=1)
        else:
            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=1)
            # Weekday labels
            for i in range(7):
                self.daylabel.append(tk.Label(self, text=weekdays[i], bg=self.colour['label'], relief=self.relief['label']))
                self.daylabel[i].grid(row=0, column=i, sticky=tk.N+tk.S+tk.E+tk.W)

        # Fill the week with day objects
        self.days = []
        for i in range(7):
            day = self.day + timedelta(days=i)
            if simplified:
                self.days.append(Day_Simple(self, self.doctor, day))
            else:
                self.days.append(Day_Scheduled(self, self.doctor, day, True))

            self.days[i].grid(row=0 if simplified else 1, column=i, sticky=tk.N+tk.S+tk.E+tk.W)

    def View_Day(self, event=None, day=None):
        self.root.View_Day(event, day)

    def Close(self):
        for d in self.days:
            d.Close()
                    
#------------------------------------------------------------------------------
class Month(tk.Frame):
    # root:
    #     space for frame needed
    #     method "View_Day" must be callable
    def __init__(self, root, doctor, day):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.doctor = doctor
        self.day = day.replace(day=1)
        self.root = root
        self.log = logging.getLogger(__name__)
        self.daylabel = []

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Window Configure
        for i in range(7):
            self.grid_columnconfigure(i, weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=0)
        for i in range(4):
            self.grid_rowconfigure(i+1, weight=1)

        # Weekday labels
        for i in range(7):
            self.daylabel.append(tk.Label(self, text=weekdays[i], bg=self.colour['label'], relief=self.relief['label']))
            self.daylabel[i].grid(row=0, column=i, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # Fill month with weeks
        self.weeks = []
        for i in range(4):
            delta = timedelta(days=7*i)
            self.weeks.append(Week(self, self.doctor, self.day+delta, True))
            self.weeks[i].grid(row=i+1, column=0, columnspan=7,  sticky=tk.N+tk.S+tk.E+tk.W)

    def View_Day(self, event=None, day = None):
        self.root.View_Day(event, day)

    def Close(self):
        for w in self.weeks:
            w.Close()

        
