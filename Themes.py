#------------------------------------------------------------------------------
# All widget colours are controlled from here
class Colours():
    #Calendar
    calendarbase = {'frame':'#db4437',
                    'button':'#db4437',
                    'buttonactive':'red',
                    'savebutton':'orange',
                    'label':'grey',                    
                    'entry':'white'}

    calendar = {'frame':'white',
                'button':'#db4437',
                'buttonactive':'red',
                'savebutton':'orange',
                'entry':'white',
                'label':'grey'}

    #Patient
    patientbase = {'frame':'#0f9d58',
                   'button':'#0f9d58',
                   'buttonactive':'green',
                   'savebutton':'orange',
                   'entry':'white',
                   'label':'grey'}
    
    patient = {'frame':'#0f9d58',
               'button':'#0f9d58',
               'buttonactive':'green',
               'savebutton':'orange',
               'entry':'white',
               'label':'grey'}

    #Stock
    stockbase = {'frame':'#4285f4',
                 'button':'#4285f4',
                 'buttonactive':'blue',
                 'savebutton':'orange',
                 'entry':'white',
                 'label':'grey'}

    stock = {'frame':'#4285f4',
             'button':'#4285f4',
             'buttonactive':'blue',
             'savebutton':'orange',
             'entry':'white',
             'label':'grey'}


#------------------------------------------------------------------------------
# All widget reliefs are controlled from here
class Relief():
    #Calendar
    calendarbase = {'frame':'flat',
                    'button':'flat',
                    'entry':'flat',
                    'savebutton':'flat',
                    'label':'raised'}
    
    calendar = {'frame':'flat',
                'button':'flat',
                'savebutton':'flat',
                'entry':'flat',
                'label':'raised'}

    #Patient
    patientbase = {'frame':'flat',
                   'button':'flat',
                   'savebutton':'flat',
                   'entry':'flat',
                   'label':'raised'}
    
    patient = {'frame':'flat',
               'button':'flat',
               'savebutton':'flat',
               'entry':'flat',
               'label':'raised'}

    #Stock
    stockbase = {'frame':'flat',
                 'button':'flat',
                 'savebutton':'flat',
                 'entry':'flat',
                 'label':'raised'}
    
    stock = {'frame':'flat',
             'button':'flat',
             'savebutton':'flat',
             'entry':'flat',
             'label':'raised'}

#------------------------------------------------------------------------------
# All formats for dates are here
class Dates():
    dateformats = {'slashdate':'%Y/%m/%d',
                   'slashdate_colontime':'%Y/%m/%d %H:%M:%S',
                   'dashdate':'%Y-%m-%d',
                   'dashdate_colontime':'%Y-%m-%d %H:%M:%S',
                   'colontime':'%H:%M:%S'}

    
