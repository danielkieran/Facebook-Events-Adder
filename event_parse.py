import requests
from bs4 import BeautifulSoup
import json
from hidden import username, password
import pandas as pd

# DataFrame 
df = pd.read_csv('facebook_pages.csv', header=0)


def selection():
    # This function returns whether to sort by Uni or Society
    print('First question, sort by university or by culture?')
    while True: # loops until valid input is made
        try:
            txt = int(input('1 - University\n2 - Culture\n3 - Quit program\n'))
        except ValueError:
            print('Not a number!')
        else:
            if ( 0 < txt < 4):
                break
            else:
                print('Out of range. Try again')
    
    return txt

def selection2(list_type):
    # This function returns the second user selection
    global df
    # Sorted by University
    if list_type == 1:
        print('Select a University')
        uni_list = df['unis/societies'].copy().to_list()
        list_size = int(len(uni_list)+1)
        for number, uni in enumerate(uni_list):
            print(str(number+1) + ' - ' + str(uni))
        print('Please enter the number associated with the university.')
        while True: # loops until valid input is made
            try:
                txt = int(input())
            except ValueError:
                print('Not a number!')
            else:
                if ( 0 < txt < list_size):
                    break
                else:
                    print('Out of range. Try again')
        return txt
    # Sorted by Cultural society focus
    if list_type == 2:
        print('Select a Culture.')
        soc_list=list(df.copy())
        del soc_list[0]
        list_size = int(len(soc_list)+1)
        for number, soc in enumerate(soc_list):
            print(str(number+1) + ' - ' + str(soc))
        print('Please enter the number associated with the culture.')
        while True: # loops until valid input is made
            try:
                txt = int(input())
            except ValueError:
                print('Not a number!')
            else:
                if ( 0 < txt < list_size):
                    break
                else:
                    print('Out of range. Try again')
        return txt

def soc_list_by_uni(uni):
    # This function lists the societies by University
    global df
    df_uni = df.copy() #Don't want to manipulate the original dataframe so make a copy
    df_uni.set_index('unis/societies', inplace=True)
    series = df_uni.iloc[uni-1].dropna()
    soc_links = series.to_list()
    return soc_links

def soc_list_by_culture(culture):
    # This function lists societies by society focus
    global df
    df_cul = df.copy() # Don't want to manipulate original df so make a copy
    df_cul.rename(columns=df_cul.iloc[0])
    series = df_cul.iloc[:,culture].dropna()
    soc_links = series.to_list()
    return soc_links

def get_society(list_of_urls):
    # This function returns a number which represents a society from a list of societies
    length = len(list_of_urls)
    print('Found ' + str(length) + ' facebook pages!')
    payload = {                    # facebook asks for your email and password to facebook to make requests
            'email': username,
            'password': password
        }

    POST_LOGIN_URL = "http://www.facebook.com/login?"
    counter = 1
    for society_url in list_of_urls:

        with requests.Session() as session:
            post = session.post(POST_LOGIN_URL, data=payload)
            page = requests.get(society_url)
            soup = BeautifulSoup(page.content, "html.parser") # Html code of page in soup
            title = soup.title.text.replace(' - Events | Facebook', '') # manipulate the title text
            print(str(counter) + ' - ' + title) # associated number to society
        counter = counter + 1
    print(str(counter) + ' - All\nTo view events, enter a the number associated with a society or "All".') #Added an 'All' option to list all events from all societies
    while True: # loops until valid input is made
        try:
            txt = int(input(''))
        except ValueError:
                print('Not a number!')
        else:
            if ( 0 < txt < length+2):
                return txt
            else:
                print('Out of range. Try again')
    
def get_return():
    # This function checks whether the user wants to return
    print('Enter \'return\' to go back to main menu if they are no events you have interest in. Otherwise press any key to proceed.')
    
    while True:
        try:
            txt = str(input())
        except:
            ValueError
        else:
            if txt == 'return':
                return False
            return True
    
def get_list_of_events_to_add(events_df):
    # This function gets the list of events user wants to add
    row_count = events_df.shape[0]
    print('\nWhich events do you want to add to calender? (pick number between 1-' + str(row_count) + ')\nYou can enter up to ' + str(row_count) + ' events before entering any letter to stop.\n')
    while True: # gets a list of user inputs but stops when a non-integer is inputed. Also checks if whether values and length is valid
        try:
            my_list = []
            while True:
                my_list.append(int(input()))
        except:

            if  0 < len(my_list) <= row_count: # checks length of list
                if all(0 < i <= row_count for i in my_list) == True: # checks if values (for events) are valid
                    return [my_list, events_df]
            print('Something went wrong, try enter again.')

def select_event_from_society(fb_url):
    print('Collecting events ..')
    payload = {                         # facebook asks for your own fb account in order to make requests
            'email': username,
            'password': password
        }

    POST_LOGIN_URL = "http://www.facebook.com/login?"

    with requests.Session() as session:
        post = session.post(POST_LOGIN_URL, data=payload)
        page = requests.get(fb_url) # make request for fb page
        soup = BeautifulSoup(page.content, "html.parser") # html code from web page to variable soup
        title = soup.title.text.replace(' - Events | Facebook', '') # modify title text
        links = [a.get('href') for a in soup.find_all('a', href=True)] #https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
    
    series = pd.Series(links, index = links) # series of links found in fb_urls
    event_links = series.loc[series.str.startswith('/events/', na=False)].to_list() # links that start with '/events' -> indicates its a facebook event url
    no_of_links = len(event_links) # number of event links

    if no_of_links < 1:
        print('No events found.')
        return 0
    else:
        print(str(no_of_links) + ' events found.')
        
        # lists will be used to add event details to main dataframe
        event_title_list = []
        time_list = []
        loc_list = []

        for i in range(0, no_of_links):
            event_links[i] = 'https://mbasic.facebook.com' + event_links[i]
        
        for event in event_links:
            with requests.Session() as session:
                post = session.post(POST_LOGIN_URL, data=payload)
                page = requests.get(event)
                soup = BeautifulSoup(page.content, "html.parser")
                title_filter = soup.find_all('h3') # title found in h3 tag, ignore the rest of soup
                time_filter = soup.find_all('dt') # time found in a dt tag, ignore the rest of soup
                loc_filter = soup.find_all('dd') # location found in the dd tag, ignore the rest of soup

            for detail in title_filter:
                detail = str(detail.text)
                if detail == 'Summary': # ignore the text which writes 'Summary'
                    pass
                else:
                    event_title_list.append(detail) # add title to list
            
            temp = []
            for detail in time_filter:
                detail = str(detail.text)
                temp.append(detail) # add text to temporary list
            time_list.append(temp[0])  # time is always found first so only add that to time_list, ignore rest

            temp = []
            for detail in loc_filter:
                detail = str(detail.text)
                temp.append(detail) # add text to temporary list
            loc_list.append(temp[-1]) # location is always found last so only add that to  time_list, ignore rest

        events_table = pd.DataFrame(
            {'event_title': event_title_list,
            'event_time': time_list,
            'event_loc': loc_list
            
            })
        events_table.index+=1
        print('\nEvents held by ' + str(title) + ':')
        print(events_table[['event_title','event_time']])
        ans = get_return()
        if ans == False:
            return False
        else:
            event_details = get_list_of_events_to_add(events_table)
            event_details.append(title) # Add the society name to the dataframe
            return event_details

def select_event_from_societies(fb_urls):
    print('Collecting events ..')
    payload = {                         # facebook asks for your own fb account in order to make requests
            'email': username,
            'password': password
        }

    POST_LOGIN_URL = "http://www.facebook.com/login?"
    
    all_events = pd.DataFrame(columns = ['event_title', 'event_time', 'event_loc', 'society']) # main dataframe

    for fb_url in fb_urls:
        with requests.Session() as session:
            post = session.post(POST_LOGIN_URL, data=payload)
            page = requests.get(fb_url)
            soup = BeautifulSoup(page.content, "html.parser") # html code from web page to variable soup
            title = soup.title.text.replace(' - Events | Facebook', '') # modify title text
            links = [a.get('href') for a in soup.find_all('a', href=True)] #https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions collect url links found in fb_url

        series = pd.Series(links, index = links) # series of links found in fb_urls
        event_links = series.loc[series.str.startswith('/events/', na=False)].to_list() # links that start with '/events' -> indicates its a facebook event url
        no_of_links = len(event_links)

        if no_of_links < 1: # no links
            print('No events found for ' + title + '\n')
    
        else:
            print(str(no_of_links) + ' events found for ' + title + '\n')

            # lists will be used to add event details to main dataframe
            event_title_list = [] 
            time_list = []
            loc_list = []

            for i in range(0, no_of_links):
                event_links[i] = 'https://mbasic.facebook.com' + event_links[i] # modify the links for http requests later  
            
            for event in event_links:
                with requests.Session() as session:
                    post = session.post(POST_LOGIN_URL, data=payload)
                    page = requests.get(event)
                    soup = BeautifulSoup(page.content, "html.parser")
                    title_filter = soup.find_all('h3') # title found in h3 tag, ignore the rest of soup
                    time_filter = soup.find_all('dt') # time found in a dt tag, ignore the rest of soup
                    loc_filter = soup.find_all('dd') # location found in the dd tag, ignore the rest of soup

                for detail in title_filter:
                    detail = str(detail.text)
                    if detail == 'Summary': # ignore the text which writes 'Summary'
                        pass
                    else:
                        event_title_list.append(detail) # add title to list
                
                temp = []
                for detail in time_filter:
                    detail = str(detail.text)
                    temp.append(detail) # add text to temporary list
                time_list.append(temp[0]) # time is always found first so only add that to time_list, ignore rest

                temp = []
                for detail in loc_filter:
                    detail = str(detail.text)
                    temp.append(detail) # add text to temporary list
                loc_list.append(temp[-1]) # location is always found last so only add that to  time_list, ignore rest

            events_table = pd.DataFrame(
                {'event_title': event_title_list,
                'event_time': time_list,
                'event_loc': loc_list,
                'society': title 
                
                })
        
            all_events = all_events.append(events_table, ignore_index = True) # append dataframe to main dataframe

    if all_events.empty == True:
        return False
    else:
        all_events.index+=1
        grouped_df = all_events.copy().groupby('society')
        print('Here is a list of all events.\n')
        for key, item in grouped_df: #item is each society df, key is the society name
            print(key, "\n")
            print(grouped_df.get_group(key)[['event_title', 'event_time']].to_string(header=False), "\n\n") # Construct DataFrame from group with provided name.

        ans = get_return()

        if ans == False:
            return ans # return to main menu
        else:
            event_details = get_list_of_events_to_add(all_events)
            return event_details # returns [my_list, events_df]