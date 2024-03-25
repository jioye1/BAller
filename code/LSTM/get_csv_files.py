from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

url = "https://fbref.com/en/comps/Big5/2022-2023/stats/players/2022-2023-Big-5-European-Leagues-Stats"
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

else:
    print(f"\n{response.status_code}")

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find("table", {"id": "stats_standard"})

# Extract data from the table using Pandas
if table:
    df = pd.read_html(str(table))[0]
    print("Table extracted successfully:")
    df.to_csv("2022-2023.csv", index=False)
    # print(df)

    # Save the DataFrame to a CSV file
    # df.to_csv("table_data.csv", index=False)
    # print("Data saved to 'table_data.csv' successfully.")
else:
    print("Table not found with the specified ID.")
