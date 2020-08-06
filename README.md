# Facebook-Events-Adder
A python program that utilizes BeautifulSoup (bs4) and GoogleAPI to add facebook events held by college societies onto Google Calender. It can list and add mutiple events at an instance following the user selection. 

Before running the code, a few prerequisites:
(1.) Create a Google developer console project to authenticate the user to apply changes for their Google Calender. Get the creden tials information in json format and rename it 'client_secret.json'.
(2.) Get credentials object with Googleapiclient and store it in a pickle file called 'token.pkl'. 
(3.) Insert your facebook payload in 'hidden.py'.

For (1.), follow this video -> https://www.youtube.com/watch?v=j1mh0or2CX8 from 1:33 to 5:04. The Google developer console website has changed its interface a slight bit but the steps are the same. Instead of entering 'Other', select 'Web application' in the 4:09 part of the video.

For (2.), you can continue to watch the video until 11:24 for verbal explanation. Open jupyter notebook and run get_credentials_token.ipynb to create your 'token.pkl' which will give permission for main.py to add events to your calender.

For (3.), insert your facebook email in the double apostrophes of 'username' and your password in the double apostrophes of 'password'. Facebook requires your account details for parsing its HTML code.

Once the 3 steps are completed, run main.py in terminal and freely add your events!

# Features
The facebook_events.csv file is a table with a row index of university names and a column header of types/cultural-aims of societies. In each unit lies the corresponding society events page in mbasic format. Mbasic makes it easier to parse the HTML code with bs4.

To convert a facebook events page to mbasic is easy!
1. Get the facebook event page of your society of interest - eg. https://www.facebook.com/tcdjapanese/events/?ref=page_internal
2. Replace 'www' to 'mbasic' - becoming https://mbasic.facebook.com/tcdjapanese/events/?ref=page_internal

That's it! 

You can add more universities/societies to the csv file with their corresponding mbasic links in place. This way you choose to keep the societies you have most keen in. Works with any society page so feel free to fill it in!
The current csv file has cultural societies from universities in the Dublin area.

# References
Indian Pythonista's video above was a great help for the project. Following his video tutorial made it much easier than reading through the docs. https://www.youtube.com/channel/UCkUq-s6z57uJFUFBvZIVTyg
Adriaan Van Niekerk's channel has helped a lot when it comes to parsing with bs4 https://www.youtube.com/channel/UC62YcVWO968SSeAM1YK_C-w
