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
import datetime

# ----------------------------------------------------------------------------------

# Function: ParseArguments()
# Parses command line flags
# Returns args object
def ParseArguments():
    parser = argparse.ArgumentParser(description="This program will take a csv of app ids expored from jamf_gather_apps.py, back them up to a text file, and delete them from Jamf.Example usage: jamf_delete_apps.py --url https://sub.jamfcloud.com --file delete.csv --user testinguser --pass supersecret")
    parser.add_argument('--url', dest='jssurl', type=str, help='Your JAMF URL. (Must include https://) Example: https://sub.jamfcloud.com', required=True)
    parser.add_argument('--file', dest='filename', type=str, help='The filename you would like to source the appids for deleteion from.', required=True)
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

# Function: WriteArrayFile(array, filename)
# Writes an array to a file of choice.
# Returns Void
def WriteArrayFile(array, filename):
    try:
        with open(filename, 'w', newline='') as file:
            for item in array:
                 file.write("%s\n" % item)

    except IOError:
        print("I/O Error")

# Function: ReadCSV(filename)
# Reads csv and extracts array of Application IDs
# Returns array
def ReadCSV(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            for line in csv.DictReader(file):
                data.append(line["id"])
    except IOError:
        print("I/O Error")
    return data

# Function: DeleteApps(array, url, session)
# Queries API for specific applications based on array of app ids, then backs their json data up to a *.backup file in the case of accidental deletion then deletes the apps
# Returns Void
def DeleteApps(array, url, session):
    backup = []
    for x in range(len(array)):
        jss_url = url + "/JSSResource/mobiledeviceapplications/id/{}".format(str(array[x]))
        jss_response = session.get(jss_url)
        jss_json = json.loads(jss_response.text)
        backup.append(jss_json)
        delete = session.delete(jss_url)
    WriteArrayFile(backup, "{}.backup".format(str(datetime.datetime.now().timestamp())))


# Main Function

def main():
    args = ParseArguments()
    csv_file = args.filename
    basejss = args.jssurl
    user = args.username
    password = args.password
    session = CreateSession(user,password)
    data = ReadCSV(csv_file)
    DeleteApps(data,basejss,session)

    
if __name__ == "__main__":
    main()
