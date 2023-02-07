from getpass import getpass
import requests
import json
from datetime import datetime
import re
from badgr_lite.models import BadgrLite

from lib.config import USERNAME, MAP_NAME_FILE, TOKEN_FILE

## Introduce the password to access to Badgr and gettin a token
pwrd = getpass('Introduce contrasena Badgr: ')
auth_params = {'username':USERNAME, 'password':pwrd}
auth_url = 'https://api.badgr.io/o/token'

## Send auth info and receive a file which is going to be saved
## in a json file. It expires in 1 day
token_raw = requests.post(auth_url, data=auth_params).content
token = json.loads(token_raw)

with open(TOKEN_FILE, 'w') as f:
    json.dump(token, f)

## Connect to Badgr and print the badges
client = BadgrLite(token_filename=TOKEN_FILE)

cb = client.badges
print("\n\n")
for badge in cb:
    print(badge)

print("\n")

ls_badges_out = []
ls_norm_att_out = []
ls_names = []
while True:
    ## Print only those which contains a certain string
    # You can finish the process just when you have at least one badge
    name_fil = input("Filtra por nombre (Q para salir): ")
    if (name_fil.upper() == "Q")&(len(ls_badges_out)>=1):
        break
    elif (name_fil.upper() == "Q")&(len(ls_badges_out)<1):
        print("\nNecesitas al menos un badge\n")
        continue
    
    cb_fil = [badge for badge in cb if name_fil.lower() in badge.name.lower()]

    if cb_fil == []:
        print("No hay coincidencias")
    else:
        for badge in cb_fil:
            print(badge)

    print("\n")

    ## Get ID of the one you are interested in assigning
    # You can finish the process just when you have at least one badge
    id = input("Copia y pega el ID del badge (Q para salir): ")
    if (id.upper() == "Q")&(len(ls_badges_out)>=1):
        break
    elif (id.upper() == "Q")&(len(ls_badges_out)<1):
        print("\nNecesitas al menos un badge\n")
        continue
    
    # Check out all the badges
    badge = [bd for bd in cb if bd.entity_id == id][0]

    norm_att = list(filter(lambda x: (not re.match('_', x)) 
                        & (x not in ['REQUIRED_ATTRS', 'REQUIRED_JSON']), 
                    dir(badge)))

    # Get the badges and their properties in two lists
    # Future: It could be just one list [(badge1, attributes1), ...]
    ls_badges_out.append(badge)
    ls_norm_att_out.append(norm_att)
    
    # Get the names so that we can see our current selection
    ls_names.append(getattr(badge, 'name', badge.entity_id))

    print("\nCurrent selection: ", ls_names)
    print("\n\n")
print("\n")

## Read name mappings
with open(MAP_NAME_FILE, 'r', encoding='utf-8') as f_names:
    d_names = json.load(f_names)

## Ask for the receiver's email
receivers = []
while True:
    email = input(f"Introduce Correos Destinatarios (Q to finish, All to send to {MAP_NAME_FILE}): ")
    if email.upper() == "Q":
        break
    elif email.upper() == "ALL":
        receivers = list(d_names.keys())
        break
    else:
        # HOTFIX: Needs a name
        receivers.append(email)
        print(receivers, end="\n")

## Format the badge content just to avoid errors
print("\n\n")
print("Sending...", "\n")
for email in receivers:
    email = email.replace("\n", "") 
    d_att = {}

    for norm_att, badge in zip(ls_norm_att_out, ls_badges_out):
        for att in norm_att:
            d_att[att] = getattr(badge,att)

        d_att['created_at'] = datetime.strftime(d_att['created_at'], '%Y-%m-%dT%H:%M:%S')
        d_att['recipient'] = {"identity": email}
        d_att['narrative'] = "Otorgado a {} por su excelente desempeño".format(d_names[email])
        d_att["notify"] = True
        d_att.pop('expires')

        ## Assign the badge
        result = client.award_badge(badge.entity_id, badge_data=d_att)

        print(email)
        print(d_att['name'])
        print(result)
        print("\n")