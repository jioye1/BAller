from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time
import json
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

all_player_names_url = "https://fbref.com/en/comps/9/2022-2023/wages/2022-2023-Premier-League-Wages"

response = requests.get(all_player_names_url)

if response.status_code == 200:
    html_content = response.text

else:
    print(f"\n SERVER RESPONSE: {response.status_code}")
    print(f"RETRY AFTER: {response.headers.get('Retry-After')}")

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a')

pattern = r"^/en/players/[a-zA-Z0-9]+"

player_count = 0
saved_links = []
for link in links:
	href = link.get('href')
	if href is not None and re.search(pattern, href) and ('<img class="poptip"' not in href):
	    if link.find_parents('div', id='footer'):
	        continue
	    if link.find_parents('div', id='meta'):
	    	continue
	    else:
	    	player_count += 1
	    	s1, s2 = href.rsplit('/', 1)
	    	saved_links.append(f"https://fbref.com{s1}/matchlogs/2022-2023/{s2}-Match-Logs")
	    	#print(f"https://fbref.com{s1}/matchlogs/2022-2023/{s2}-Match-Logs")

# print(f"\n PLAYER COUNT: {player_count}")
#print(saved_links)

prem_2022_2023_match_dictionary = {}

break_count = 0
for link in saved_links:
	
	s1, s2 = link.rsplit('/', 1)

	current_name = s2[:-11]

	prem_2022_2023_match_dictionary[current_name] = []
	print(f"Starting to fill the match stats for: {current_name} ...")

	current_link = link

	time.sleep(3.2)
	response = requests.get(current_link)

	if response.status_code == 200:
		html_content = response.text

	else:
	    print(f"\n ERROR | SERVER RESPONSE: {response.status_code}")
	    sys.exit()


	soup = BeautifulSoup(html_content, 'html.parser')

	table = soup.find("table", {"id": "matchlogs_all"})

	if table:
		df = pd.read_html(str(table))[0]
		#print(df)
		for index, row in df.iterrows():
			if row.iloc[2] == "Premier League":
				prem_2022_2023_match_dictionary[current_name].append([row.iloc[i] for i in range(3, len(row)-1)])
			else:
				continue
		print(f"Done.")
		print("========================================================\n")


		break_count += 1

	'''if break_count == 1:
		break'''

#print(prem_2022_2023_match_dictionary)
with open('raw_prem_dictionary.json', 'w') as f:
    json.dump(prem_2022_2023_match_dictionary, f)
