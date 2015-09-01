import Tkinter as tk
import logging
from Themes import Colours, Relief
from Calendar import Day, Week, Month

class CalendarBase(tk.Toplevel):
    # root:
    #     no space needed
    #     variable "calendar" can be set to None
    
    def __init__(self, root):
        # Variables
        self.view = 'day'
        self.log = logging.getLogger('op.calendar')
        self.colour = Colours.calendarbase
        self.relief = Relief.calendarbase
        self.root = root

        # Build Window
        tk.Toplevel.__init__(self, root, bg=self.colour['frame'])
        self.title('Calendar')
        self.protocol('WM_DELETE_WINDOW', self.Close)
        
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
                                     activebackground=self.colour['buttonactive'])
        self.jumpforwardday = tk.Button(self,
                                        text='next',
                                        bg=self.colour['button'],
                                        relief=self.relief['button'],
                                        highlightthickness=0,
                                        activebackground=self.colour['buttonactive'])
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

        # Start by displaying day information
        self.View_Day()
        
        # Initial Widget Properties
        self.yearbox.insert(0, 'yyyy')
        self.monthbox.insert(0, 'mm')
        self.daybox.insert(0, 'dd')

        self.jumpbackmenu.menu = tk.Menu(self.jumpbackmenu, tearoff=0)
        self.jumpbackmenu['menu'] = self.jumpbackmenu.menu
        self.jumpbackmenu.menu.add_command(label='week')
        self.jumpbackmenu.menu.add_command(label='month')
        self.jumpbackmenu.menu.add_command(label='year')
        self.jumpforwardmenu.menu = tk.Menu(self.jumpforwardmenu, tearoff=0)
        self.jumpforwardmenu['menu'] = self.jumpforwardmenu.menu
        self.jumpforwardmenu.menu.add_command(label='week')
        self.jumpforwardmenu.menu.add_command(label='month')
        self.jumpforwardmenu.menu.add_command(label='year')

        self.doctormenu.menu = tk.Menu(self.doctormenu, tearoff=0)
        self.doctormenu['menu'] = self.doctormenu.menu
        self.doctormenu.menu.add_command(label='Jessica')        

        self.viewmenu.menu = tk.Menu(self.viewmenu, tearoff=0)
        self.viewmenu['menu'] = self.viewmenu.menu
        self.viewmenu.menu.add_command(label='day', command=self.View_Day)
        self.viewmenu.menu.add_command(label='week', command=self.View_Week)
        self.viewmenu.menu.add_command(label='month', command=self.View_Month)        

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

    def View_Day(self, event=None):
        try:
            self.calendarspace.destroy()
        except:
            pass
        self.calendarspace = Day(self)
        self.calendarspace.grid(row=1, column=0, columnspan=11, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        self.view = 'day'

    def View_Week(self):
        try:
            self.calendarspace.destroy()
        except:
            pass
        self.calendarspace = Week(self, 9)
        self.calendarspace.grid(row=1, column=0, columnspan=11, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        self.view = 'week'

    def View_Month(self):
        try:
            self.calendarspace.destroy()
        except:
            pass
        self.calendarspace = Month(self)
        self.calendarspace.grid(row=1, column=0, columnspan=11, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
        self.view = 'month'

    def Refresh(self):
        if self.view == 'day':
            self.View_Day()
        elif self.view == 'week':
            self.View_Week()
        elif self.view == 'month':
            self.View_Month()
        else:
            self.log.error('Refresh failed to understand self.view variable')

    def Close(self):
        self.root.calendar = None
        self.destroy()
