from DataBase import DataBase
from datetime import datetime, timedelta
from os.path import isfile, join, isdir
from os import walk, mkdir
from glob import glob
import logging

#------------------------------------------------------------------------------
# For viewing and manipulating doctor data, this will access and maintain all database entries about doctors
class DataDoctor(DataBase):
    doctorfields = {'firstname':str(), 'lastname':str(), 'designation':str(), 'notes':str()}

    folder = DataBase.folder+'doctors/'

    def __init__(self):
        DataBase.__init__(self)
        self.log = logging.getLogger(__name__)

    # Given the id or the name of a doctor, will find them and return their atributes
    # -_idorname: string with the unique id or the doctor name, unique id is best
    def View(self, _idorname):
        searchresults = glob(DataDoctor.folder+'*'+_idorname+'*.doctor')
        if len(searchresults) != 1:
            raise IOError('Could not find doctor or id: %s' % _idorname)
        return self._View(searchresults[0])

    # Returns a list of the atributes for every active doctor
    def View_All(self):
        alldoctors = []
        for f in glob(DataDoctor.folder+'*.doctor'):
            alldoctors.append(self._View(f))

        return alldoctors

    # Given the id or the name of a doctor, will find them and return their atributes. sets file to writable mode
    # -_idorname: string with the unique id or the doctor name, unique id is best
    def Open(self, _idorname):
        searchresults = glob(DataDoctor.folder+'*'+_idorname+'*.doctor')
        if len(searchresults) != 1:
            raise IOError('Could not find doctor or id: %s' % _idorname)
        return self._Open(searchresults[0])

    # Writes the doctor atributes to a file
    # -contents: list containing an empty or prefilled dictionary at 0, and all the doctor atribtes at 1
    def Write(self, contents):
        for key in ['firstname', 'lastname']:
            if key not in contents[1]:
                raise AttributeError('necessary field(s) not present for doctor')
                
        try:
            self._NewHeader(contents)
        except ValueError:
            pass

        filename = DataDoctor.folder+contents[0]['_id']+'_'+contents[1]['firstname'].lower()+contents[1]['lastname'].lower()+'.doctor'

        self._Write(filename, contents)

    # Sets the open flag to false so the file can no longer be writen to. Will write the contents first, if they are given
    def Close(self, filename, contents=None):
        self._Close(filename, contents)

    # To be called at closing, ensures no files were left open
    def Close(self):
        self._Close()
        
