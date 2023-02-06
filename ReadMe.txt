MWOMechScraper

READ ME!


This tool was developed by Zach Gherman to assist players to more easily view the 'Mechs they have played the most and
have the most time piloting for the online video game MechWarriorOnline. This tool simply opens a session with the
mwomercs.com webpage and navigates to the players profile mechstat page and scrapes data from the table available. It
then compiles the data and transforms it into easy-to-read .csv (comma separated value) files {mech_data_unsorted.csv,
mech_data_sorted_TP.csv, and mech_data_sorted_MP.csv}. The sorted .csv files list 'Mechs in descending order for quick
and easy comprehension of what 'Mechs that player plays the most. 
MWOMechScraper now also spits out another .csv which contains a list of all 'Mechs you currently own!
No longer are the days of asking players if they own a specific 'Mech, simply point them to this tool and have them
send you their owned_mechs.csv. Coalesce multiple players owned_mechs.csvs to quickly and efficiently build your teams
drop-deck based on what people already own!

HOW TO USE:
You will need to download and install the latest version of Python.
    Steps to install Python:
        1) Open your web-browser and navigate to https://www.python.org/
        2) Navigate to Downloads and install the latest appropriate version based on the machine you are running on.
        3) Double click the downloaded file and install for all users. Please ensure that Python is added to your path.
           (This will ensure that you can use Python from any location in your file system)
        4) Once installation is completed, select 'Disable path length limit' so that you can use more than 260 characters
           in a file path.
        5) Press the 'Close' button to end the installation.


Once you have installed Python simply scroll up, find the big green '<>Code' button, click on it,
select 'Download ZIP', and extract the contents of the .zip file to where ever you like.

Next, you will need the libraries associated with the script.
Open the Command Prompt and type the following commands,
pip install BeautifulSoup4
pip install requests
pip install pandas

BeautifulSoup4 allows us to pull data from HTML and XML files and parse it.
requests allows us to make HTTP requests, or in our case, log in to mwomercs.com.
pandas allows us to analyze and format the data scraped from mwomercs.com.

Now navigate to where you extracted the contents to and double-click main.py to run the script.

The script will prompt you for the email and password that you use for mwomercs.com. Type in your email and password
when prompted and now wait until your personal .csv files have been created!

The included .csv files are example outputs of what to expect and are the direct product of scraping my personal account.
You may delete all included .csv files as they will be generated for you anyway when the program is run.