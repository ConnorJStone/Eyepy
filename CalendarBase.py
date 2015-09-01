import Tkinter as tk
import logging
from Themes import Colours, Relief
from Calendar import Day, Week, Month

class CalendarBase(tk.Toplevel):
    # root:
    #     no space needed

    isopen = False
    
    def __init__(self, root):
        CalendarBase.isopen = True
        
        # Variables
        self.log = logging.getLogger('op.calendar')
        self.colour = Colours.calendarbase
        self.relief = Relief.calendarbase
        self.root = root
        self.doctor = tk.StringVar()
        self.view = tk.StringVar()
        
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

    def View_Set(self, event=None):
        try:
            self.calendarspace.destroy()
        except:
            pass
        if self.view.get() == 'day':
            self.calendarspace = Day(self)
        elif self.view.get() == 'week':
            self.calendarspace = Week(self, 9)
        elif self.view.get() == 'month':
            self.calendarspace = Month(self)
        else:
            self.log.error('Calendar Base: Could not set view, unrecognized self.view value: %s' % self.view.get())
        self.calendarspace.grid(row=1, column=0, columnspan=11, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)
            
    def View_Day(self, event=None):
        self.view.set('day')
        self.View_Set()
        
    def View_Week(self, event=None):
        self.view.set('week')
        self.View_Set()

    def View_Month(self, event=None):
        self.view.set('month')
        self.View_Set()

    def Refresh(self, event=None):
        self.View_Set()

    def Close(self):
        CalendarBase.isopen = False
        self.destroy()
