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
Load the program up in your favorite Python interpreter.
Import the libraries.
Navigate over to the creds.py and input your email and password associated with your account within the appropriate
fields then hit 'Run'. After a few moments, your personal .csv files will be generated for your viewing pleasure and
personal use.

The included .csv files are example outputs of what to expect and are the direct product of scraping my personal account.
Don't worry about deleting the files as when the program is run successfully, the contents will be overwritten with
your account's information.