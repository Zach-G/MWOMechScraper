# MWOMechScraper
## README
This tool was developed by Zach Gherman to assist players to more easily view the 'Mechs they have played the most and have the most time piloting for the online video game [MechWarrior Online](https://mwomercs.com).

This tool simply opens a session with the mwomercs.com webpage and navigates to the players profile mechstat page and scrapes data from the table available. It then compiles the data and transforms it into easy-to-read .csv (comma separated value) files:

- mech_data_unsorted.csv

- mech_data_sorted_TP.csv

- and mech_data_sorted_MP.csv

The sorted .csv files list 'Mechs in descending order for quick and easy comprehension of what 'Mechs that player plays the most.

MWOMechScraper now also spits out another .csv (owned_mechs.csv) which contains a list of all 'Mechs you currently own in the format of [Base Mech, Variant, Name, Tonnage, Faction, Weight Class, Number of Equipped Skill Points]. The Base 'Mech details the base variant of special chassis variants (E.G., Spider-5D(P) variant's base variant is the Spider-5D). The Variant denotes the actual variant of the 'Mech (E.G., SDR-5D(P)). The Name is the name that the player has given the 'Mech in the Mechlab. The Tonnage is the amount of Tons the 'Mech is. The Faction details which faction the 'Mech is (I.E., Clan or Inner Sphere). The Weight Class details the size of the 'Mech (Light, Medium, Heavy, Assault). The Number of Equipped Skill Points shows how skilled out a 'Mech is.

No longer are the days of asking players if they own a specific 'Mech, simply point them to this tool and have them send you their owned_mechs.csv. Coalesce multiple players owned_mechs.cvs to quickly and efficiently build your teams drop-deck based on what people already own! Use the "Team 'Mech-list" button to quickly see who owns what mechs to find substitute players in a moment's notice or to save your players from having to spend C-Bills / MC!

---

## IMPORTANT
This tool needs to log into your MWO Profile page to access your mech data. Your log-in credentials are not stored or visible to anyone. However, this tool makes an attempt to hide your credentials on your personal screen by masking your password input with asterisks (*).
Please, feel free to review the code yourself and ensure that the only addresses used are the MWOMercs login, profile pages and your personal accounts JSONs.

## HOW TO USE
To run this tool simply download and run the executable located in https://github.com/Zach-G/MWOMechScraper/releases. Just scroll down to the bottom of the page, click 'MWOMechScraper.exe' and the download will begin. The tool will then be residing in your 'downloads' folder. Please note that MWOMechScraper will create the csv files in whatever folder it is contained in. I.E, If you run the tool from your downloads folder, it will generate the csv files in your downloads folder.

Again, the tool will prompt you for the email and password that you use for [MWO](https://mwomercs.com/) if you select the buttons labeled "Online". Type in your email and password into the terminal when prompted and now wait until your personal .CSV files have been created!

## Offline Version
The "HTML File" buttons allow for the user to choose HTML files containing the information they wish to scrape. To get the 'Mech tonnage, we still require an internet connection to make a request to the [MechDB API](https://mwo.nav-alpha.com/api/mechs/) to then store a local version of the database on the user's machine. If a user does not wish to press the "Update Offline MechDB" button, the values for tonnage associated with their 'Mechs in the .CSV Files will be "--". For the "HTML File Stat Scraper" button to work, the player must first log into [MWOMercs](https://mwomercs.com/) and navigate to their profiles 'Mech Stats page (Profile->Stats->Mech Stats) then save a copy of the HTML by right-clicking on the website page, selecting "Save Page As...", and saving the page with the ".html" extension. For the "HTML File Mech Scraper" button to work, the user must first log into [MWOMercs](https://mwomercs.com/) and navigate to their Profile. Next they must mouse-over every 'Mech they own long enough to see their number of skill nodes equipped for the owned 'Mechs. This is because information pertaining to the 'Mechs on the webpage is live-loaded when the player mouses over the icon of their owned 'Mech. Once all owned 'Mechs have been moused over the user may again right-click the webpage and select "Save Page As..." with the .html file extension. The tool will prompt the user for their In-Game name via a message box to properly name the .CSV file when it is created.

## Running the source code yourself
For those who are skeptical about running the executable and would prefer to run the source code instead, you will need 
to download and install Python, add Python to your Path environment, and then download all the libraries associated with 
the tool. Below I have listed the steps to install Python, ensure that Python is in your Path environment, and the command 
prompt lines to install the required libraries.

You will need to download and install the latest version of Python.

### Installing Python
1. Open your web-browser and navigate to https://www.python.org/
2. Follow the instructions listed for your particular system on https://wiki.python.org/moin/BeginnersGuide/Download


### Next, you need to ensure that your PC understands where Python is located on your PC
Here are the steps to set up your PATH environment to include Python, so you can run the script:

1. Left-click the Windows button on your taskbar then right-click "This PC" and select "Properties".
2. Look for "Advanced system settings" on the window that pops up and left-click it.
3. Left-click on the "Environment Variables" button on the bottom right.
4. In the "System variables" section, select the "Path" variable and click "Edit". The next screen shows all directories that are currently associated with the PATH variable.
5. Left-click "New" and enter Python's install directory (The path to where Python was installed).

**NOTE**: Usually you can find the installed binary in this path location if you did not select a path, like `%APPDATA%\Local\Programs\Python`

### Get the library dependencies
Next, you will need the libraries associated with the script.
Open the Command Prompt and type the following commands:

```sh
python -m pip install BeautifulSoup4
python -m pip install requests
python -m pip install pandas
python -m pip install regex
python -m pip install tkinter
python -m pip install glob
```

#### What do these dependencies do?
[BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/) allows us to pull data from HTML and XML files and parse it.
[requests](https://pypi.org/project/requests/) allows us to make HTTP requests, or in our case, log in to mwomercs.com.
[pandas](https://pandas.pydata.org/) allows us to analyze and format the data scraped from mwomercs.com.
[regex](https://docs.python.org/3/howto/regex.html) is used for regular expressions.
[tkinter](https://docs.python.org/3/library/tkinter.html) is used to create the GUI.
[glob](https://docs.python.org/3/library/glob.html) is used to find all pathnames matching a specified pattern.

Once you have installed Python and all the required libraries simply scroll up, find the big green '<>Code' button, 
click on it, select 'Download ZIP', and extract the contents of the .zip file to where ever you like.

Now navigate to where you extracted the contents to and double-click main.py to run the script.

## Thanks / Contributors

Thank you Tarogato for being a guinea pig and helping me test this tool via attempting to follow the README.
- Including Python to Path environment
- Updating command prompt pip commands
- Updating ReadMe
- Pushing me to hide the password
- Pointing out redundancies and suggesting additions to owned_mechs.csv

A big thank you to Woodrick for asking that this tool be developed.
- Making suggestions for the README

Thank you Grinny for cleaning up my horrible README and the root directory.
- Adding the gitignore
- Adding the requirements.txt
- (grinny was here, Hail Cargonia)

Thank you Bak3y for providing a way for users to use a creds.txt so that users do not need to enter their credentials every time and for fixing an os path bug for Linux machines.
- Adding mechDB API to gather Tonnage, Faction, and Weight Class.

Thank you K2B for creating and maintaining mechDB! This tool would be incomplete without your API!

Thank you CougChaos for helping find bugs within the HTML scraper.

Thank you YuriPro for noticing that the Viper Scaleshot was being improperly recognized by the tool.

A big thank you to the following players who sent me their _owned_mechs.csv's so that the example Team_List_Of_Mechs.csv could be populated with real player information!
- U94, abobra, Sunwraith, Chosen by Heaven, NimhTG, VulkanNo1, SirEpicPwner, and Tarogato,
- and the pilot who wished to remain nameless, Generic Player 1.