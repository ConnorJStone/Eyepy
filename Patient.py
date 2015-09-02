import Tkinter as tk
from Themes import Colours, Relief
from Appointment import AppointmentBase
import logging


#------------------------------------------------------------------------------
class PatientList(tk.Frame):
    # root:
    #     space for frame
    #     variable "sortby" has a string
    #     variable "searchby" has a dictionary indexed by strings with boolean values
    #     variable "doctor" has a string
    
    def __init__(self,root):
        # Variables
        self.colour = Colours.patient
        self.relief = Relief.patient
        self.log = logging.getLogger('op.patient.list')
        self.patients = []
        self.root = root
        self.patientview = None
        
        # Build Window
        tk.Frame.__init__(self,root, bg=self.colour['frame'])

        # Configure Window
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Label
        self.listlabel = tk.Label(self,text='Sorted by: Name, Doctor: Jessica', bg=self.colour['label'], relief=self.relief['label'])
        self.listlabel.grid(row=0,column=0,columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # List box with scroll bar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
        self.patientlistbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.patientlistbox.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.scrollbar['command'] = self.patientlistbox.yview

        # Bind Double Click to switch to day view
        self.patientlistbox.bind('<Double-Button-1>', self.Patient_View)

        self.Fill()


    def Fill(self):#deleteme
        for i in range(100):
            self.patientlistbox.insert(tk.END, 'this person, %d' % i)

    def Patient_View(self, event=None):
        if not PatientView.isopen:
            self.patientview = PatientView(self)

class PatientView(tk.Toplevel):
    # root:
    #     no space needed

    isopen = False
    
    def __init__(self, root):
        PatientView.isopen = True
        
        # Variables
        self.colour = Colours.patient
        self.relief = Relief.patient
        self.root = root

        # Build Window
        tk.Toplevel.__init__(self,root, bg=self.colour['frame'])
        self.title('Patient')
        self.protocol('WM_DELETE_WINDOW', self.Close)
        
        # Configure Window
        for i in range(6): self.grid_columnconfigure(i,weight=1)
        for i in range(8): self.grid_rowconfigure(i,weight=0)

        # Widgets
        self.labels = {}
        self.entryfields = {}
        self.labels['designation'] = tk.Label(self,text='Designation')
        self.labels['firstname'] = tk.Label(self, text='First Name')
        self.labels['lastname'] = tk.Label(self, text='Last Name')
        self.labels['preferedname'] = tk.Label(self, text='Prefered Name')
        self.labels['phonenumber_home'] = tk.Label(self, text='Home Number')
        self.labels['phonenumber_cell'] = tk.Label(self, text='Cell Number')
        self.labels['phonenumber_work'] = tk.Label(self, text='Work Number')
        self.labels['address_number'] = tk.Label(self, text='Street Number')
        self.labels['address_name'] = tk.Label(self, text='Street Name')
        self.labels['address_province'] = tk.Label(self, text='Province')
        self.labels['address_city'] = tk.Label(self, text='City')
        self.labels['address_postalcode'] = tk.Label(self, text='Postal Code')
        self.labels['dateofbirth'] = tk.Label(self, text='Date Of Birth')
        self.labels['healthcardnumber'] = tk.Label(self,text='Healthcard Number')
        self.labels['doctor'] = tk.Label(self, text='Doctor')
        self.labels['medicaldoctor'] = tk.Label(self,text='Medical Doctor')
        self.labels['typicalcode'] = tk.Label(self, text='Typical Code')

        for l in self.labels:
            self.entryfields[l] = tk.Entry(self, bg=self.colour['entry'], relief=self.relief['entry'])


        self.copybutton = tk.Button(self, text='Copy', highlightthickness=0, bg=self.colour['button'], relief=self.relief['button'])
        self.appointmentbutton = tk.Button(self, text='Appointment', highlightthickness=0, bg=self.colour['button'], relief=self.relief['button'], command=self.NewAppointment)
        self.invoicemenu = tk.Menubutton(self,text='Invoice', bg=self.colour['button'], relief=self.relief['button'])
        self.prescriptionmenu = tk.Menubutton(self, text='Prescription', bg=self.colour['button'], relief=self.relief['button'])
        self.miscmenu = tk.Menubutton(self, text='Misc', bg=self.colour['button'], relief=self.relief['button'])
        self.refreshbutton = tk.Button(self,text='Refresh', highlightthickness=0, bg=self.colour['button'], relief=self.relief['button'])
        self.savebutton = tk.Button(self, text='Save', highlightthickness=0, bg=self.colour['savebutton'], relief=self.relief['savebutton'])

        # Menu Definitions
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
        self.copybutton.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.appointmentbutton.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.invoicemenu.grid(row=0, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.prescriptionmenu.grid(row=0, column=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.miscmenu.grid(row=0, column=4, sticky=tk.N+tk.E+tk.S+tk.W)
        self.refreshbutton.grid(row=0, column=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self.savebutton.grid(row=0,column=6, sticky=tk.N+tk.E+tk.S+tk.W) 
        self.labels['designation'].grid(row=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['firstname'].grid(row=1, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['lastname'].grid(row=1, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['preferedname'].grid(row=1, column=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['phonenumber_home'].grid(row=1, column=4, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['phonenumber_cell'].grid(row=1, column=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['phonenumber_work'].grid(row=1, column=6, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['address_number'].grid(row=3, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['address_name'].grid(row=3, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['address_province'].grid(row=3, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['address_city'].grid(row=3, column=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['address_postalcode'].grid(row=3, column=4, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['dateofbirth'].grid(row=3, column=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['healthcardnumber'].grid(row=3, column=6, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['doctor'].grid(row=5, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['medicaldoctor'].grid(row=5, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.labels['typicalcode'].grid(row=5, column=2, sticky=tk.N+tk.E+tk.S+tk.W)

        self.entryfields['designation'].grid(row=2, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['firstname'].grid(row=2, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['lastname'].grid(row=2, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['preferedname'].grid(row=2, column=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['phonenumber_home'].grid(row=2, column=4, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['phonenumber_cell'].grid(row=2, column=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['phonenumber_work'].grid(row=2, column=6, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['address_number'].grid(row=4, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['address_name'].grid(row=4, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['address_province'].grid(row=4, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['address_city'].grid(row=4, column=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['address_postalcode'].grid(row=4, column=4, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['dateofbirth'].grid(row=4, column=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['healthcardnumber'].grid(row=4, column=6, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['doctor'].grid(row=6, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['medicaldoctor'].grid(row=6, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.entryfields['typicalcode'].grid(row=6, column=2, sticky=tk.N+tk.E+tk.S+tk.W)
        


    def NewAppointment(self):
        if not AppointmentBase.isopen:
            self.appointment = AppointmentBase(self)
        
    def Close(self):
        PatientView.isopen = False
        self.destroy()
        
