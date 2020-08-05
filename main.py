from event_parse import *
from add_to_calender import *

print('This is a script that adds events held by East-Asian cultural societies from Facebook to Google Calender.')

                
def main():
    
    while True:
        try:
            # User Selection
            entry1 = selection()
            entry2 = selection2(entry1) # Get 2 user inputs for menu
            if entry1 == 1:
                society_urls = soc_list_by_uni(entry2)
            elif entry1 == 2:
                society_urls = soc_list_by_culture(entry2)
            else:
                return False # Breaks loop for user to quit the program
            
            society_no = get_society(society_urls) # get the society chosen from list

            if society_no > len(society_urls): # means they pressed the 'All' button
                selected_event = select_event_from_societies(society_urls) # lists all events and asks the user for events to add to calender

            else:
                link = society_urls[society_no-1] # -1 because lists count from 0
                selected_event = select_event_from_society(link) # lists the events of a single society and asks the user for events to add to calender
        except:
            ValueError
        else:
            if selected_event == False:
                print('Returning to main page.\n')
            else:
                
                if len(selected_event) > 2:                     # returned selected_event = [list_of_numbers_representing_events, events_table, society_name]
                    add_event(selected_event[0], selected_event[1], selected_event[2])
                else:                                           # or returned selected_event = [list_of_numbers_representing events, events_df]
                    s = "empty" 
                    add_events(selected_event[0], selected_event[1], s) # s is a placeholder
                
                print('Operation is complete. Check your calendar!\nWould you like to add more events? y/n')

                while True: # asks user to keep adding events or quit program
                    try:
                        text = str(input())
                    except:
                        ValueError
                    else:
                        if text == 'y':
                            print('Returning to main page')
                            break
                        if text == 'n':
                            return False
                        print('type in y or n.')

if __name__ =="__main__":
    main()  