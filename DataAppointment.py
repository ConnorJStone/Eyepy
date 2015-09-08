from DataBase import DataBase
from datetime import datetime, timedelta
from os.path import isfile, join, isdir
from os import walk, mkdir
from glob import glob
import logging

class DataAppointment(DataBase):
    visiblefields = {'firstname':str(), 'lastname':str(), 'code':int(), 'year':int(), 'month':int(), 'day':int(), 'hour':int(), 'minute':int(), 'doctor':str(), 'healthcard'=str(), 'notes':str()}
    extrafields = {'patient_id':str()}

    folder = DataBase.folder+'appointments/'
    
    def __init__(self):
        DataBase.__init__(self)
        self.log = logging.getLogger(__name__)

    # Returns all of the information from the appointment with a given ID and date
    # -_id: file unique id
    # -date: a datetime object
    def View(self, _id, date):
        filename = folder+date.strftime('%Y/%m/%d/')+_id+'.appointment' 
        if isfile(filename):
            return self._View(filename)
        else:
            raise IOError('Could not find: '+filename)

    # Returns all of the information from the appointment with a given ID. FAR slower than the other option
    # -_id: file unique id
    def View(self, _id):
        filename = _id + '.appointment'
        for root, dirs, files in walk(DataAppointment.folder, False):
            if filename in files:
                filename = join(root,filename)
                break
        else:
            raise IOError('Could not find ID: %s in appointments folder' % _id)

        return self._View(filename)

    # Returns the information for all appointments on a given date
    # -date: a datetime object
    def View_All(self, date):
        allappointments = []
        
        for f in glob(DataAppointment.folder+date.strftime('%Y/%m/%d/')+'*.appointment'):
            allappointments.append(self._View(f))

        return allappointments

    # Returns all of the information from the appointment with a given ID and date
    # -_id: file unique id
    # -date: a datetime object
    def Open(self, _id, date):
        filename = folder+date.strftime('%Y/%m/%d/')+_id+'.appointment' 
        if isfile(filename):
            return self._Open(filename)
        else:
            raise IOError('Could not find: '+filename)

    # Returns all of the information from the appointment with a given ID. FAR slower than the other option
    # -_id: file unique id
    def Open(self, _id):
        filename = _id + '.appointment'
        for root, dirs, files in walk(DataAppointment.folder, False):
            if filename in files:
                filename = join(root,filename)
                break
        else:
            raise IOError('Could not find ID: %s in appointments folder' % _id)

        return self._Open(filename)

    # Writes the contents to its coresponding file, if this is a new appointment, it will create the header information
    # -contents: all of the appointment information
    def Write(self, contents):
        for key in ['year','month','day']:
            if key not in contents[1]:
                raise AttributeError('necessary field(s) not present for an appointment')
                
        if len(contents[0]) == 0:
            today = datetime.today()
            contents[0]['_id'] = self._GetNewID()
            contents[0]['createdon_date'] = today.strftime('%Y/%m/%d')
            contents[0]['createdon_time'] = today.strftime('%H:%M:%S')
            contents[0]['open'] = False
            contents[0]['lastedited'] = today.strftime('%Y/%m/%d %H:%M:%S')
            self.log.debug('Created new appointment:\n%s' % str(contents))

        try:
            folder = DataAppointment.folder+contents[0]['createdon_date']
            filename = folder+'/'+contents[0]['_id']+'.appointment'

            self._Write(filename, contents)
        except KeyError:
            raise ValueError('Contents did not contain necessary information')

    # Closes a file so others can write to it, if contents is not None, it will write the contents first, then close
    def Close(self, filename, contents = None):
        self._Close(filename, contents)

    # Called at the end to clean up any currently opened files
    def Close(self):
        self._Close()
