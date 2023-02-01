# Imports
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import creds

# Urls
# Log-in Webpage
login_url = 'https://mwomercs.com/do/login'
# Logged-In Player Mech Stats Webpage
profileMechStats_url = 'https://mwomercs.com/profile/stats?type=mech'
# Logged-In Player's Raw Data of Mechs
collection_data_url = 'https://mwomercs.com/mech-collection/data'

# Player's Credentials to be used on log-in
payload = {
    'email': creds.email,
    'password': creds.password
}

# Open a session
with requests.session() as s:
    s.post(login_url, data=payload)
    r = s.get(profileMechStats_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Obtain information from tag <table>
    mechs_table = soup.find('table', class_='table table-striped')
    # print(mechs_table)

    # Collect the headers
    headers = []
    for i in mechs_table.find_all('th'):
        title = i.text
        headers.append(title)

    # Create the dataframe
    mech_data = pd.DataFrame(columns=headers)

    # Fill the dataframe
    for j in mechs_table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(mech_data)
        mech_data.loc[length] = row

    # Convert scraped data table to .csv
    mech_data.to_csv('mech_data_unsorted.csv', index=False)

    # ----------- Sort By Time Played -----------
    sorted_time_played = pd.read_csv('mech_data_unsorted.csv')

    # Find all 'mechs that have X>24 hours play time
    filtered = sorted_time_played[sorted_time_played['Time Played'].str.contains("day")]

    # List to store all converted times for 'mechs with X>24 hours play time
    times_to_add = []

    # Do calculations to show appropriate number of hours instead of "X day(s)"
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

    # Change the Time Played Integers to Strings
    for b in range(len(mutated_times)):
        sorted_time_played.loc[sorted_time_played.index[b], 'Time Played'] = mutated_times[b]

    # As the mech's were already previously sorted, and we have done no rearranging, simply output to .csv
    sorted_time_played.to_csv('mech_data_sorted_TP.csv', index=False)

    # Create .csv of mech's sorted by matches played.
    sorted_matches_played = pd.read_csv('mech_data_unsorted.csv')
    sorted_matches_played.sort_values(["Matches Played"], axis=0, ascending=False, inplace=True)
    sorted_matches_played.to_csv('mech_data_sorted_MP.csv', index=False)

    # ---------- Player Profile Scraper ----------
    response = s.get(collection_data_url)
    # Create a file to store the raw data
    file1 = open('mech_collection.json', 'w')
    # Fill the file with the data for use
    file1.writelines(response.text)
    # Close the file to prevent memory mismanagement
    file1.close()

    # A list container to store which 'mechs are owned
    owned_mechs = []

    with open('mech_collection.json') as f:
        # Convert the JSON file into a python recognizable data format (I.E., Dict)
        data = json.load(f)
        collection = data['collection']
        for collection_data in collection:
            variants_data = collection_data['variants']
            for specific_variant in variants_data:
                if variants_data[specific_variant]['owned'] is True:
                    owned_mechs.append(variants_data[specific_variant]['display_name'])

        # Convert list of owned 'mechs into a dataframe
        df_owned_mechs = pd.DataFrame(owned_mechs, columns=['Owned \'Mechs'])

        # Create a .csv from the dataframe of owned 'mechs
        df_owned_mechs.to_csv('owned_mechs.csv', index=False)
