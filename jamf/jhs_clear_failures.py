# Copyright (c) 2020 Brandon Childers

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

import requests
import json
import datetime
print(datetime.datetime.now())
basejss = "https://my.jamfcloud.com/JSSResource"
smart_group_id = 185 # Use API to grab Smart Group ID #
jssm = basejss + "/mobiledevicegroups/id/{}".format(str(smart_group_id))
jss_user = "API_USER"
jss_password = "super_secret"
jss_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
s = requests.Session()
s.auth = (jss_user, jss_password)
s.headers.update(jss_headers)

jss_response = s.get(jssm)
jss_json = json.loads(jss_response.text)
group = jss_json["mobile_device_group"]
devices = group["mobile_devices"]
print("Gathering IDs")
ids = []
for x in range(len(devices)):
    device = devices[x]
    ids.append(device['id'])


print("Removing Failed Commands - This may take 20+ minutes based on inventory size.")
for y in ids:
    getmdurl = basejss + "/commandflush/mobiledevices/id/{}/status/Failed".format(str(y))
    dcommand = s.delete(getmdurl)
    print("Deleted Fled Commands for ID: {} - Response was: {}".format(str(y), dcommand))
