MWOMechScraper

READ ME!

This tool was developed by Zach Gherman to assist players to more easily view the 'Mechs they have played the most and
have the most time piloting for the online video game MechWarriorOnline. This tool simply opens a session with the
mwomercs.com webpage and navigates to the players profile mechstat page and scrapes data from the table available. It
then compiles the data and transforms it into easy-to-read .csv (comma separated value) files {mech_data_unsorted.csv,
mech_data_sorted_TP.csv, and mech_data_sorted_MP.csv}. The sorted .csv files list 'Mechs in descending order for quick
and easy comprehension of what 'Mechs that player plays the most. 
MWOMechScraper now also spits out another .csv which contains a list of all 'Mechs you currently own as well as a list
of all your mech's wih the names you gave them and how many skill points they have equipped!
No longer are the days of asking players if they own a specific 'Mech, simply point them to this tool and have them
send you their owned_mechs.csv or owned_mechs_SP.csv. Coalesce multiple players owned_mechs.csvs to quickly and
efficiently build your teams drop-deck based on what people already own!
________________________________________________________________________________________________________________________

IMPORTANT:
This tool needs to log into your MWO Profile page to access your mech data. Your log-in credentials are not stored or
visible to anyone. However, this tool makes no attempt to hide your credentials on your personal screen.
Please, feel free to review the code yourself and ensure that the only addresses used are the MWOMercs login and
profile pages.

________________________________________________________________________________________________________________________

HOW TO USE:

There are two methods of running this tool. Method 1 entails installing Python on your machine and running the script
directly. Method 2 is simply running the executable!

************************************************************************************************************************
Method 1,
You will need to download and install the latest version of Python.
    Steps to install Python:
        1) Open your web-browser and navigate to https://www.python.org/
        2) Navigate to Downloads and install the latest appropriate version based on the machine you are running on.
        3) Double click the downloaded file and install for all users. Please ensure that Python is added to your path.
           (This will ensure that you can use Python from any location in your file system)
        4) Once installation is completed, select 'Disable path length limit' so that you can use more than 260 characters
           in a file path.
        5) Press the 'Close' button to end the installation.

Next, you need to ensure that your PC understands where Python is located on your PC.
    Steps to set up your PATH environment to include Python, so you can run the script:
        1) Left-click the Windows button on your taskbar then right-click "This PC" and select "Properties".
        2) Look for "Advanced system settings" on the window that pops up and left-click it.
        3) Left-click on the "Environment Variables" button on the bottom right.
        4) In the "System variables" section, select the "Path" variable and click "Edit". The next screen shows all
           directories that are currently associated with the PATH variable.
        5) Left-click "New" and enter Python's install directory (The C: path to where Python was installed).
           NOTE: Usually you can find the installed binary in this path location,
                 C:\Users\AppData\Local\Programs\Python


Once you have installed Python simply scroll up, find the big green '<>Code' button, click on it,
select 'Download ZIP', and extract the contents of the .zip file to where ever you like.

Next, you will need the libraries associated with the script.
Open the Command Prompt and type the following commands,
python -m pip install BeautifulSoup4
python -m pip install requests
python -m pip install pandas

BeautifulSoup4 allows us to pull data from HTML and XML files and parse it.
requests allows us to make HTTP requests, or in our case, log in to mwomercs.com.
pandas allows us to analyze and format the data scraped from mwomercs.com.

Now navigate to where you extracted the contents to and double-click main.py to run the script.
************************************************************************************************************************

************************************************************************************************************************
Method 2,
Head over to the latest release ( https://github.com/Zach-G/MWOMechScraper/releases/tag/v1.0.3 ) and scroll down to the
bottom of the page. Click 'main.exe' and a download will begin. Once it is finished downloading you can simply run the
executable! Note that the .csv files the tool creates will be created in the same folder that the executable is run
in. So if you don't cut/paste the executable to a folder then the .csv's will be created in your downloads folder.
************************************************************************************************************************

No matter what method you choose to employ, the script will prompt you for the email and password that you use for
mwomercs.com. Type in your email and password when prompted and now wait until your personal .csv files have
been created!

The included .csv files are example outputs of what to expect and are the direct product of scraping my personal account.
You may delete all included .csv files as they will be generated for you anyway when the program is run. If you choose
not to delete them they will be overwritten with your 'Mech data.

If the tool is run via the .exe, the output .csv files will be created in whatever directory the .exe was run in
(this will be the 'dist' folder if you didn't move the executable).

************************************************************************************************************************
I will work on an "offline" version in which players can send their HTML's to someone to have the .CSVs created.
This however will require more effort from the users as they will need to ensure that they load all the data on their
profile page by hovering their mouse over each individual 'Mech they own before exporting the HTML. This is because the
data is grabbed from the website using GET requests to the player's unique JSON once the player hovers over the owned
'Mech. Without the GET requests, the HTML is incomplete and grabbing the Mech names and number of skill points equipped 
to each individual 'Mech is impossible.

________________________________________________________________________________________________________________________
Thank you Tarogato for being a guinea pig and helping me test this tool via attempting to follow the README.
- Including Python to Path environment
- Updating command prompt pip commands
- Updating ReadMe

A big thank you to Woodrick for asking that this tool be developed.
