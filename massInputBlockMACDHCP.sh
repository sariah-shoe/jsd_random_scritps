#!/bin/sh

# This script will output the correctly formatted syntax for inputing a csv of mac-addresses to block from receiving DHCP reservations. You can pipe | this into pbcopy on a mac. Then paste it
# into the firewall. Note: make sure you're under your vdom.

echo "config system dhcp server"

# show system dhcp server to see index' of rules and grab the correct "counter value"

echo "edit 26"
echo "config reserved-address"
counter=650
cat file.csv | while read line; do
currentMAC=${line}
l="edit ${counter}"
echo "$l"
let "counter++"
echo "set mac ${currentMAC}"
echo "set action block"
echo "next"
done
echo "end"
echo "end"
