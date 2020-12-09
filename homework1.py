import requests
from pprint import pprint
import json

# github username
username = "IgSurg"

# url to request
url = f"https://api.github.com/users/{username}/repos"
# make the request and return the json

response = requests.get(url)
if response.ok:
    repos_data = response.json()

# print JSON name

for i in range(len(repos_data)):
    print(f"Репозиторий {i+1}: {repos_data[i]['name']}")

# write to file
with open("homework1-git.json", "w") as f:
    json.dump(repos_data, f)

#############################################################################################




