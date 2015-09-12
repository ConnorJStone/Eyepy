from DataBase import DataBase
from datetime import datetime, timedelta
from os.path import isfile, join, isdir
from os import walk, mkdir, remove
from glob import glob
import logging

#------------------------------------------------------------------------------
# For accessing and manipulating all database entries related to patients
class DataPatient(DataBase):
    # These fields go in the line after the header
    patientfields = {'designation':'Designation', 'firstname':'First Name', 'lastname':'Last Name', 'preferedname':'Prefered Name', 'phone_home':'Home Phone #', 'phone_cell':'Cell Phone #', 'phone_work':'Work Phone #', 'address_street':'Street #', 'address_province':'Province', 'address_postalcode':'Postal Code', 'address_city':'City', 'dateofbirth':'Date of Birth', 'doctor_id':'Doctor Unique ID', 'medicaldoctor':'Medical Doctor', 'typicalcode':'Typical Code', 'healthcard':'Healthcard #', 'futureappointments':dict(), 'pastappointments':dict(), 'notes':'Notes', 'family_id':list()}
    # This is the order to display the fields in a patient view, note that not all fields are visible
    patientvieworder = ['designation','firstname','lastname','preferedname','phone_home','phone_cell','phone_work','address_street','address_province','address_postalcode','address_city','dateofbirth','doctor_id','medicaldoctor','typicalcode','healthcard','notes']

    # All fields which hold insurance information
    insurancefields = {'company':'Company', 'plannumber':'Plan Number', 'planholder_name':'Name of Plan Holder', 'planholder_birthday':'Plan Holder Birthday', 'planholder_relation':'Relation to Plan Holder', 'fundingfor':'Plan Funds'}

    # All fields which hold information about the patients prescription
    prescriptionfields = {'od':'OD', 'os':'OS', 'glasses_rxdate':'Date of Rx for Glasses', 'glasses_rxexpire':'Date Glasses Rx Expires', 'glasses_sphere':'Glasses Sphere', 'glasses_cyl':'Glasses Cyl', 'glasses_axis':'Glasses Axis', 'glasses_add':'Glasses Add', 'glasses_height':'Glasses Height', 'glasses_prism':'Glasses Prism', 'contact_rxdate':'Date of Rx for Contacts', 'contact_rxexpire':'Date Contacts Rx Expires', 'contact_sphere':'Contacts Sphere', 'contact_cyl':'Contacts Cyl', 'contact_axis':'Contacts Axis', 'contact_add':'Contacts Add', 'contact_height':'Contacts Height', 'contact_prism':'Contacts Prism'}

    folder = DataBase.folder + 'patients/'
    
    def __init__(self):
        DataBase.__init__(self)
        self.log = logging.getLogger(__name__)

    # Given the id or the name of a patient, will find them and return their atributes
    # -_idorname: string with the unique id or the patient name, unique id is best
    def View(self, _idorname, fields = []):
        searchresults = glob(DataPatient.folder+'*'+_idorname+'*.patient')
        if len(searchresults) != 1:
            raise IOError('Could not find patient or id: %s' % _idorname)
        return self._View(searchresults[0], fields)

    # Returns a list of the atributes for every active patient
    def View_All(self, fields = []):
        allpatients = []
        for f in glob(DataPatient.folder+'*.patient'):
            allpatients.append(self._View(f, fields))

        return allpatients

    # Given the id or the name of a patient, will find them and return their atributes. sets file to writable mode
    # -_idorname: string with the unique id or the patient name, unique id is best
    def Open(self, _idorname):
        searchresults = glob(DataPatient.folder+'*'+_idorname+'*.patient')
        if len(searchresults) != 1:
            raise IOError('Could not find patient or id: %s' % _idorname)
        return self._Open(searchresults[0])

    # Writes the patient atributes to a file
    # -contents: list containing an empty or prefilled dictionary at 0, and all the patient atribtes at 1
    def Write(self, contents):
        for key in ['firstname', 'lastname']:
            if key not in contents[1]:
                raise AttributeError('necessary field(s) not present for patient')
                
        try:
            self._NewHeader(contents)
        except ValueError:
            pass

        filename = self.PatientFolder(contents)

        try:
            oldcontents = self.View(contents[0]['_id'])
            if oldcontents[1]['firstname'] != contents[1]['firstname'] or oldcontents[1]['lastname'] != contents[1]['lastname']:
                print 'in if'
                oldfilename = self.PatientFolder(oldcontents)
                remove(oldfilename)
                self.openfiles.pop(self.openfiles.index(oldfilename))
                print 'removed I think'
        except:
            oldcontents = []

        try:
            self._Write(filename, contents)
        except:
            if oldcontents != []:
                self._Write(filename, oldcontents)


    # Creats the filepath to a patient's database entry
    def PatientFolder(self, contents):
        return DataPatient.folder+contents[0]['_id']+'_'+contents[1]['firstname'].lower()+contents[1]['lastname'].lower()+'.patient'

    # Sets the open flag to false so the file can no longer be writen to. Will write the contents first, if they are given
    def Close(self, filename, contents=None):
        self._Close(filename, contents)

    # To be called at closing, ensures no files were left open
    def Close(self):
        self._Close()
        
