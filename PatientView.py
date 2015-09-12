import Tkinter as tk
from Themes import Colours, Relief
import logging
from DataDoctor import DataDoctor

#------------------------------------------------------------------------------
# Holds all the accessable information about a patient
class PatientView(tk.Frame):
    # root:
    #     space for frame

    def __init__(self, root, patient_id=None):
        # Variables
        self.log = logging.getLogger(__name__)
        self.colour = Colours.patientbase
        self.relief = Relief.patientbase
        self.datadoctor = DataDoctor()
        self.root = root
        self.patient_id = patient_id
        self.labels = []
        self.entryboxes = []
        self.entryboxvariables = []
        self.doctormenu = None
        self.doctorvariable = tk.StringVar()

        # Build Window
        tk.Frame.__init__(self, root, bg=self.colour['frame'], relief=self.relief['frame'])

        # Configure Window
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        for i in range(len(DataPatient.patientvieworder)):
            self.grid_rowconfigure(i, weight=1)
        
        # Widgets
        for pf in DataPatient.patientvieworder:
            if pf != 'doctor_id':
                self.entryboxvariables.append(tk.StringVar())
                self.labels.append(tk.Label(self, text=DataPatient.patientfields[pf], bg=self.colour['label'], relief=self.relief['label']))                
                self.entryboxes.append(tk.Entry(self, textvariable=self.entryboxvariables[-1], bg=self.colour['entry'], relief=self.relief['entry']))
            else:
                self.labels.append(tk.Label(self, text='Doctor', bg=self.colour['label'], relief=self.relief['label']))
                self.entryboxes.append(None)
                self.entryboxvariables.append(None)

        self.doctormenu = tk.Menubutton(self,
                                        text='',
                                        bg=self.colour['entry'],
                                        relief=self.relief['entry'],
                                        anchor=tk.W,
                                        activebackground=self.colour['buttonactive'])
        
        # Configure Widgets
        self.doctormenu.menu = tk.Menu(self.doctormenu, tearoff=0)
        self.doctormenu['menu'] = self.doctormenu.menu
        for doc in self.datadoctor.View_All():
            self.doctormenu.menu.add_radiobutton(label=doc[1]['firstname'], value=doc[0]['_id'], variable=self.doctorvariable, command=self.DoctorSelectTextUpdate)

        self.Fill_Fields()

        # Place Widgets
        for l in range(len(self.labels)):
            self.labels[l].grid(row=l, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
            if DataPatient.patientvieworder[l] != 'doctor_id':
                self.entryboxes[l].grid(row=l, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
            else:
                self.doctormenu.grid(row=l, column=1, sticky=tk.N+tk.E+tk.S+tk.W)


    # Loads information from the database and puts it in the correct fields
    def Fill_Fields(self, refresh=False):
        if refresh:
            patient = self.root.datapatient.View(self.patient_id)
        else:
            patient = self.root.datapatient.Open(self.patient_id)

        for i in range(len(DataPatient.patientvieworder)):
            if DataPatient.patientvieworder[i] != 'doctor_id':
                self.entryboxvariables[i].set(patient[1][DataPatient.patientvieworder[i]])
            else:
                self.doctorvariable.set(patient[1][DataPatient.patientvieworder[i]])

        self.DoctorSelectTextUpdate()

    # Changes the menu text so that it displays the selected doctor
    def DoctorSelectTextUpdate(self):
        self.doctormenu.config(text=self.datadoctor.View(self.doctorvariable.get())[1]['firstname'])

    # Collects the information entered in each field
    def Get_Fields(self, event=None):
        fields = {}
        
        for i in range(len(DataPatient.patientvieworder)):
            if self.entryboxes[i] != None:
                fields[DataPatient.patientvieworder[i]] = self.entryboxvariables[i].get()
            else:
                fields[DataPatient.patientvieworder[i]] = self.doctorvariable.get()

        return fields

    # Reloads the information about the patient from the database
    def Refresh(self, event=None):
        self.Fill_Fields(True)

    def Close(self):
        self.datadoctor.Close()
