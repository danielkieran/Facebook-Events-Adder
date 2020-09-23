# Facebook-Events-Adder
A python program that utilizes BeautifulSoup (bs4) and GoogleAPI to add facebook events held by college societies onto Google Calendar. It can list and add mutiple events at an instance following the user selection. 

Before running the code, a few prerequisites:
(1.) Create a Google developer console project to authenticate event creation for their Google Calendar. Get the credentials information in json format and rename it 'client_secret.json'.
(2.) Store credentials object in a pickle file, call it 'token.pkl'. If you need help watch the demo video or use 'get_credentials_token.ipynb'.
(3.) Store your facebook username and password as variables in 'hidden.py'.

The creation of 'client_secret.json' and 'token.pkl' is shown in this video from 0.00 - 10.47 -> https://www.youtube.com/watch?v=V589bYQ5zmM
You can also just follow the entire video to understand how events are added.

# Features
The facebook_events.csv file is a table with a row index of university names and a column header of types/cultural-aims of societies. In each unit lies the corresponding society events page in mbasic format. Mbasic makes it easier to parse the HTML code with bs4.

To convert a facebook events page to mbasic is easy!
1. Get the facebook event page of your society of interest - eg. https://www.facebook.com/tcdjapanese/events/?ref=page_internal
2. Replace 'www' to 'mbasic' - becoming https://mbasic.facebook.com/tcdjapanese/events/?ref=page_internal

That's it! 

You can add more universities/societies to the csv file with their corresponding mbasic links in place. This way you choose to keep the societies you have most keen in. Works with any society page so feel free to fill it in!
The current csv file has cultural societies from universities in the Dublin area.

# References
Indian Pythonista's video above was a great help for the project. Following his video tutorial made it much easier than reading through the docs.
https://www.youtube.com/watch?v=j1mh0or2CX8 
Adriaan Van Niekerk's channel has helped a lot when it comes to parsing with bs4 
https://www.youtube.com/channel/UC62YcVWO968SSeAM1YK_C-w
