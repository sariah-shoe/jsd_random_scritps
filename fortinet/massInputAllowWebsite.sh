#!/bin/sh

# This script will output the correctly formatted syntax for inputing a csv of websites to whitelist. You can pipe | this into pbcopy on a mac. Then paste it
# into the firewall handling the filtering. Note: make sure you're under your vdom.

echo "config webfilter ftgd-local-rating"
cat whitelist.csv | while read line; do
currentAddress=${line}
echo "edit \"${currentAddress}\""
# show webfilter ftgd-local-rating to see rating category of existing rule. 
echo "set rating \"142"\"
echo "next"
done
echo "end"
echo "end"
