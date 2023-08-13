import requests
import json
import jq

url = "https://api.planningcenteronline.com/services/v2/songs"

headers = {
  'Authorization': 'Basic MzBlYzU1NzBjYzdiMjUyYzk4NGRmNTg4YWRiYzJmNzYzNmE1MWViOTAxNTNjOWE5NWMzZWIyMTMxNWVhZjYxYjpmOTU1MDZlOWQ3Yzk5NzgxMjE1OWZlNmNiNTk1YTI2NjI2MmQzMTdlNjM4ODYxYzVmYmNmM2E5NGMyZjM5OGFi'
}

response = requests.get(url, headers=headers)
data = response.json()

song_id_map = {}

for song_data in data['data']:
    song_id_map[song_data['attributes']['title']] = song_data['id']

print("song_id_map: ", song_id_map)

song_arrangement_map = {}


for song_data in data['data']:
    song_id = song_data['id']
    song_title = song_data['attributes']['title']
    
    arrangement_url = f"https://api.planningcenteronline.com/services/v2/songs/{song_id}/arrangements?include=keys"
    arrangement_response = requests.get(arrangement_url, headers=headers)
    arrangement_data = arrangement_response.json()

    arrangements = []
    for arrangement in arrangement_data['data']:
        arrangement_id = arrangement['id']
        arrangement_name = arrangement['attributes']['name']
        arrangement_keys = []
        
        for key_relation in arrangement['relationships']['keys']['data']:
            key_id = key_relation['id']
            key_url = f"https://api.planningcenteronline.com/services/v2/songs/{song_id}/arrangements/{arrangement_id}/keys/{key_id}"
            key_response = requests.get(key_url, headers=headers)
            key_data = key_response.json()
            
            key_attributes = key_data['data']['attributes']
            starting_key = key_attributes['starting_key']
            ending_key = key_attributes['ending_key']
            starting_minor = key_attributes['starting_minor']
            ending_minor = key_attributes['ending_minor']
            
            arrangement_keys.append({
                'key_id': key_id,
                'starting_key': starting_key,
                'ending_key': ending_key,
                'starting_minor': starting_minor,
                'ending_minor': ending_minor
            })
        
        arrangements.append({
            'id': arrangement_id,
            'name': arrangement_name,
            'keys': arrangement_keys
        })

    song_arrangement_map[song_title] = arrangements

# Prettified output using json.dumps()
prettified_output = json.dumps(song_arrangement_map, indent=2)
print(prettified_output)

# Retrieve the ID for the "Fancy" arrangement of "As The Deer"
song_title = "As The Deer"
arrangement_name = "Fancy"
fancy_arrangement_id = None

for song_data in song_arrangement_map[song_title]:
    if song_data["name"] == arrangement_name:
        fancy_arrangement_id = song_data["id"]
        break

print("Fancy arrangement ID:", fancy_arrangement_id)