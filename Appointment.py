import Tkinter as tk
import logging
from Themes import Colours, Relief
#from DataAppointment import DataAppointment
#from DataPatient import DataPatient
#from DataDoctor import DataDoctor
from datetime import datetime, timedelta

#------------------------------------------------------------------------------
# Displays the information of an appointment
# Allows the fields to be edited, will then return the values if Get_Fields() is called
class Appointment(tk.Frame):
    # root:
    #     space for frame
    #     must have a datapatient and a datadoctor object that can be accessed
    
    def __init__(self, root, appointment_id = None, appointment_date = None):
        # Variables
        self.log = logging.getLogger(__name__)
        self.root = root
        self.colour = Colours.calendar
        self.relief = Relief.calendar
        self.appointment_id = appointment_id
        self.appointment_date = appointment_date
        self.entryboxes = []
        self.entrystrings = []
        self.doctor = tk.StringVar()
        
        # Build Wondow
        tk.Frame.__init__(self, root, bg=self.colour['frame'])

        # Configure Window
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        for i in range(7):
            self.grid_rowconfigure(i, weight=0)

        # Widgets
        self.appointmentlabel = tk.Label(self, bg=self.colour['label'], relief=self.relief['label'])
        self.doctormenu = tk.Menubutton(self,
                                        text='Doctor',
                                        bg=self.colour['button'],
                                        relief=self.relief['button'],
                                        activebackground=self.colour['buttonactive'])

        # -Labels
        self.datelabel = tk.Label(self, text='Date (yyyy/mm/dd)', bg=self.colour['label'], relief=self.relief['label'])
        self.timelabel = tk.Label(self, text='Time (hh:mm)', bg=self.colour['label'], relief=self.relief['label'])
        self.firstnamelabel = tk.Label(self, text='First Name', bg=self.colour['label'], relief=self.relief['label'])
        self.lastnamelabel = tk.Label(self, text='Last Name', bg=self.colour['label'], relief=self.relief['label'])
        self.codelabel = tk.Label(self, text='Code', bg=self.colour['label'], relief=self.relief['label'])
        self.noteslabel = tk.Label(self, text='Notes', bg=self.colour['label'], relief=self.relief['label'])
        self.doctorlabel = tk.Label(self, text='Doctor', bg=self.colour['label'], relief=self.relief['label'])

        # -Entry boxes
        for i in range(6):
            self.entrystrings.append(tk.StringVar())
            self.entryboxes.append(tk.Entry(self, bg=self.colour['entry'], relief=self.relief['entry'], textvariable=self.entrystrings[i]))
        

        # Widgets config
        self.entryboxes[0].config(validate='focusout', validatecommand=self.Date_Valid)
        
        self.doctormenu.menu = tk.Menu(self.doctormenu, tearoff=0)
        self.doctormenu['menu'] = self.doctormenu.menu
        for doc in root.datadoctor.View_All():
            self.doctormenu.menu.add_radiobutton(label=doc[1]['firstname'], value=doc[0]['_id'], variable=self.doctor)

        self.Fill_Fields()
        
        # Place Widgets
        self.appointmentlabel.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.datelabel.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.timelabel.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.firstnamelabel.grid(row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.lastnamelabel.grid(row=4, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.codelabel.grid(row=5, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.noteslabel.grid(row=6, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.doctorlabel.grid(row=7, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        for i in range(6):
            self.entryboxes[i].grid(row=1+i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.doctormenu.grid(row=7, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    # Using the database, will search for the appointment and fill what fields it can    
    def Fill_Fields(self):
        if self.appointment_id == None:
            return

        try:
            if self.appointment_date == None:
                fields = root.dataappointment.View(self.appointment_id)[1]
            else:
                fields = root.dataappointment.View(self.appointment_id, self.appointment_date)[1]                
        except:
            return

        if 'date' in fields:
            self.entrystrings[0].set(fields['date'])
        if 'time' in fields:
            self.entrystrings[1].set(fields['time'])
        if 'patient_id' in fields:
            patient = self.root.datapatient.View(fields['patient_id'])
            self.entrystrings[2].set(patient[1]['firstname'])
            self.entrystrings[3].set(patient[1]['lastname'])
        if 'code' in fields:
            self.entrystrings[4].set(fields['code'])
        if 'notes' in fields:
            self.entrystrings[5].set(fields['notes'])
        if 'doctor_id' in fields:
            doctor = self.root.datadoctor.View(fields['doctor_id'])
            self.doctor.set(doctor['firstname'])


    # Returns the appointment data which has been entered into the window
    def Get_Fields(self):
        fields = {}
        date = datetime.strptime(self.entrystrings[0].get(), '%Y/%m/%d')
        fields['date'] = date.strftime('%Y/%m/%d')
        try:
            date = datetime.strptime('2015/01/01 '+self.entrystrings[1].get(), '%Y/%m/%d %H:%M')
            fields['time'] = date.strftime('%H:%M')
        except:
            pass

        fields['firstname'] = self.entrystrings[2].get()
        fields['lastname'] = self.entrystrings[3].get()
        fields['code'] = self.entrystrings[4].get()
        fields['notes'] = self.entrystrings[5].get()
        fields['doctor_id'] = self.doctor.get()

        return fields

    # Checks if the date currently entered is a valid date
    def Date_Valid(self, event=None):
        try:
            date = datetime.strptime(self.entrystrings[0].get(), '%Y/%m/%d')
            return True
        except:
            return False
            
    def Close(self):
        pass
