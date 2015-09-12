import Tkinter as tk
import logging
from Themes import Colours, Relief
from DataAppointment import DataAppointment
from DataPatient import DataPatient
from DataDoctor import DataDoctor
from datetime import datetime, timedelta
from Appointment import Appointment

#------------------------------------------------------------------------------
# Creates a window to display an appointment, also allows modification and creation of appointments
class AppointmentBase(tk.Toplevel):
    # root:
    #     no space needed
    #     variable 'appointment' can be set to None
    
    isopen = False
    
    def __init__(self,root, appointment_id = None):
        AppointmentBase.isopen = True
        
        # Variables
        self.log = logging.getLogger(__name__)
        self.colour = Colours.calendarbase
        self.relief = Relief.calendarbase
        self.root = root
        self.appointment_id = appointment_id
        self.dataappointment = DataAppointment()
        self.datapatient = DataPatient()
        self.datadoctor = DataDoctor()
        
        # Build Window
        tk.Toplevel.__init__(self,root,bg=self.colour['frame'])
        self.title('Appointment')
        self.protocol('WM_DELETE_WINDOW', self.Close)

        # Configure Window
        for i in range(4): self.grid_columnconfigure(i,weight=1)
        
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
        # Widgets
        self.checkbutton = tk.Button(self, text='Check', bg=self.colour['button'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        self.seepatientbutton = tk.Button(self, text='See Patient', bg=self.colour['button'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        self.typemenu = tk.Menubutton(self, text='Type', bg=self.colour['button'], relief=self.relief['button'])
        self.printbutton = tk.Button(self, text='Print', bg=self.colour['button'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'])
        self.savebutton = tk.Button(self, text='Save', bg=self.colour['savebutton'], highlightthickness=0, activebackground=self.colour['buttonactive'], relief=self.relief['button'], command=self.SaveAppointment)
        self.appointment = Appointment(self, self.appointment_id)
        
        # Place Widgets
        self.checkbutton.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W)
        self.seepatientbutton.grid(row=0,column=1,sticky=tk.N+tk.E+tk.S+tk.W)
        self.typemenu.grid(row=0,column=2,sticky=tk.N+tk.E+tk.S+tk.W)
        self.printbutton.grid(row=0,column=3,sticky=tk.N+tk.E+tk.S+tk.W)
        self.savebutton.grid(row=0,column=4,sticky=tk.N+tk.E+tk.S+tk.W)
        self.appointment.grid(row=1,column=0,columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)

    # Method to save the current appointment to the database
    def SaveAppointment(self, event=None):
        try:
            appointment = self.dataappointment.View(self.appointment_id)
        except:
            appointment = [{},{}]

        fields = self.appointment.Get_Fields()
        for key in fields:
            appointment[1][key] = fields[key]
            
        if 'patient_id' not in appointment[1]:
            try:
                patient = self.datapatient.View(appointment[1]['firstname'].lower()+appointment[1]['lastname'].lower())
                appointment[1]['patient_id'] = patient[0]['_id']
            except:
                print 'failed to get patient id'
        del appointment[1]['firstname']
        del appointment[1]['lastname']

        self.dataappointment.Write(appointment)

        self.Close()
        
    def Close(self):
        AppointmentBase.isopen = False
        self.root.appointment = None
        self.dataappointment.Close()
        self.appointment.Close()
        self.destroy()
