from datetime import datetime, timedelta
import logging
from time import sleep
from os.path import isfile, isdir
from os import mkdir
import string

class DataBase(object):
    # This list allows one to easily increment the id
    iditteration = list(str(i) for i in range(10)) + list(i for i in string.ascii_letters)
    # These fields MUST be in the first line of all files
    # -_id: a unique id assigned to every file
    # -createdon_date: the date on which this document was first created, formatted as %Y/%m/%d which is yyyy/mm/dd
    # -createdon_time: the time of the day, formatted as %H:%M:%S which is 24hour:minute:second
    # -open: is to track if this file has been opened for editing, left as False when just viewing
    # -lastedited: contains both date and time the file was last edited, formatted as %Y/%m/%d %H:%M:%S. Used for tracking changes
    headerfields = {'_id':str(), 'createdon_date':str(), 'createdon_time':str(), 'open':bool(), 'lastedited':str()}

    folder = 'database/'
    # This file stores the current global unique id
    idfile = folder+'.idfile.db'

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.openfiles = []
        

    # Updates the id file so that it is globally known what the current highest id is. eliminates duplicates.
    def _GetNewID(self):
        # Read the current id, leave the file blank so that nothing else will use it. If the file is blank, wait and try again
        while True:
            with open(DataBase.idfile,'r') as f:
                _id = f.read().strip()
            if _id == '-':
                sleep(0.1)
            else:
                with open(DataBase.idfile,'w') as f:
                    f.write('-')
                break

        # Check that the id is formatted properly
        if not _id.isalnum():
            raise RuntimeError('ID file corrupted! must manually fix the file')

        allZ = True
        # Find the first iterable location (ie 3rd spot for '11111ZZ', indexed as -3)
        for i in range(len(_id)):
            if _id[-1-i] != 'Z':
                iterateindex = -1-i
                allZ = False
                break

        if allZ:
            # If a place cannot be found, add a new order/spot
            _id = '0'*(len(_id)+1)
        else:
            # Increment the found index
            _id[iterateindex] = DataBase.iditteration[DataBase.iditteration.index(_id[iterateindex])+1]

            # Set everything below it to zeros
            for i in range(iterateindex+1,0):
                _id[i] = '0'

        # Write the id to the file so the next function can use it
        with open(DataBase.idfile, 'w') as f:
            f.write(_id)

        self.log.info('created ID: %s.' % _id)
        return _id

    # Opens a file solely for the purpose of viewing, you cannot save alterations if the file is opened by this method (use _Open)
    # -filename: a string with the location of the file
    def _View(self, filename):
        # Check the file exists
        if isfile(filename):
            with open(filename, 'r') as f:
                # Read each line of the file as a python expression (a dictionary)
                contents = map(lambda s: eval(s.strip()), f.readlines())
        else:
            raise IOError('Could not find: ' + filename)

        self.log.info('viewing file: %s.' % filename)
        return contents

    # Opens a file for the purpose of altering it, sets a warning so that others know it may change soon. returns the contents
    # -filename: a string with the location of the file
    def _Open(self, filename):
        # Start by getting the contents in view mode
        contents = self._View(filename)

        # If the file is opened for writing by someone else, raise error
        if contents[0]['open'] == True:
            raise RuntimeError('Someone else is using this file')

        # Set the contents so now I am potentially writing to it
        contents[0]['open'] = True

        # Write the contents with the adjusted 'open' parameter, so no one else touches the file
        with open(filename, 'w') as f:
            for line in contents:
                f.write(str(line)+'\n')

        # Track all opened files in this list
        self.openfiles.append(filename)

        self.log.info('opened file: %s.' % filename)
        return contents

    # Writes the contents of a database object to a file
    # -filename: a string with the location to write the file
    # -contents: a list of disctionaries (technically only the first element requires this)
    def _Write(self, filename, contents):
        # Check that the contents have the proper header information
        for key in DataBase.headerfields:
            if key not in contents[0]:
                raise AttributeError('header field(s) not present')

        # Check that these contents were actually intended for writing
        if contents[0]['open'] == False:
            raise RuntimeError('File was not accessed in write mode')

        # Check that the unique id is part of the filename
        if contents[0]['_id'] not in filename[filename.rfind('/')+1:filename.rfind('.')]:
            raise ValueError('contents id does not match filename id! invalid write attempt.')

        # If this file already exists, this will check that you actually opened it in write mode (using '_Open')
        try:
            checkcontents = self._View(filename)

            if checkcontents[0]['open'] == False:
                raise RuntimeError('File not opened for writing')
        except IOError:
            # Make the directory for the file if it does not exist
            if not isdir(filename[:filename.rfind('/')]):
                mkdir(filename[:filename.rfind('/')])
            
        # fixme add code to save the old version of the file here

        # Writes the contents to the file
        with open(filename, 'w') as f:
            for line in contents:
                f.write(str(line)+'\n')

        self.log.info('Wrote file: %s.' % filename)
        self.log.debug('file: %s now has contents:\n' % (filename, str(contents)))

    # Closes a file so it cannot be written to. Writes the contents of a database object to the file if provided
    # -filename: a string with the location to write the file
    # -contents: a list of disctionaries (technically only the first element requires this)
    def _Close(self, filename, contents = None):
        # Check that the object knows the file is open
        if filename not in self.openfiles:
            raise ValueError('the file: %s is not opened by this database object.' % filename)
            
        # Write the contents before closing
        if contents != None:
            self._Write(filename, contents)

        # Collect the contents as they are in the file
        curentcontents = self._View(filename)

        # If the file contents say it is already closed, this is a problem
        if curentcontents[0]['open'] == False:
            raise RuntimeError('File already closed, possible information loss!')

        # Switch the 'open' parameter, because this function is closing the file
        curentcontents[0]['open'] = False

        # Rewrite the contents with the changed 'open parameter'
        with open(filename, 'w') as f:
            for line in curentcontents:
                f.write(str(line)+'\n')

        # Remove the file from the list of opened files
        self.openfiles.pop(self.openfiles.index(filename))
        self.log.info('Closed file: %s.' % filename)

    # Closes all files which are known to be open
    def _Close(self):
        for f in self.openfiles:
            self._Close(f)
