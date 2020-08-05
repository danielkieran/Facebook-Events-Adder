import pickle
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import datefinder
import re

# timezone
time_zone = 'Europe/Dublin'

def create_event(start_time, end_time, summary, location, description):
    credentials = pickle.load(open("token.pkl", "rb")) # get credentials to manipulate calendar
    service = build("calendar", "v3", credentials=credentials)# v3 in reference https://developers.google.com/calendar/v3/reference
    global time_zone
    event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': time_zone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        
    print('Adding ' + summary + ' to calendar ...')
        
    return service.events().insert(calendarId='primary', body=event).execute()


def add_events(chosen_events, event_df, society):
    
    chosen_events = list(dict.fromkeys(chosen_events)) # removes duplicate values in user-input list
    
    for event in chosen_events:
        summary = event_df['event_title'].iloc[event-1]
        start_time = event_df['event_time'].iloc[event-1]
        location = event_df['event_loc'].iloc[event-1]
        if society == "empty":
            description = event_df['society'].iloc[event-1] + ' event.'
        else:
            description = society + ' event.'
        
        # The string values in the ['event_time'] column must be manipulated slightly in order for datefinder.find_dates to accurately determine the start and end time
        # This required a lot of testing and the following code fixes this 
        
        # *Note there are 5 different types of dates we could have collected from FB
        # 1) Thursday, April 16, 2020 at 3:00 PM UTC+01
        # 2) Friday, November 8, 2019 at 5:00 PM – 10:00 PM.
        # 3) 5 Dates · Oct 31, 2019 - Nov 28, 2019 · UTC
        # 4) Feb 16 at 11:30 AM – Feb 20 at 12:30 AM UTC
        # 5) Saturday, February 9, 2019 at 7:00 PM – 2:30 AM UTC

        filter_tuple = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        if '–' in start_time:
            if start_time.startswith(filter_tuple) == True: # Formatting dates for type 4
                start_time = start_time.replace('–', 'to')
                matches = list(datefinder.find_dates(start_time))
            else:
                result = re.search(',(.*) at', start_time)
                start_time = start_time.replace('–', 'to' + result.group(1) + ' at ')
                matches = list(datefinder.find_dates(start_time)) # Formatting dates for type 2
            
            end_time = matches[1]
            
            if start_time.count('PM') == 1 and start_time.count('AM') == 1 and start_time.find('PM') < start_time.find('AM'): # Formatting dates for type 5 -> when a PM time and ends in an AM time 
                end_time = end_time + timedelta(hours = 24)                                                                    #(in other words its the next day)
            start_time = matches[0]
        
        elif '-' in start_time:
            start_time = start_time.replace('-', 'to') # Formatting dates for type 3
            matches = list(datefinder.find_dates(start_time))
            end_time = matches[1]
            start_time = matches[0]
        
        else:
            matches = list(datefinder.find_dates(start_time)) # Formatting dates for type 1
            start_time = matches[0].replace(tzinfo=None)
            end_time = start_time + timedelta(hours = 1)
    
        create_event(start_time, end_time, summary, location, description)
        
        
    
    return 0

        