# coding=utf-8

import os
import json
from glpi import GLPI

# GLPI Api url
url = "https://hglpi.domain.com/apirest.php"

# GLPI User credentials
#user = "glpi-api"
#password = "glpi_123"

# Generate in Configuration -> General -> API
app_token = ""
# Generate in User Preference
api_token = ""

glpi = GLPI(url, app_token, api_token)


profile = json.dumps(glpi.get('ticket', 34954),
                  indent=4,
                  separators=(',', ': '),
                  sort_keys=True)

print(profile)
#print("Getting 'My' profile: ")
#print(glpi.get("getMyProfiles"))

Getid = json.loads(profile)
#print(Getid)
#print(Getid['id'])
#Getid.get('id')
#print(id)
#print(profile)

#glpi.kill()
