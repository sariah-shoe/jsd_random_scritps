# Copyright (c) 2021 Brandon Childers

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv
import requests
import json
import argparse

# ----------------------------------------------------------------------------------

# Function: ParseArguments()
# Creates a session with authentication credentials and requried headers.
# Returns Session
def ParseArguments():
    parser = argparse.ArgumentParser(description="Example usage: jamf_export_config_profiles.py --url https://sub.jamfcloud.com --file export.csv --user testinguser --pass supersecret")
    parser.add_argument('--url', dest='jssurl', type=str, help='Your JAMF URL. (Must include https://) Example: https://sub.jamfcloud.com', required=True)
    parser.add_argument('--file', dest='filename', type=str, help='The filename you would like to save the export as.', required=True)
    parser.add_argument('--user', dest='username', type=str, help='Your JAMF username.', required=True)
    parser.add_argument('--pass',dest='password', type=str, help='Your JAMF password.', required=True)
    args = parser.parse_args()
    return args


# Function: CreateSession(username, password)
# Creates a session with authentication credentials and requried headers.
# Returns Session

def CreateSession(username, password):
    jss_headers = {'Content-Type':'application/json','Accept':'application/json'}
    s = requests.Session()
    s.auth = (username, password)
    s.headers.update(jss_headers)
    return s



# Function: FetchIDS(jss_url, session)
# Queries JAMF API for all Mobile Config Profiles and extracts their config ids into an array.
# Returns conf_ids array

def FetchIDS(jss_url, session):
    conf_ids = []
    jss = jss_url + "/JSSResource/configurationprofiles"
    jss_response = session.get(jss)
    jss_json = json.loads(jss_response.text)
    full_conf_list = jss_json["configuration_profiles"]
    for x in range(len(full_conf_list)):
        current_config = full_conf_list[x]
        conf_ids.append(current_config['id'])
    return conf_ids

# Function: FetchConfInfo(jss_url, session, conf_ids)
# Queries JAMF API for all Detailed Mobile Config Info and compiles an array of specific data points.
# Returns conf_detailed array

def FetchConfInfo(jss_url, session, conf_ids):
    conf_detailed = []
    for x in range(len(conf_ids)):
        jss = jss_url + "/JSSResource/configurationprofiles/id/{}".format(str(conf_ids[x]))
        jss_response = session.get(jss)
        jss_json = json.loads(jss_response.text)
        device_profile = {}
        device_profile['id'] = jss_json['configuration_profile']['general']['id']
        device_profile['name'] = jss_json['configuration_profile']['general']['name']
        device_profile['scope'] = jss_json['configuration_profile']['scope']['mobile_device_groups']
        device_profile['scope_all'] = jss_json['configuration_profile']['scope']['all_mobile_devices']
        device_profile['scope_all_users'] = jss_json['configuration_profile']['scope']['all_jss_users']
        conf_detailed.append(device_profile)
    return conf_detailed



# Function: WriteToCSV(conf_detailed, column_headers, filename)
# Writes to CSV
# Void Return

def WriteToCSV(conf_detailed, column_headers, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)
            writer.writeheader()
            for data in conf_detailed:
                writer.writerow(data)
    except IOError:
        print("I/O Error")


# Main Function

def main():
    csv_columns = ['id','name','scope','scope_all','scope_all_users']
    args = ParseArguments()
    csv_file = args.filename
    basejss = args.jssurl
    user = args.username
    password = args.password
    session = CreateSession(user,password)
    ids = FetchIDS(basejss, session)
    conf_data = FetchConfInfo(basejss, session, ids)
    WriteToCSV(conf_data, csv_columns, csv_file)
    
if __name__ == "__main__":
    main()
