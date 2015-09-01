import Tkinter as tk
import logging
from Themes import Colours, Relief

#------------------------------------------------------------------------------
class Day(tk.PanedWindow):

    def __init__(self,root):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.log = logging.getLogger('op.calendar.day')

        # Build Window
        tk.PanedWindow.__init__(self, root, bg=self.colour['frame'], orient=tk.HORIZONTAL)

        # Place Widgets
        self.available = Day_Available(self, '2015/08/31')
        self.add(self.available)
        
        self.scheduled = Day_Scheduled(self, '2015/08/31')
        self.add(self.scheduled)
        
# Shows the spaces available for new appointments
class Day_Available(tk.Frame):

    def __init__(self, root, day):
        #  Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.day = day
        self.log = logging.getLogger('op.calendar.day')

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Window Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Top row Configure
        self.available = tk.Label(self, text=self.day, bg=self.colour['label'], relief=self.relief['label'])
        self.available.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # List box with scroll bar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.scheduledlistbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scheduledlistbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar['command'] = self.scheduledlistbox.yview

        # Bind Double Click to switch to day view
        self.scheduledlistbox.bind('<Double-Button-1>', self.saynumber)

        self.Fill()

    def Fill(self):#deleteme
        for i in range(100):
            self.scheduledlistbox.insert(tk.END, 'time available here, %d' % i)

    def saynumber(self, event):#deleteme
        selection = self.scheduledlistbox.curselection()
        value = self.scheduledlistbox.get(selection[0])
        print 'at %d we have this string: \"%s\"' % (selection[0], value)

        
# Shows the currently scheduled appointments
class Day_Scheduled(tk.Frame):

    def __init__(self, root, day, simplified=False):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.day = day
        self.log = logging.getLogger('op.calendar.day')

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])
        
        # Window Configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Top Label
        self.scheduled = tk.Label(self, text=self.day, bg=self.colour['label'], relief=self.relief['label'])
        self.scheduled.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        if simplified: self.scheduled.bind('<Button-1>', root.View_Day)
        
        # List box with scroll bar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.scheduledlistbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scheduledlistbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar['command'] = self.scheduledlistbox.yview

        # Bind Double Click to switch to day view
        self.scheduledlistbox.bind('<Double-Button-1>', self.saynumber)

        self.Fill()

    def Fill(self):#deleteme
        for i in range(100):
            self.scheduledlistbox.insert(tk.END, 'person info here, %d' % i)

    def saynumber(self, event):#deleteme
        selection = self.scheduledlistbox.curselection()
        value = self.scheduledlistbox.get(selection[0])
        print 'at %d we have this string: \"%s\"' % (selection[0], value)
        
# To be used for the week and month views
class Day_Simple(tk.Frame):

    def __init__(self, root, day, values):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.day = day
        self.log = logging.getLogger('op.calendar.day')

        # Build Window
        tk.Frame.__init__(self, root)

        # Configure Window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create Info Labels
        self.daylabel = tk.Label(self, text=self.day, bg=self.colour['label'], relief=self.relief['label'])
        self.startlabel = tk.Label(self, text='start: %d' % values[0], bg=self.colour['label'], relief=self.relief['label'])
        self.endlabel = tk.Label(self, text='end: %d' % values[1], bg=self.colour['label'], relief=self.relief['label'])
        self.nappointments = tk.Label(self, text='appointments: %d' % values[2], bg=self.colour['label'], relief=self.relief['label'])

        # Place Info Labels
        self.daylabel.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.startlabel.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.endlabel.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.nappointments.grid(row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # Click to jump to day view
        self.daylabel.bind('<Button-1>', root.View_Day)

#------------------------------------------------------------------------------
class Week(tk.Frame):

    def __init__(self, root, day, simplified=False, scheduled=True):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.day = day
        self.root = root
        self.log = logging.getLogger('op.calendar.week')

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Configure Window
        self.grid_rowconfigure(0, weight=1)
        for i in range(7):
            self.grid_columnconfigure(i, weight=1)

        # Fill the week with day objects
        self.days = []
        for i in range(7):
            if simplified:
                self.days.append(Day_Simple(self, '2015/08/%0.2d' % (i+self.day), [8, 5, i+2]))
            elif scheduled:
                self.days.append(Day_Scheduled(self, '2015/08/%0.2d' % (i+self.day), True))
            else:
                self.days.append(Day_Available(self, '2015/08/%0.2d' % (i+self.day)))

            self.days[i].grid(row=0, column=i, sticky=tk.N+tk.S+tk.E+tk.W)

    def View_Day(self, event=None):
        self.root.View_Day()
                    
#------------------------------------------------------------------------------
class Month(tk.Frame):

    def __init__(self, root):
        # Variables
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.root = root
        self.log = logging.getLogger('op.calendar.month')

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Window Configure
        self.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)

        # Fill month with weeks
        self.weeks = []
        for i in range(4):
            self.weeks.append(Week(self, i*7+1, True))
            self.weeks[i].grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

    def View_Day(self, event=None):
        self.root.View_Day()

        
