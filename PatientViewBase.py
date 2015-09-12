import Tkinter as tk
from Themes import Colours, Relief
import logging
from DataPatient import DataPatient

from AppointmentBase import AppointmentBase
from PatientView import PatientView

#------------------------------------------------------------------------------
# Creates the window to view a patient and their informaiton
class PatientViewBase(tk.Toplevel):
    # root:
    #     no space needed
    #     variable 'patientview' can be set to None

    isopen = False
    
    def __init__(self, root, patient_id=None):
        PatientViewBase.isopen = True

        # Variables
        self.log = logging.getLogger(__name__)
        self.colour = Colours.patient
        self.relief = Relief.patient
        self.root = root
        self.patient_id = patient_id
        self.patientview = None
        self.datapatient = DataPatient()
        
        # Build Window
        tk.Toplevel.__init__(self, root, bg=self.colour['frame'], relief=self.relief['frame'])
        self.title('Patient View')
        self.protocol('WM_DELETE_WINDOW', self.Close)

        # Configure Window
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Widgets
        self.appointmentbutton = tk.Button(self, text='Appointment', highlightthickness=0, bg=self.colour['button'], relief=self.relief['button'])
        self.invoicemenu = tk.Menubutton(self,text='Invoice', bg=self.colour['button'], relief=self.relief['button'])
        self.prescriptionmenu = tk.Menubutton(self, text='Prescription', bg=self.colour['button'], relief=self.relief['button'])
        self.miscmenu = tk.Menubutton(self, text='Misc', bg=self.colour['button'], relief=self.relief['button'])
        self.refreshbutton = tk.Button(self,text='Refresh', highlightthickness=0, bg=self.colour['button'], relief=self.relief['button'], command=self.Refresh)
        self.savebutton = tk.Button(self, text='Save', highlightthickness=0, bg=self.colour['savebutton'], relief=self.relief['savebutton'], command=self.SavePatient)

        self.patientview = PatientView(self, self.patient_id)

        # Widget Configure
        self.invoicemenu.menu = tk.Menu(self.invoicemenu, tearoff=0)
        self.invoicemenu['menu'] = self.invoicemenu.menu
        self.invoicemenu.menu.add_command(label='Frame')        
        self.invoicemenu.menu.add_command(label='Lense')        
        self.invoicemenu.menu.add_command(label='Misc')

        self.prescriptionmenu.menu = tk.Menu(self.prescriptionmenu, tearoff=0)
        self.prescriptionmenu['menu'] = self.prescriptionmenu.menu
        self.prescriptionmenu.menu.add_command(label='Glasses')        
        self.prescriptionmenu.menu.add_command(label='Contacts')        

        self.miscmenu.menu = tk.Menu(self.miscmenu, tearoff=0)
        self.miscmenu['menu'] = self.miscmenu.menu
        self.miscmenu.menu.add_command(label='Print Patient Label')        
        self.miscmenu.menu.add_command(label='Print Address Label')        
        self.miscmenu.menu.add_command(label='Print Rx')        
        self.miscmenu.menu.add_command(label='Print CLRx')        
        self.miscmenu.menu.add_command(label='Print Copy Rx')        
        self.miscmenu.menu.add_command(label='Print Copy CLRx')        
        self.miscmenu.menu.add_command(label='Lab Order')        
        self.miscmenu.menu.add_command(label='Insurance Information')        
        self.miscmenu.menu.add_command(label='Delete Patient')        

        # Place Widgets
        self.appointmentbutton.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.invoicemenu.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.prescriptionmenu.grid(row=0, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.miscmenu.grid(row=0, column=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.refreshbutton.grid(row=0, column=4, sticky=tk.N+tk.E+tk.S+tk.W)
        self.savebutton.grid(row=0,column=5, sticky=tk.N+tk.E+tk.S+tk.W)

        self.patientview.grid(row=1, column=0, columnspan=6, sticky=tk.N+tk.E+tk.S+tk.W)

    # Saves the entered data to the database
    def SavePatient(self, event=None):
        try:
            patient = self.datapatient.View(self.patient_id)
        except IOError:
            patient = [{},{}]
        except RuntimeError:
            return

        patient[1] = self.patientview.Get_Fields()
        self.datapatient.Write(patient)
        self.Close()

    # Reload patient information from the database
    def Refresh(self, event=None):
        self.patientview.Refresh(event)

    def Close(self):
        PatientViewBase.isopen = False
        self.root.patientview = None
        self.datapatient.Close()
        self.patientview.Close()
        self.destroy()
