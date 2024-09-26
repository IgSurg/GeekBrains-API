import requests
import json
import base64

json_string = '{"inputtext":"Привет. Как дела?","ssml":"Text","voicename":"ru-RU-Standard-E_FEMALE","voicetype":"HeadPhones",' \
              '"encoding":"Mp3","speed":1,"pitch":0,"volume":0,"saveFileLocally":"Yes"}'

data = json.loads(json_string)

usrPass = b'name:password'
b64Val = base64.b64encode(usrPass)
b64Val = str(b64Val,'utf-8')

resp = requests.post('https://www.de-vis-software.ro/tts.aspx',
                                  headers={"Authorization": "Basic %s" % b64Val,
                                                 'Content-Type': 'application/json',
                                                 'Accept': 'application/json'}, json=data)
resp_data = resp.json()
print(resp_data)