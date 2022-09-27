# coding=utf-8

import os
import json
from glpi import GLPI

# GLPI Api url
url = "https://hglpi.ufba.br/apirest.php"

# GLPI User credentials
#user = "glpi-api"
#password = "glpi_123"

# Generate in Configuration -> General -> API
app_token = "Gx1v3Knn4kzo6prgH5xSZYTgdSK7ehAid26mb7pg"
# Generate in User Preference
api_token = "VQpfz8UywZuyTkr2MnIUC9rC5BkmCv0MtcT6Ku24"

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
