# Imports
import json
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import maskpass

# Urls
# Log-in Webpage
login_url = 'https://mwomercs.com/do/login'
# Logged-In Player Mech Stats Webpage
profileMechStats_url = 'https://mwomercs.com/profile/stats?type=mech'
# Logged-In Player's Raw Data of Mechs
collection_data_url = 'https://mwomercs.com/mech-collection/data'
# Logged-In Player's Profile Webpage
player_url = 'https://mwomercs.com/profile'

# Current Working Directory, needed for the storing of the files being created.
cwd = os.getcwd()


# A function for gathering user credentials from a specific file or user input if the file does not exist.
def gatherlogincreds():
    # Attempt to load from creds.txt
    try:
        print("Attempting to find credentials file, creds.txt.")
        creds = Path("creds.txt").read_text()
        if creds != "":
            print("creds.txt found.")
            match_e = re.search(r"^email=(.*)$", creds, re.MULTILINE)
            playeremail = match_e.group(1)

            match_p = re.search(r"^password=(.*)$", creds, re.MULTILINE)
            playerpassword = match_p.group(1)
            return {'email': playeremail, 'password': playerpassword}

    # if creds doesn't exist prompt user as normal
    except Exception:
        print("creds.txt not found.")
        playeremail = input("Please enter your email: ")

        print("Press Left-CTRL to reveal your password.")
        playerpassword = maskpass.advpass()
        return {'email': playeremail, 'password': playerpassword}


# A function for gathering the user's in-game player name.
def gatheruser_ign(session):
    r = session.get(player_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    player_ign = soup.find('h1')
    return player_ign.text


# A helper function to find and return the list of headers from the supplied table of 'Mech Stats.
def unsorted_headerhelper(table):
    # list to store headers of the table from the HTML from profileMechStats_url.
    headers = []
    print("Gathering table headers.")
    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    return headers


# A function to fill the unsorted 'Mech Stats dataframe.
def unsorted_filldataframehelper(table, dataframe):
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(dataframe)
        dataframe.loc[length] = row


# A function to return the table found within the html text of the 'Mech Stats page.
def unsorted_htmltablehelper(htmltext):
    # Obtain information from tag <table>
    return htmltext.find('table', class_='table table-striped')


# A function to set up the unsorted 'Mech stats dataframe and create it's .csv file.
def unsorted_dataframehelper(htmltext, user):
    # Create the dataframe
    print("Creating dataframe to hold data.")
    mech_data = pd.DataFrame(columns=unsorted_headerhelper(unsorted_htmltablehelper(htmltext)))
    print("Finished setting up dataframe.")

    # Fill the dataframe
    print("Filling dataframe with the table from " + profileMechStats_url)
    unsorted_filldataframehelper(unsorted_htmltablehelper(htmltext), mech_data)
    print("Finished filling the dataframe.")

    # Convert scraped data table to .csv
    print("Converting (unsorted) dataframe to .csv format for users viewing.")
    mech_data.to_csv(cwd + os.sep + user + "_" + 'mech_data_unsorted.csv', index=False)
    print("Finished converting dataframe to .csv format.")


# A function to scrape the 'Mech Stats table on the user's profile 'Mech Stats page.
def unsortedmechstats(session, user):
    r = session.get(profileMechStats_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    unsorted_dataframehelper(soup, user)


# A function to sort the unsorted 'Mech Stats by time played.
def sortedmechstats_tp(user):
    print("Begin sorting by time played.")
    # Create a copy of the unsorted data to be sorted.
    sorted_time_played = pd.read_csv(user + "_" + 'mech_data_unsorted.csv')

    # Find all 'Mechs that have X>24 hours play time.
    print("Finding all 'Mechs with greater than 24 hours played.")
    filtered = sorted_time_played[sorted_time_played['Time Played'].str.contains("day")]

    # List to store all converted times for 'Mechs with X>24 hours play time
    times_to_add = []

    # Do calculations to show appropriate number of hours instead of "X day(s)"
    print("Converting 'days' to 24 hours.")
    for k in filtered['Time Played']:
        time = k.split(' ')
        hours_to_add = 24 * int(time[0])
        # time[1] contains "days" which is what we are removing.
        hms = time[2]
        hms = hms.split(':')
        hours = hours_to_add + int(hms[0])
        hms = str(hours) + ':' + hms[1] + ':' + hms[2]
        times_to_add.append(hms)

    # Change the Time Played strings of the 'mechs with X>24 hours time played to the calculated amount
    for x in range(len(times_to_add)):
        sorted_time_played.loc[filtered.index[x], 'Time Played'] = times_to_add[x]

    # List to store all 'mechs time played
    allHMS = []

    # Remove all ':' characters from the string and convert the resulting string to an integer
    for y in sorted_time_played['Time Played']:
        time = y.split(':')
        hms = time[0] + time[1] + time[2]
        allHMS.append(int(hms))

    # Change the Time Played Strings to the integers
    for z in (range(len(allHMS))):
        sorted_time_played.loc[sorted_time_played.index[z], 'Time Played'] = allHMS[z]

    # Sort the Time Played column by the integer values in descending order
    sorted_time_played = sorted_time_played.sort_values(['Time Played'], axis=0, ascending=False)

    # List to store our conversion from integer back to string with the appropriate format
    mutated_times = []

    # Convert integers to string in the correct format
    # I got lazy and tired. Went with ugly brute-forced code to reformat the time back to H:M:S
    for a in sorted_time_played['Time Played']:
        mtime = str(a)
        if len(mtime) == 1:
            mtime = "00:00:0" + mtime
        elif len(mtime) == 2:
            mtime = "00:00:" + mtime
        elif len(mtime) == 3:
            mtime = "00:0" + mtime[0] + ':' + mtime[1] + mtime[2]
        elif len(mtime) == 4:
            mtime = "00:" + mtime[0] + mtime[1] + ':' + mtime[2] + mtime[3]
        elif len(mtime) == 5:
            mtime = "0" + mtime[0] + ':' + mtime[1] + mtime[2] + ':' + mtime[3] + mtime[4]
        elif len(mtime) == 6:
            mtime = mtime[0] + mtime[1] + ':' + mtime[2] + mtime[3] + ':' + mtime[4] + mtime[5]
        elif len(mtime) > 6:
            seconds = mtime[-2] + mtime[-1]
            minutes = mtime[-4:-2]
            hours = mtime[:-4]
            mtime = hours + ':' + minutes + ':' + seconds
        mutated_times.append(mtime)

    # Change the Time Played Integers to the Strings we just built.
    for b in range(len(mutated_times)):
        sorted_time_played.loc[sorted_time_played.index[b], 'Time Played'] = mutated_times[b]

    print("Finished sorting by time played.")

    # Remove column that offers no real beneficial information
    print("Removing 'XP Earned' entry from dataframe.")
    sorted_time_played.drop(columns=['XP Earned'], inplace=True)

    # As the mech's were already previously sorted, and we have done no rearranging, simply output to .csv
    print("Converting (sorted) time played dataframe to .csv format for users viewing.")
    sorted_time_played.to_csv(cwd + os.sep + user + "_" + 'mech_data_sorted_TP.csv', index=False)


# A function for sorting the unsorted 'Mech stats by matches played.
def sortedmechstats_mp(user_ign):
    print("Begin sorting by matches played.")
    # Create dataframe of mech's sorted by matches played.
    sorted_matches_played = pd.read_csv(user_ign + "_" + 'mech_data_unsorted.csv')

    # Removed columns that offer no real beneficial information
    print("Removing 'Time Played' and 'XP Earned' entries from dataframe.")
    sorted_matches_played.drop(columns=['Time Played', 'XP Earned'], inplace=True)

    # Sort by the values stored in the Matches Played column.
    sorted_matches_played.sort_values(["Matches Played"], axis=0, ascending=False, inplace=True)

    print("Converting (sorted) matches played dataframe to .csv format for users viewing.")
    sorted_matches_played.to_csv(cwd + os.sep + user_ign + "_" + 'mech_data_sorted_MP.csv', index=False)


# A function for gathering information about the user's owned 'Mechs.
def playerownedmechstats(session, user_ign):
    print("Begin gathering all player owned 'Mechs.")
    # Access the JSON that contains all the players 'Mech variant information at collection_data_url.
    response = session.get(collection_data_url)

    # A dictionary to contain 'Mech IDs and their skill nodes.
    dict_mechIDs = {}

    # Old code for opening a JSON file stored on the machine. Keeping this here as a reminder for the
    # offline version.
    # with open(cwd + os.sep + playername + "_" + 'mech_collection.json') as f:

    # Convert the JSON text into a python recognizable data format (I.E., Dict)
    print("Loading players 'Mech Collectin JSON.")
    data = json.loads(response.text)
    collection = data['collection']
    print("Parsing the JSON and gathering all owned 'Mechs Variants and associated mechIDs.")
    for collection_data in collection:
        variants_data = collection_data['variants']
        for specific_variant in variants_data:
            if variants_data[specific_variant]['owned'] is True:
                # Store the list of mechIDs for a specific variant
                mechIDs = variants_data[specific_variant]['mech_ids']

                # Create an entry in the dictionary of 'Mechs to hold the list of mechIDs
                dict_mechIDs[variants_data[specific_variant]['display_name']] = mechIDs
    print("Finished parsing and gathering all owned 'Mech Variants and their associated mechIDs.")

    # A list to contain tuples (Mech Variant, Name player gave it, # skill points assigned).
    list_mech_chass_name_SP = []

    print("Gathering owned 'Mech user defined name, and number of equipped skill points from "
          "https://mwomercs.com/mech-collection/data/stats?mid[]=<Individual 'Mechs MechID>")
    print("Gathering additional 'Mech information (Tonnage, Faction, Class) from mechDB API.")
    print("This may take a while, so please be patient.")

    # also grab chassis data from the MechDB API - we have to lie about the user agent or we'll get blocked
    url = "https://mwo.nav-alpha.com/api/mechs/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer Z8YvyDlFEubyCYGbqtkaGMrfmAKuJwHOXaae3hxqbml1ytmww2qpeiKRgp97efG1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
    }
    mechdb = requests.request("POST", url, headers=headers)
    if mechdb.status_code == 200:
        mechdata = mechdb.json()
    else:
        print("Unable to load extra data from MechDB. Continuing.")
        mechdata = ""

    for mech, mechID in dict_mechIDs.items():
        for i in mechID:
            # We now have access to each individual 'mechs mechID.

            # ------------- Individual mech's skill point scraper ---------------
            # Create url of the specific 'Mech we want the information of
            spec_mech_url = collection_data_url + "/stats?mid[]=" + i
            response_spec_mech = session.get(spec_mech_url)
            dict_spec_mech = json.loads(response_spec_mech.text)

            for mech_chassis in dict_spec_mech['mechs']:
                mechlab_mechname = mech_chassis['name']
                spec_mech_skills = mech_chassis['skills']['NumEquippedSkillNodes']
                if mechdata != "":
                    for mechinfo in mechdata["data"]:
                        if mechinfo['display_name'] == mech:
                            mech_tonnage = mechinfo['tonnage']
                            mech_faction = mechinfo['faction']
                            mech_class = mechinfo['class']
                else:
                    mech_tonnage = "--"
                    mech_faction = "--"
                    mech_class = "--"
                # Using regex to remove special variant tags from mechs to be used as a "base" 'Mech for easier
                # crafting of look-up tables.
                list_mech_chass_name_SP.append((re.sub("[(].*?[)]", "", mech), mech, mechlab_mechname, mech_tonnage,
                                                mech_faction, mech_class, spec_mech_skills))

    # Convert list of tuples (mech variant, name, equipped skill points) into a dataframe.
    print("Converting list of tuples (Base, Variant, User Defined Name, Tonnage, Faction, Weight Class, Skill "
          "Points) to data frame.")
    df_list_mech_name_sp = pd.DataFrame(list_mech_chass_name_SP,
                                        columns=['Base', 'Variant', 'Name', 'Tonnage', 'Faction', 'Class',
                                                 'Skill Points'])

    # Convert dataframe to csv file.
    print("Converting (Base, Variant, User Defined Name, Tonnage, Faction, Weight Class, Skill Points) "
          "dataframe to .csv format for users viewing.")
    df_list_mech_name_sp.to_csv(cwd + os.sep + user_ign + "_" + 'owned_mechs_SP.csv', index=False)


def main():
    # Player's Credentials to be used on log-in
    payload = gatherlogincreds()

    try:
        # Open a session
        with requests.session() as s:
            print("Attempting to log in to mwomercs.com with the supplied credentials and gather the relevant "
                  "information. One moment please. :)")
            print("Please do not touch your keyboard while the program is working. Unless you want this prompt to "
                  "disappear into the aether upon completion.")
            # Send log in credentials to the log in url.
            s.post(login_url, data=payload)
            print("Log in successful.")

            # Get player profile name
            print("Gathering player's in-game name to create customized save files.")
            playername = gatheruser_ign(s)
            print("Finished gathering users in-game name.")

            print("Gathering information on players 'Mech stats on " + profileMechStats_url)
            print("This may take a minute, so please be patient.")
            unsortedmechstats(s, playername)
            print("Finished gathering information on " + profileMechStats_url)

            # ----------- Sort By Time Played -----------
            print("Sorting 'Mechs by Time Played.")
            sortedmechstats_tp(playername)
            print("Finished sorting by Time Played.")

            # ---------- Sort by Matches Played ----------
            print("Sorting 'Mechs by matches played.")
            sortedmechstats_mp(playername)
            print("Finished sorting by Matches Played.")

            # ---------- Player Profile Scraper ----------
            print("Gathering information about player's owned 'Mechs "
                  "(Variant, mechID) from players unique JSON located at "
                  "https://mwomercs.com/mech-collection/data")
            playerownedmechstats(s, playername)
            print("Finished gathering information about player's owned 'Mechs.")

            print("Your spreadsheets have been created! :D")
    except AttributeError:
        print("Incorrect credentials supplied. The program failed to log in to mwomercs.com and find the appropriate "
              "tables.")

    input("Press 'Enter' to continue or simply close this script.")

if __name__ == "__main__":
    main()
