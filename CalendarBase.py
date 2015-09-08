import Tkinter as tk
import logging
from Themes import Colours, Relief
from datetime import datetime, timedelta

from Calendar import Day, Week, Month

class CalendarBase(tk.Toplevel):
    # root:
    #     no space needed

    isopen = False
    
    def __init__(self, root):
        CalendarBase.isopen = True
        
        # Variables
        self.log = logging.getLogger(__name__)
        self.colour = Colours.calendarbase
        self.relief = Relief.calendarbase
        self.root = root
        self.doctor = tk.StringVar()
        self.view = tk.StringVar()
        self.calendarspace = None
        self.day = datetime.today()
        
        # Build Window
        tk.Toplevel.__init__(self, root, bg=self.colour['frame'])
        self.title('Calendar')
        self.protocol('WM_DELETE_WINDOW', self.Close)
        self.bind('<Escape>', self.Close)
        
        # Window Configure
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        for i in range(3, 11): self.grid_columnconfigure(i, weight=1)
            
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # Declare Widgets
        self.yearbox = tk.Entry(self,
                                bg=self.colour['entry'],
                                width=5,
                                relief=self.relief['entry'])
        self.monthbox = tk.Entry(self,
                                 bg=self.colour['entry'],
                                 width=3,
                                 relief=self.relief['entry'])
        self.daybox = tk.Entry(self,
                               bg=self.colour['entry'],
                               width=3,
                               relief=self.relief['entry'])
        
        self.jumpbackmenu = tk.Menubutton(self,
                                          text='jump back',
                                          bg=self.colour['button'],
                                          relief=self.relief['button'],
                                          activebackground=self.colour['buttonactive'])
        self.jumpbackday = tk.Button(self,
                                     text='prev',
                                     bg=self.colour['button'],
                                     relief=self.relief['button'],
                                     highlightthickness=0,
                                     activebackground=self.colour['buttonactive'],
                                     command=self.Jump_Back)
        
        self.jumpforwardday = tk.Button(self,
                                        text='next',
                                        bg=self.colour['button'],
                                        relief=self.relief['button'],
                                        highlightthickness=0,
                                        activebackground=self.colour['buttonactive'],
                                        command=self.Jump_Forward)
        
        self.jumpforwardmenu = tk.Menubutton(self,
                                             text='jump forward',
                                             bg=self.colour['button'],
                                             relief=self.relief['button'],
                                             activebackground=self.colour['buttonactive'])

        self.doctormenu = tk.Menubutton(self,
                                        text='Doctor',
                                        bg=self.colour['button'],
                                        relief=self.relief['button'],
                                        activebackground=self.colour['buttonactive'])

        self.viewmenu = tk.Menubutton(self,
                                      text='View',
                                      bg=self.colour['button'],
                                      relief=self.relief['button'],
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

        # Initial Widget Properties
        self.yearbox.bind('<Return>', self.Entry_Day)
        self.monthbox.bind('<Return>', self.Entry_Day)
        self.daybox.bind('<Return>', self.Entry_Day)

        self.jumpbackmenu.menu = tk.Menu(self.jumpbackmenu, tearoff=0)
        self.jumpbackmenu['menu'] = self.jumpbackmenu.menu
        self.jumpbackmenu.menu.add_command(label='week', command=self.Jump_Back_Week)
        self.jumpbackmenu.menu.add_command(label='month', command=self.Jump_Back_Month)
        self.jumpbackmenu.menu.add_command(label='year', command=self.Jump_Back_Year)

        self.jumpforwardmenu.menu = tk.Menu(self.jumpforwardmenu, tearoff=0)
        self.jumpforwardmenu['menu'] = self.jumpforwardmenu.menu
        self.jumpforwardmenu.menu.add_command(label='week', command=self.Jump_Forward_Week)
        self.jumpforwardmenu.menu.add_command(label='month', command=self.Jump_Forward_Month)
        self.jumpforwardmenu.menu.add_command(label='year', command=self.Jump_Forward_Year)

        self.doctormenu.menu = tk.Menu(self.doctormenu, tearoff=0)
        self.doctormenu['menu'] = self.doctormenu.menu
        self.doctormenu.menu.add_radiobutton(label='Jessica', value='jessica', variable=self.doctor)
        self.doctormenu.menu.add_radiobutton(label='Connor', value='connor', variable=self.doctor)
        self.doctor.set('jessica')

        self.viewmenu.menu = tk.Menu(self.viewmenu, tearoff=0)
        self.viewmenu['menu'] = self.viewmenu.menu
        self.viewmenu.menu.add_radiobutton(label='day', value='day', variable=self.view, command=self.View_Set)
        self.viewmenu.menu.add_radiobutton(label='week', value='week', variable=self.view, command=self.View_Set)
        self.viewmenu.menu.add_radiobutton(label='month', value='month', variable=self.view, command=self.View_Set)
        self.view.set('day')

        # Place Widgets
        self.yearbox.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.monthbox.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.daybox.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.jumpbackmenu.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
        self.jumpbackday.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W)
        self.jumpforwardday.grid(row=0, column=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.jumpforwardmenu.grid(row=0, column=6, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.doctormenu.grid(row=0, column=7, sticky=tk.N+tk.S+tk.E+tk.W)
        self.viewmenu.grid(row=0, column=8, sticky=tk.N+tk.S+tk.E+tk.W)
        self.printbutton.grid(row=0, column=9, sticky=tk.N+tk.S+tk.E+tk.W)
        self.refreshbutton.grid(row=0, column=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.View_Set()

        self.log.info('Started the calendar')

    def View_Set(self, event=None):
        try:
            self.calendarspace.destroy()
        except:
            pass
        if self.view.get() == 'day':
            self.calendarspace = Day(self,self.doctor.get(), self.day)
        elif self.view.get() == 'week':
            self.calendarspace = Week(self,self.doctor.get(), self.day)
        elif self.view.get() == 'month':
            self.calendarspace = Month(self,self.doctor.get(), self.day)
        else:
            self.log.error('Calendar Base: Could not set view, unrecognized self.view value: %s' % self.view.get())
        self.calendarspace.grid(row=1, column=0, columnspan=11, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

        self.yearbox.delete(0,tk.END)
        self.monthbox.delete(0,tk.END)
        self.daybox.delete(0,tk.END)
        self.yearbox.insert(0, self.day.strftime('%Y'))
        self.monthbox.insert(0, self.day.strftime('%m'))
        self.daybox.insert(0, self.day.strftime('%d'))

            
    def View_Day(self, event=None, day=None):
        self.view.set('day')
        if day != None:
            self.day = day
        self.View_Set()
        
    def View_Week(self, event=None):
        self.view.set('week')
        self.View_Set()

    def View_Month(self, event=None):
        self.view.set('month')
        self.View_Set()

    def Entry_Day(self, event=None):
        try:
            date = datetime(year=int(self.yearbox.get()), month=int(self.monthbox.get()), day=int(self.daybox.get()))
            self.day = date
        except:
            return

        self.View_Set()

    def Jump_Forward(self, event=None):
        if self.view.get() == 'day':
            self.Jump_Forward_Day(event)
        elif self.view.get() == 'week':
            self.Jump_Forward_Week(event)
        elif self.view.get() == 'month':
            self.Jump_Forward_Month(event)
        else:
            self.log.error('Could not interpret self.view.get(), got value: %s' % self.view.get())

    def Jump_Back(self, event=None):
        if self.view.get() == 'day':
            self.Jump_Back_Day(event)
        elif self.view.get() == 'week':
            self.Jump_Back_Week(event)
        elif self.view.get() == 'month':
            self.Jump_Back_Month(event)
        else:
            self.log.error('Could not interpret self.view.get(), got value: %s' % self.view.get())

    def Jump_Forward_Day(self, event=None):
        self.day = self.day + timedelta(days=1)
        self.View_Set()

    def Jump_Forward_Week(self, event=None):
        self.day = self.day + timedelta(days=7)
        self.View_Set()
        
    def Jump_Forward_Month(self, event=None):
        self.day = self.day + timedelta(days=29)
        self.View_Set()

    def Jump_Forward_Year(self, event=None):
        self.day = self.day + timedelta(days=365)
        self.View_Set()

    def Jump_Back_Day(self, event=None):
        self.day = self.day - timedelta(days=1)
        self.View_Set()

    def Jump_Back_Week(self, event=None):
        self.day = self.day - timedelta(days=7)
        self.View_Set()
        
    def Jump_Back_Month(self, event=None):
        self.day = self.day - timedelta(days=29)
        self.View_Set()

    def Jump_Back_Year(self, event=None):
        self.day = self.day - timedelta(days=365)
        self.View_Set()

    def Refresh(self, event=None):
        self.View_Set()

    def Close(self, event=None):
        CalendarBase.isopen = False
        self.root.calendar = None
        if self.calendarspace != None:
            self.calendarspace.Close()
        self.destroy()
