#!/usr/bin/python3
############################
# Domain Expiration script #
############################

import os, re, sys
import xml.etree.ElementTree as ET
from datetime import date
from datetime import datetime

# Domain parameter
domain = sys.argv[1]

# Path to the script
scriptPath = '/etc/zabbix/scripts/domainExpiration/'

# Defining variables for authorization on 'namecheap' API
ncUser = sys.argv[2]
apiUser = sys.argv[3]
apiKey = sys.argv[4]
clientIp = sys.argv[5]

# Command used to get info from 'namecheap' provider
apiCommand = 'curl -s "https://api.namecheap.com/xml.response?ApiUser='+ apiUser +'&ApiKey=' + apiKey + '&UserName=' + ncUser + '&ClientIp=' + clientIp + '&Command=namecheap.domains.getinfo&DomainName="' + domain + ' > ' + scriptPath + domain + '.xml'

# Checking if file exists for timesaving
if os.path.isfile(scriptPath + domain + '.xml') == False:
    # Getting general information about domain
    cmnd = os.system(apiCommand)

# Defining current date
currentDateGet = str(datetime.now())
currentDateRegex = re.compile(r'\d\d\d\d-\d\d-\d\d')
currentDateMatch = currentDateRegex.search(currentDateGet)
currentDate = currentDateMatch.group().split('-')
expirationDate = ''

# Parsing 'domain'.xml data
fileTree = ET.parse(scriptPath + domain + '.xml')
root = fileTree.getroot()
for child in root.findall('.//{http://api.namecheap.com/xml.response}DomainDetails/{http://api.namecheap.com/xml.response}ExpiredDate'):
    exp = child.text
    expirationDate = exp.split('/')

# Preformating dates
cDate = date(int(currentDate[0]), int(currentDate[1]), int(currentDate[2]))
eDate = date(int(expirationDate[2]), int(expirationDate[0]), int(expirationDate[1]))

# Getting dates delta
deltaDates = eDate - cDate
if deltaDates.days < 0:
    print('0')
else:
    print(deltaDates.days)
