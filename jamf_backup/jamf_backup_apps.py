# Copyright (c) 2021 Brandon Childers and Sariah Shoemaker

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions
#:

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
    parser = argparse.ArgumentParser(description="Example usage: jamf_export_apps.py --url https://sub.jamfcloud.com --file export.csv --user testinguser --pass supersecret")
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
# Queries JAMF API for all Configuration Profiles and extracts their app ids into an array.
# Returns config_ids array

def FetchIDS(jss_url, session):
    config_ids = []
    jss = jss_url + "/JSSResource/configurationprofiles"
    jss_response = session.get(jss)
    print(jss_response) # Testing
    jss_json = json.loads(jss_response.text)
    print(jss_json)
    for profile in jss_json["configuration_profiles"]:
        config_ids.append(profile["id"])
    print (config_ids)
    return config_ids

# Function: FetchConfigData(jss_url, session, config_ids)
# Queries JAMF API for each Configuration Profiles data and puts that data into a dictionary config_data
# Returns config_data

def FetchConfigData(jss_url, session, config_ids):
    config_data = {}
    for id in config_ids:
        jss = jss_url + "/JSSResource/configurationprofiles/id/" + str(id)
        jss_response = session.get(jss)
        jss_json = json.loads(jss_response.text)
        config_data[id] = jss_json
    print (config_data)
    return (config_data)

# Function: CreateDirectory(directory_name)
# Creates a directory to put the data in
# Returns success statement

def CreateDirectory(directory_name):
    pass

# Function: WriteXMLToFiles(config_data, directory_name, file_name)
# Writes the config_data to an XML file
# Returns success statement

def WriteXMLToFiles(config_data, directory_name, file_name):
    pass

# Main Function

def main():
    args = ParseArguments()
    basejss = args.jssurl
    user = args.username
    password = args.password
    session = CreateSession(user,password)
    ids = FetchIDS(basejss, session)
    config_data = FetchConfigData(basejss, session, ids)  

if __name__ == "__main__":
    main()
