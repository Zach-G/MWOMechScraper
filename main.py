# Imports
import json
import os
import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Urls
# Log-in Webpage
login_url = 'https://mwomercs.com/do/login'
# Logged-In Player Mech Stats Webpage
profileMechStats_url = 'https://mwomercs.com/profile/stats?type=mech'
# Logged-In Player's Raw Data of Mechs
collection_data_url = 'https://mwomercs.com/mech-collection/data'
# Logged-In Player's Profile Webpage
player_url = 'https://mwomercs.com/profile'
# MechDB API
mech_db_url = "https://mwo.nav-alpha.com/api/mechs/"

# Current Working Directory, needed for the storing of the files being created.
cwd = os.getcwd()


# ------------------------------------- ONLINE SECTION -------------------------------------

# A function for gathering user credentials from a specific file or user input if the file does not exist.
def gather_login_creds(output_box):
    # Attempt to load from creds.txt
    try:
        update_output(output_box, "Attempting to find credentials file, creds.txt.\n")

        creds = Path("creds.txt").read_text()
        if creds != "":
            update_output(output_box, "creds.txt found.\n")

            match_e = re.search(r"^email=(.*)$", creds, re.MULTILINE)
            player_email = match_e.group(1)

            match_p = re.search(r"^password=(.*)$", creds, re.MULTILINE)
            player_password = match_p.group(1)
            return {'email': player_email, 'password': player_password}
    # if creds.txt doesn't exist prompt user as normal
    except Exception:
        player_email = ""
        player_password = ""

        update_output(output_box, "creds.txt not found.\n")

        # create a dialog box for getting the user's email and password
        dialog = tk.Toplevel()
        dialog.title("Login")
        tk.Label(dialog, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        email_entry = tk.Entry(dialog)
        email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Center the dialog box on the screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2
        y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2
        dialog.geometry("+%d+%d" % (x, y))

        # Nested function for the submit button to ensure the user typed in something to both fields {email, password}.
        def submit():
            nonlocal player_email
            nonlocal player_password
            player_email = email_entry.get()
            player_password = password_entry.get()
            if not player_email or not player_password:
                tk.messagebox.showerror("Error", "Please enter both email and password.")
                return
            dialog.destroy()

        # Create submit button.
        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        dialog.transient(output_box.master)
        dialog.grab_set()
        output_box.master.wait_window(dialog)

        return {'email': player_email, 'password': player_password}


# A function for gathering the user's in-game player name.
def gather_user_ign(session, output_box):
    update_output(output_box, "Attempting to gather user's in-game name to create customized save files.\n")

    r = session.get(player_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    player_ign = soup.find('h1')

    update_output(output_box, "Finished gathering users in-game name.\n")
    return player_ign.text


# A function to scrape the 'Mech Stats table on the user's profile 'Mech Stats page.
def unsorted_mech_stats(session, user, output_box):
    update_output(output_box, "Attempting to gather information on players 'Mech stats at " +
                  profileMechStats_url + "\n")
    update_output(output_box, "This may take a minute, so please be patient.\n")

    r = session.get(profileMechStats_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    unsorted_data_frame_helper(soup, user, output_box)


# A function to return the JSON from mechDB if a successful request was made.
def mech_db_helper(output_box):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer Z8YvyDlFEubyCYGbqtkaGMrfmAKuJwHOXaae3hxqbml1ytmww2qpeiKRgp97efG1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
    }
    mech_db = requests.request("POST", mech_db_url, headers=headers)
    if mech_db.status_code == 200:
        update_output(output_box, "Loading additional data from MechDB.")
        return mech_db.json()
    else:
        update_output(output_box, "Unable to load extra data from MechDB. Continuing.")
        return ""


# A function for gathering information about the user's owned 'Mechs.
def player_owned_mechs_info(session, user_ign, output_box):
    update_output(output_box, "Attempting to gather information about player's owned 'Mechs "
                  "(Variant, mechID) from players unique JSON located at https://mwomercs.com/mech-collection/data\n")
    # Access the JSON that contains all the players 'Mech variant information at collection_data_url.
    update_output(output_box, "Opening session with " + collection_data_url + "\n")
    response = session.get(collection_data_url)

    # A dictionary to contain 'Mech IDs and their skill nodes.
    dict_mech_ids = {}

    # Convert the JSON text into a python recognizable data format (I.E., Dict)
    update_output(output_box, "Loading players 'Mech Collection JSON.\n")
    data = json.loads(response.text)
    collection = data['collection']
    update_output(output_box, "Parsing the JSON and gathering all owned 'Mechs Variants and associated mechIDs.\n")
    for collection_data in collection:
        variants_data = collection_data['variants']
        for specific_variant in variants_data:
            if variants_data[specific_variant]['owned'] is True:
                # Store the list of mechIDs for a specific variant
                mech_ids = variants_data[specific_variant]['mech_ids']
                # Create an entry in the dictionary of 'Mechs to hold the list of mechIDs
                dict_mech_ids[variants_data[specific_variant]['display_name']] = mech_ids
    update_output(output_box, "Finished parsing and gathering all owned 'Mech Variants and their associated mechIDs.\n")

    # A list to contain tuples (Mech Variant, Name player gave it, # skill points assigned).
    list_mech_chass_name_sp = []

    update_output(output_box, "Gathering owned 'Mech user defined name, and number of equipped skill points from "
                  "https://mwomercs.com/mech-collection/data/stats?mid[]=<Individual 'Mechs MechID>\n")
    update_output(output_box, "Gathering additional 'Mech information (Tonnage, Faction, Class) from mechDB API.\n")
    update_output(output_box, "This may take a while, so please be patient.\n")

    # also grab chassis data from the MechDB API - we have to lie about the user agent; or we'll get blocked
    mech_data = mech_db_helper(output_box)

    for mech, mechID in dict_mech_ids.items():
        for i in mechID:
            # We now have access to each individual 'mechs mechID.

            # ------------- Individual mech's skill point scraper ---------------
            # Create url of the specific 'Mech we want the information of
            spec_mech_url = collection_data_url + "/stats?mid[]=" + i
            response_spec_mech = session.get(spec_mech_url)
            dict_spec_mech = json.loads(response_spec_mech.text)

            for mech_chassis in dict_spec_mech['mechs']:
                mechlab_mech_name = mech_chassis['name']
                spec_mech_skills = mech_chassis['skills']['NumEquippedSkillNodes']
                if mech_data != "":
                    for mech_info in mech_data["data"]:
                        if mech_info['display_name'] == mech:
                            mech_tonnage = mech_info['tonnage']
                            mech_faction = mech_info['faction']
                            mech_class = mech_info['class']
                else:
                    mech_tonnage = "--"
                    mech_faction = "--"
                    mech_class = "--"
                # Using regex to remove special variant tags from mechs to be used as a "base" 'Mech for easier
                # crafting of look-up tables.
                list_mech_chass_name_sp.append((re.sub("[(].*?[)]", "", mech), mech, mechlab_mech_name, mech_tonnage,
                                                mech_faction, mech_class, spec_mech_skills))
    update_output(output_box, "Finished gathering information about player's owned 'Mechs.\n")

    # Convert list of tuples (mech base variant, actual variant, name, tonnage, faction, weight class, equipped skill
    # points) into a dataframe.
    update_output(output_box, "Converting list of tuples (Base, Variant, User Defined Name, Tonnage, Faction, "
                              "Weight Class, Skill Points) to dataframe.\n")
    df_list_mech_name_sp = pd.DataFrame(list_mech_chass_name_sp,
                                        columns=['Base', 'Variant', 'Name', 'Tonnage', 'Faction', 'Class',
                                                 'Skill Points'])

    # Convert dataframe to csv file.
    update_output(output_box, "Converting (Base, Variant, User Defined Name, Tonnage, Faction, Weight Class, "
                              "Skill Points) dataframe to .csv format for users viewing.\n")
    df_list_mech_name_sp.to_csv(cwd + os.sep + user_ign + "_" + 'owned_mechs_SP.csv', index=False)


def run_online_stat_scraper(output_box):
    # Code for online stat scraper
    update_output(output_box, "Running Online Stat Scraper")
    # Player's Credentials to be used on log-in
    payload = gather_login_creds(output_box)
    try:
        # Check if the site is available
        if not is_site_available(login_url):
            raise Exception("Unable to connect to the site. Please check your internet connection and try again.")

        # Open a session
        with requests.session() as s:
            update_output(output_box, "Attempting to log in to mwomercs.com with the supplied credentials and gather "
                                      "the relevant information. One moment please. :)\n")
            # Send log in credentials to the log in url.
            response = s.post(login_url, data=payload)
            if check_log_in_creds(response, output_box) is False:
                return
            if response.status_code == 200:
                update_output(output_box, "Log in successful.\n")

                # Get player profile name
                player_name = gather_user_ign(s, output_box)

                # Get unsorted table of 'Mech stats and create a .csv of it.
                unsorted_mech_stats(s, player_name, output_box)

                # ---------- Sort By Time Played ----------
                sorted_mech_stats_tp(player_name, output_box)

                # ---------- Sort by Matches Played ----------
                sorted_mech_stats_mp(player_name, output_box)

                update_output(output_box, "Your spreadsheets have been created! :D\n")
            else:
                update_output(output_box, "Failed to log in with status code: {response.status_code}\n")
    except Exception as e:
        template = "An exception of type {0} occurred.\n"
        message = template.format(type(e).__name__)
        update_output(output_box, message)


def run_online_mech_scraper(output_box):
    # Code for online stat scraper
    update_output(output_box, "Running Online Stat Scraper\n")
    # Player's Credentials to be used on log-in
    payload = gather_login_creds(output_box)
    try:
        # Check if the site is available
        if not is_site_available(login_url):
            raise Exception("Unable to connect to the site. Please check your internet connection and try again.\n")

        # Open a session
        with requests.session() as s:
            update_output(output_box, "Attempting to log in to mwomercs.com with the supplied credentials and gather "
                                      "the relevant information. One moment please. :)\n")
            # Send log in credentials to the log in url.
            response = s.post(login_url, data=payload)

            if check_log_in_creds(response, output_box) is False:
                return
            if response.status_code == 200:
                update_output(output_box, "Log in successful.\n")

                # Get player profile name
                player_name = gather_user_ign(s, output_box)

                # ---------- Players Owned 'Mechs ----------
                player_owned_mechs_info(s, player_name, output_box)

                update_output(output_box, "Your spreadsheets have been created! :D\n")
            else:
                update_output(output_box, "Failed to log in with status code: {response.status_code}\n")
    except Exception as e:
        template = "An exception of type {0} occurred.\n"
        message = template.format(type(e).__name__)
        update_output(output_box, message)
# ------------------------------------------------------------------------------------------


# ------------------------------------- OFFLINE SECTION ------------------------------------

# A function to set up the unsorted 'Mech stats dataframe and create it's .csv file.
def unsorted_data_frame_helper(htmltext, user, output_box):
    # Create the dataframe
    update_output(output_box, "Creating dataframe to hold data.\n")
    mech_data = pd.DataFrame(columns=unsorted_header_helper(unsorted_html_table_helper(htmltext, output_box),
                                                            output_box))
    if mech_data.columns.empty:
        return False
    update_output(output_box, "Finished setting up dataframe.\n")

    # Fill the dataframe
    update_output(output_box, "Filling dataframe with the table from " + profileMechStats_url + "\n")

    unsorted_fill_data_frame_helper(unsorted_html_table_helper(htmltext, output_box), mech_data, output_box)
    update_output(output_box, "Finished filling the dataframe.\n")

    # Convert scraped data table to .csv
    update_output(output_box, "Converting (unsorted) dataframe to .csv format for users viewing.\n")
    mech_data.to_csv(cwd + os.sep + user + "_" + 'mech_data_unsorted.csv', index=False)
    update_output(output_box, "Finished converting dataframe to .csv format.\n")


# A helper function to find and return the list of headers from the supplied table of 'Mech Stats.
def unsorted_header_helper(table, output_box):
    # list to store headers of the table from the HTML from profileMechStats_url.
    headers = []

    update_output(output_box, "Gathering table headers.\n")
    try:
        for i in table.find_all('th'):
            title = i.text
            headers.append(title)
        return headers
    except Exception as e:
        template = "An exception of type {0} occurred.\n"
        message = template.format(type(e).__name__)
        update_output(output_box, message)
        update_output(output_box, "Are you sure you selected the correct .html file?\n")


# A function to fill the unsorted 'Mech Stats dataframe.
def unsorted_fill_data_frame_helper(table, dataframe, output_box):
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(dataframe)
        dataframe.loc[length] = row

    update_output(output_box, "Finished gathering information at " + profileMechStats_url +
                  " and filling the dataframe.\n")


# A function to return the table found within the html text of the 'Mech Stats page.
def unsorted_html_table_helper(htmltext, output_box):
    # Obtain information from tag <table>
    update_output(output_box, "Finding Table of 'Mech stats.\n")
    return htmltext.find('table', class_='table table-striped')


# A function for sorting the unsorted 'Mech stats by matches played.
def sorted_mech_stats_mp(user_ign, output_box):
    update_output(output_box, "Now attempting to sort 'Mechs by matches played.\n")
    update_output(output_box, "Loading data from unsorted .csv file to dataframe.\n")

    # Create dataframe of 'Mechs sorted by matches played.
    sorted_matches_played = pd.read_csv(user_ign + "_" + 'mech_data_unsorted.csv')
    update_output(output_box, "Finished loading the unsorted data to dataframe.\n")

    # Removed columns that offer no real beneficial information
    update_output(output_box, "Removing 'Time Played' and 'XP Earned' entries from dataframe.\n")
    sorted_matches_played.drop(columns=['Time Played', 'XP Earned'], inplace=True)
    update_output(output_box, "Finished removing the 'Time Played' and 'XP Earned' columns from the dataframe.\n")

    # Sort by the values stored in the Matches Played column.
    update_output(output_box, "Sorting dataframe entries by Matches Played.\n")
    sorted_matches_played.sort_values(["Matches Played"], axis=0, ascending=False, inplace=True)
    update_output(output_box, "Finished sorting dataframe entries by Matches Played.\n")

    update_output(output_box, "Converting (sorted) Matches Played dataframe to .csv format for users viewing.\n")
    sorted_matches_played.to_csv(cwd + os.sep + user_ign + "_" + 'mech_data_sorted_MP.csv', index=False)
    update_output(output_box, "Finished converting Matches Played dataframe to .csv format.\n")


# A function to sort the unsorted 'Mech Stats by time played.
def sorted_mech_stats_tp(user, output_box):
    update_output(output_box, "Now attempting to sort 'Mechs by Time Played.\n")
    update_output(output_box, "Loading data from unsorted csv file.\n")
    # Create a copy of the unsorted data to be sorted.
    sorted_time_played = pd.read_csv(user + "_" + 'mech_data_unsorted.csv')

    # Find all 'Mechs that have X>24 hours play time.
    update_output(output_box, "Filtering out all 'Mechs with greater than 24 hours played.\n")
    filtered = sorted_time_played[sorted_time_played['Time Played'].str.contains("day")]
    update_output(output_box, "Finished filtering out all 'Mechs with greater than 24 hours played.\n")

    # List to store all converted times for 'Mechs with X>24 hours play time
    times_to_add = []

    # Do calculations to show appropriate number of hours instead of "X day(s)"
    update_output(output_box, "Converting 'days' to 24 * (number of days); to get total number of hours played "
                              "for filtered 'Mechs.\n")
    for k in filtered['Time Played']:
        time = k.split(' ')
        hours_to_add = 24 * int(time[0])
        # time[1] contains "days" which is what we are removing.
        hms = time[2]
        hms = hms.split(':')
        hours = hours_to_add + int(hms[0])
        hms = str(hours) + ':' + hms[1] + ':' + hms[2]
        times_to_add.append(hms)
    update_output(output_box, "Finished converting 'days' to hours.\n")

    # Change the Time Played strings of the 'mechs with X>24 hours time played to the calculated amount
    update_output(output_box, "Converting filtered 'Mechs Time Played entry with the converted days to hours.\n")
    for x in range(len(times_to_add)):
        sorted_time_played.loc[filtered.index[x], 'Time Played'] = times_to_add[x]
    update_output(output_box, "Finished converting filtered 'Mechs Time Played entry with the converted days to "
                              "hours.\n")

    # List to store all 'mechs time played
    all_hms = []

    # Remove all ':' characters from the string and convert the resulting string to an integer
    for y in sorted_time_played['Time Played']:
        time = y.split(':')
        hms = time[0] + time[1] + time[2]
        all_hms.append(int(hms))

    # Change the Time Played Strings to the integers
    for z in (range(len(all_hms))):
        sorted_time_played.loc[sorted_time_played.index[z], 'Time Played'] = all_hms[z]

    # Sort the Time Played column by the integer values in descending order
    update_output(output_box, "Sorting by Time Played entries of 'Mechs.\n")
    sorted_time_played = sorted_time_played.sort_values(['Time Played'], axis=0, ascending=False)
    update_output(output_box, "Finished sorting by Time Played.\n")

    # List to store our conversion from integer back to string with the appropriate format
    mutated_times = []

    # Convert integers to string in the correct format
    # I got lazy and tired. Went with ugly brute-forced code to reformat the time back to H:M:S
    update_output(output_box, "Reformatting Time Played to an easier-to-read format.\n")
    for a in sorted_time_played['Time Played']:
        mut_time = str(a)
        if len(mut_time) == 1:
            mut_time = "00:00:0" + mut_time
        elif len(mut_time) == 2:
            mut_time = "00:00:" + mut_time
        elif len(mut_time) == 3:
            mut_time = "00:0" + mut_time[0] + ':' + mut_time[1] + mut_time[2]
        elif len(mut_time) == 4:
            mut_time = "00:" + mut_time[0] + mut_time[1] + ':' + mut_time[2] + mut_time[3]
        elif len(mut_time) == 5:
            mut_time = "0" + mut_time[0] + ':' + mut_time[1] + mut_time[2] + ':' + mut_time[3] + mut_time[4]
        elif len(mut_time) == 6:
            mut_time = mut_time[0] + mut_time[1] + ':' + mut_time[2] + mut_time[3] + ':' + mut_time[4] + mut_time[5]
        elif len(mut_time) > 6:
            seconds = mut_time[-2] + mut_time[-1]
            minutes = mut_time[-4:-2]
            hours = mut_time[:-4]
            mut_time = hours + ':' + minutes + ':' + seconds
        mutated_times.append(mut_time)
    update_output(output_box, "Finished reformatting Time Played to an easier-to-read format.\n")

    # Change the Time Played Integers to the Strings we just built.
    update_output(output_box, "Storing the easier-to-read to the Time Played column of the dataframe.\n")
    for b in range(len(mutated_times)):
        sorted_time_played.loc[sorted_time_played.index[b], 'Time Played'] = mutated_times[b]
    update_output(output_box, "Finished storing the easier-to-read entries to the Time Played "
                              "column of the dataframe.\n")

    # Remove column that offers no real beneficial information
    update_output(output_box, "Removing 'XP Earned' entry from dataframe.\n")
    sorted_time_played.drop(columns=['XP Earned'], inplace=True)

    # As the 'Mechs were already previously sorted, and we have done no rearranging, simply output to .csv
    update_output(output_box, "Converting (sorted) time played dataframe to .csv format for users viewing.\n")
    sorted_time_played.to_csv(cwd + os.sep + user + "_" + 'mech_data_sorted_TP.csv', index=False)


def run_offline_stat_scraper(output_box):
    # Code for offline stat scraper
    update_output(output_box, "Running Offline Stat Scraper\n")
    update_output(output_box, "Please select the HTML file containing the stats.\n")

    soup = get_file_path(output_box)
    if soup is not None:  # check if soup is not None
        update_output(output_box, "Please enter your in-game username so we may properly label the file.\n")
        user_ign = get_user_ign(output_box)

        if unsorted_data_frame_helper(soup, user_ign, output_box) is False:
            return
        # ---------- Sort By Time Played ----------
        sorted_mech_stats_tp(user_ign, output_box)
        # ---------- Sort by Matches Played ----------
        sorted_mech_stats_mp(user_ign, output_box)

        update_output(output_box, "Your spreadsheets have been created! :D\n")
    else:
        update_output(output_box, "File path not valid or file not selected. HTML file does not exist.\n")


def run_offline_mech_scraper(output_box):
    # Code for offline mech scraper
    update_output(output_box, "Running Offline Mech Scraper\n")
    soup = get_file_path(output_box)
    if soup is not None:  # check if soup is not None
        user_ign = get_user_ign(output_box)
        html_mech_scraper(soup, user_ign, output_box)
    else:
        update_output(output_box, "File path not valid or file not selected. HTML file does not exist.\n")


def html_mech_scraper(html, user_ign, output_box):
    # Code for scraping the HTML of the User's Profile.
    update_output(output_box, "Starting to scrape the provided HTML file for relevant 'Mech information.\n")
    update_output(output_box, "This may take a moment. Please be patient. :)\n")

    # A list for us to store tuples containing the information about a 'Mech from the HTML file provided.
    mech_list = []

    try:
        # Find all 'Mechs that are owned within the HTML provided.
        for owned_mechs in html.find_all('li', class_='mech-collection-item owned'):
            # Get the 'Mechs Chassis Variant from the <h5> Header.
            chassis_variant = owned_mechs.find('h5').text
            parent = owned_mechs.find_parent('ul')
            grandparent = parent.find_parent('div')
            # Get the 'Mechs associated Faction [Inner Sphere, Clan] and it's Weight Class [Light, Medium, Heavy, Assault].
            # The HTML has the information saved in the following format, "Faction Weight_Class". So we need to split along
            # the spaces to separate the Factions from the Weight Class.
            chassis_faction_and_weight_class = grandparent.find('h3', class_='mech-collection-chassis-subtitle')
            chassis_faction_and_weight_class = chassis_faction_and_weight_class.text.split()
            if len(chassis_faction_and_weight_class) == 2:
                # Clan
                mech_faction = chassis_faction_and_weight_class[0].lower()  # Using .lower() to follow MechDB convention.
                mech_weight_class = chassis_faction_and_weight_class[1].lower()
            else:
                # Inner Sphere
                mech_faction = chassis_faction_and_weight_class[0].lower() + "_" + \
                               chassis_faction_and_weight_class[1].lower()
                mech_weight_class = chassis_faction_and_weight_class[2].lower()

            try:
                # Grab the tag which contains potential lists of multiple copies of the same 'Mech.
                duplicate_mechs = owned_mechs.find('ul')
                # Grab each individual copy of the same 'Mech a player owns.
                individual_mech = duplicate_mechs.find_all('li')
            except Exception as e:
                template = "An exception of type {0} occurred.\n"
                message = template.format(type(e).__name__)
                update_output(output_box, message)
                update_output(output_box, "Are you sure you properly loaded all 'Mech entries before saving your "
                                          "html file?\n")
                return

            # Find the 'Mechs player-defined name, and it's number of equipped skill points.
            for mech in individual_mech:
                # First span entry denotes the copy of the 'Mech (E.G., If you own two copies of the same 'Mech, this entry
                # will be "1)" and "2)").
                span_entries = mech.find('span')

                # Second span entry denotes the player defined name for the 'Mech (I.E., renaming the 'Mech in the Mech Lab)
                span_entries = span_entries.find_next_sibling('span')
                mechlab_mech_name = span_entries.text

                # Third span entry denotes the string of equipped skill nodes (E.G., "83 / 91").
                # We only care about the first token, as it is the number denoting the number of equipped nodes.
                span_entries = span_entries.find_next_sibling('span')
                span_entries = span_entries.text.split()
                num_skill_nodes_equipped = span_entries[0]

                # Open the locally stored MechDB JSON file and grab the specified 'Mechs tonnage.
                try:
                    with open("mechdb.json", "r") as file:
                        mech_data = json.load(file)
                        # Check that the JSON file is populated with the string of mech information.
                        if mech_data != "":
                            for mech_info in mech_data["data"]:
                                # Find the correct tonnage associated with the mech we are currently looking at.
                                if mech_info['display_name'] == chassis_variant:
                                    mech_tonnage = mech_info['tonnage']
                                    # Create a tuple of the information about the specific 'Mech and store it in a list.
                                    mech_list.append(((re.sub("[(].*?[)]", "", chassis_variant), chassis_variant,
                                                   mechlab_mech_name, mech_tonnage, mech_faction, mech_weight_class,
                                                   num_skill_nodes_equipped)))
                        else:
                            # The JSON string of information does not exist.
                            mech_tonnage = "--"
                            # Create a tuple of the information about the specific 'Mech and store it in a list.
                            mech_list.append(((re.sub("[(].*?[)]", "", chassis_variant), chassis_variant,
                                           mechlab_mech_name, mech_tonnage, mech_faction, mech_weight_class,
                                           num_skill_nodes_equipped)))

                except (FileNotFoundError, json.JSONDecodeError):
                    # The JSON file was not found.
                    mech_tonnage = "--"
                    # Create a tuple of the information about the specific 'Mech and store it in a list.
                    mech_list.append(((re.sub("[(].*?[)]", "", chassis_variant), chassis_variant,
                                   mechlab_mech_name, mech_tonnage, mech_faction, mech_weight_class,
                                   num_skill_nodes_equipped)))

        # Check that the list is empty.
        if not mech_list:
            # If empty, explain why their .csv may not have been created.
            update_output(output_box, "Mech List was not generated due to an error occurring.\n")
            update_output(output_box, "Are you sure you selected the correct .html file?\n")
        else:
            # Otherwise, create their .csv file.
            update_output(output_box, "We have finished making the list of owned 'Mechs and their appropriate "
                                      "tuples.\n")

            # Convert list of tuples (mech base variant, actual variant, name, tonnage, faction, weight class, equipped
            # skill points) into a dataframe.
            update_output(output_box, "Converting list of tuples (Base, Variant, User Defined Name, Tonnage, Faction, "
                                      "Weight Class, Skill Points) to data frame.\n")
            df_list_mech_name_sp = pd.DataFrame(mech_list,
                                                columns=['Base', 'Variant', 'Name', 'Tonnage', 'Faction', 'Class',
                                                         'Skill Points'])

            # Convert dataframe to csv file.
            update_output(output_box, "Converting (Base, Variant, User Defined Name, Tonnage, Faction, Weight Class, "
                                      "Skill Points) dataframe to .csv format for users viewing.\n")

            df_list_mech_name_sp.to_csv(cwd + os.sep + user_ign + "_" + 'owned_mechs_SP.csv', index=False)

            update_output(output_box, "Your spreadsheets have been created! :D\n")
    except Exception as e:
        template = "An exception of type {0} occurred.\n"
        message = template.format(type(e).__name__)
        update_output(output_box, message)
        update_output(output_box, "Are you sure you selected the correct .html file?\n")

# ------------------------------------------------------------------------------------------


# ------------------------------------- AUXILIARY ------------------------------------------

# A function for updating the output text box on the GUI, so we don't need to continuously call the same 5 lines
# of code.
def update_output(output_box, output_str):
    output_box.config(state=tk.NORMAL)     # Turn off "Read-Only" on the text box.
    output_box.insert(tk.END, output_str)  # Print the string to the text box.
    output_box.update()                    # Update the display of the text box to see the newly printed string.
    output_box.see(tk.END)                 # Automatically "scroll-down" the text box.
    output_box.config(state=tk.DISABLED)   # Turn on "Read-Only" on the text box.


# A method to check if the site is available.
def is_site_available(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code >= 400:
            return False
        return True
    except requests.exceptions.RequestException:
        return False


def get_file_path(output_box):
    # Ask the user to select a file
    update_output(output_box, "Gathering file path to the HTML file from user.\n")

    file_path = tk.filedialog.askopenfilename(initialdir=os.path.expanduser('~'), title="Select HTML File",
                                              filetypes=[("HTML Files", "*.html")])
    # Check if the user selected a file
    if file_path:
        # If a file was selected, print the path to the file
        update_output(output_box, "Selected file: " + file_path + "\n")
        with open(file_path, "r", encoding="utf8") as file:
            # Read the contents of the file and parse with BeautifulSoup
            html = file.read()
            soup = BeautifulSoup(html, "html.parser")
            return soup  # return the soup object
    else:
        # If no file was selected, print a message to the console and return None
        update_output(output_box, "No file selected\n")
        return None


# A function to prompt the user for an In-Game Name so the Offline files may be properly labeled.
def get_user_ign(output_box):
    user_ign = ""  # variable to store the user's input.

    # Nested function for the submit button to store the user's input before destroying the box that prompts the user.
    def submit_username():
        nonlocal user_ign
        user_ign = user_ign_entry.get()
        dialog.destroy()

    # Set up box to prompt user for their In-Game name.
    dialog = tk.Toplevel()
    dialog.title("In-Game Name")
    tk.Label(dialog, text="Please enter your in-game username so we may properly label the file.").grid(row=0,
                                                                                                        column=0,
                                                                                                        padx=5,
                                                                                                        pady=5)
    user_ign_entry = tk.Entry(dialog)
    user_ign_entry.grid(row=1, column=0, padx=5, pady=5)

    # Create submit button for prompt box.
    submit_button = tk.Button(dialog, text="Submit", command=submit_username)
    submit_button.grid(row=2, column=0, padx=5, pady=5)

    # Center the prompt box in the center of the users screen
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2
    y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2
    dialog.geometry("+%d+%d" % (x, y))

    dialog.transient(output_box.master)
    dialog.grab_set()
    output_box.master.wait_window(dialog)

    return user_ign


# A function to store a copy of MechDB's API JSON response on the user's machine.
def update_offline_mech_db(output_box):
    # Code for updating the locally stored information of MechDB.
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer Z8YvyDlFEubyCYGbqtkaGMrfmAKuJwHOXaae3hxqbml1ytmww2qpeiKRgp97efG1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
    }
    update_output(output_box, "Attempting to establish a connection with MechDB "
                              "(https://mwo.nav-alpha.com/api/mechs/).\n")
    mech_db = requests.request("POST", mech_db_url, headers=headers)
    if mech_db.status_code == 200:
        update_output(output_box, "Connection with MechDB successful.\n")
        update_output(output_box, "Saving additional data from MechDB.\n")
        with open("mechdb.json", "w") as outfile:
            json.dump(mech_db.json(), outfile)
            update_output(output_box, "MechDB information successfully saved.\n")

    else:
        update_output(output_box, "Unable to load extra data from MechDB.\n")
        update_output(output_box, "MechDB information failed to save.\n")


def check_log_in_creds(response, output_box):
    if 'Invalid email/password' in response.text:
        update_output(output_box, "Invalid email/password entered, please try again.\n")
        return False
    if 'An internal server error has occured' in response.text:  # Lols. PGI has a typo in their error message.
        update_output(output_box, "(50) An internal server error has occurred. Please contact support.\n")
        update_output(output_box, "... Just to be clear, contact PGI support. It's their error, not mine.\n")
        return False
    if 'Please enter your email and password!' in response.text:
        update_output(output_box, "Please enter your email and password!\n")
# ------------------------------------------------------------------------------------------


def main():
    # Create the GUI
    root = tk.Tk()
    root.title("MechWarriorOnline Mech Scraper")
    root.geometry("768x720")

    # Label to explain a little about how to use MWOMechScraper
    label_text = "Welcome to the MechWarriorOnline Mech Scraper!\n\n"
    label_text += "This program scrapes data from the mwomercs.com website to collect\n"
    label_text += "information about your in-game stats and owned 'Mechs and outputs .CSV \n"
    label_text += "files for easy understanding of what your 'Mech stats are and what 'Mechs\n"
    label_text += "you own. Please use the buttons below to start the online or offline stat\n"
    label_text += "or 'Mech scraper. The message box below will display the status of the tool\n"
    label_text += "as it runs. If the file \"creds.txt\" is not found within the same folder\n"
    label_text += "containing the tool when the online version is ran, you will be prompted\n"
    label_text += "for your email and password.\n"
    label_text += "If the offline version(s) are ran, it will prompt you for your in-game name\n"
    label_text += "to properly name the .CSV files.\n"
    label_text += "NOTE: To run the offline Mech scraper it is suggested to first update your offline\n"
    label_text += "mechdb by pressing the \"Update Offline MechDB\" button. This does require a connection\n"
    label_text += "to the internet but ensures you will have the tonnage values for the 'Mech Chassis.\n"
    label_text += "This will allow the tool to store a local version of the MechDB API's response so the\n"
    label_text += "tool may get the tonnage of 'Mechs."

    label = tk.Label(root, text=label_text, font=("Courier", 10), justify="left")
    label.pack(fill=tk.BOTH, padx=20, pady=20)

    # create a read-only text box
    output_box = tk.Text(root, height=10, width=80, state="disabled")
    output_box.pack()

    # Create a frame for the online buttons
    online_frame = tk.Frame(root)
    online_frame.pack()

    # create the online buttons
    online_stat_button = tk.Button(online_frame, text="Online Stat Scraper", font=("Arial", 12),
                                   command=lambda: run_online_stat_scraper(output_box), padx=10, pady=10)
    online_mech_button = tk.Button(online_frame, text="Online Mech Scraper", font=("Arial", 12),
                                   command=lambda: run_online_mech_scraper(output_box), padx=10, pady=10)

    # add the online buttons to the frame
    online_stat_button.pack(side="left", padx=10)
    online_mech_button.pack(side="right", padx=10)

    # create a frame for the offline buttons
    offline_frame = tk.Frame(root)
    offline_frame.pack()

    # create the offline buttons
    offline_stat_button = tk.Button(offline_frame, text="Offline Stat Scraper", font=("Arial", 12),
                                    command=lambda: run_offline_stat_scraper(output_box), padx=10, pady=10)
    offline_mech_button = tk.Button(offline_frame, text="Offline Mech Scraper", font=("Arial", 12),
                                    command=lambda: run_offline_mech_scraper(output_box), padx=10, pady=10)

    # add the offline buttons to the frame
    offline_stat_button.pack(side="left", padx=10, pady=10)
    offline_mech_button.pack(side="right", padx=10, pady=10)

    # create a frame for the update button
    update_frame = tk.Frame(root)
    update_frame.pack()

    # create the update button
    update_db_button = tk.Button(update_frame, text="Update Offline MechDB", font=("Arial", 12),
                                 command=lambda: update_offline_mech_db(output_box), padx=10, pady=10)

    # add the update button to the frame
    update_db_button.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
