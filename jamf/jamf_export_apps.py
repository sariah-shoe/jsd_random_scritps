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
# Queries JAMF API for all Mobile Apps and extracts their app ids into an array.
# Returns app_ids array

def FetchIDS(jss_url, session):
    app_ids = []
    jss = jss_url + "/JSSResource/mobiledeviceapplications"
    jss_response = session.get(jss)
    jss_json = json.loads(jss_response.text)
    full_app_list = jss_json["mobile_device_applications"]
    for x in range(len(full_app_list)):
        current_app = full_app_list[x]
        app_ids.append(current_app['id'])
    return app_ids

# Function: FetchAppInfo(jss_url, session, app_ids)
# Queries JAMF API for all Detailed App Info and compiles an array of specific data points.
# Returns apps_detailed array

def FetchAppInfo(jss_url, session, app_ids):
    apps_detailed = []
    for x in range(len(app_ids)):
        jss = jss_url + "/JSSResource/mobiledeviceapplications/id/{}".format(str(app_ids[x]))
        jss_response = session.get(jss)
        jss_json = json.loads(jss_response.text)
        device_profile = {}
        device_profile['id'] = jss_json['mobile_device_application']['general']['id']
        device_profile['name'] = jss_json['mobile_device_application']['general']['name']
        device_profile['display_name'] = jss_json['mobile_device_application']['general']['display_name']
        device_profile['bundle_id'] = jss_json['mobile_device_application']['general']['bundle_id']
        device_profile['version'] = jss_json['mobile_device_application']['general']['version']
        device_profile['scope'] = jss_json['mobile_device_application']['scope']['mobile_device_groups']
        device_profile['scope_all'] = jss_json['mobile_device_application']['scope']['all_mobile_devices']
        device_profile['scope_all_users'] = jss_json['mobile_device_application']['scope']['all_jss_users']
        device_profile['vpp_on'] = jss_json['mobile_device_application']['vpp']['assign_vpp_device_based_licenses']
        if device_profile['vpp_on'] == True:
            device_profile['vpp_licenses'] = jss_json['mobile_device_application']['vpp']['total_vpp_licenses']
            device_profile['vpp_licenses_used'] = jss_json['mobile_device_application']['vpp']['used_vpp_licenses']
            device_profile['vpp_licenses_remaining'] = jss_json['mobile_device_application']['vpp']['remaining_vpp_licenses']
        apps_detailed.append(device_profile)
    return apps_detailed



# Function: WriteToCSV(apps_detailed, column_headers, filename)
# Writes to CSV
# Void Return

def WriteToCSV(apps_detailed, column_headers, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)
            writer.writeheader()
            for data in apps_detailed:
                writer.writerow(data)
    except IOError:
        print("I/O Error")


# Main Function

def main():
    csv_columns = ['id','name','display_name','bundle_id','version','scope','scope_all','scope_all_users','vpp_on','vpp_licenses','vpp_licenses_used','vpp_licenses_remaining']
    args = ParseArguments()
    csv_file = args.filename
    basejss = args.jssurl
    user = args.username
    password = args.password
    session = CreateSession(user,password)
    ids = FetchIDS(basejss, session)
    app_data = FetchAppInfo(basejss, session, ids)
    WriteToCSV(app_data, csv_columns, csv_file)
    
if __name__ == "__main__":
    main()
