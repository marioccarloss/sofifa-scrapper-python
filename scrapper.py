import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv, json

def get_data():
	url = "https://sofifa.com/players?type=all&tm%5B0%5D=243&offset="
	soup = BeautifulSoup(requests.get(url).content, "html.parser")

	rv = []
	for row in soup.select("tbody tr"):
		id_ = row.select_one("img[id]")["id"]
		name = row.select_one(".col-name").get_text(strip=True)
		age = row.select_one(".col-ae").get_text(strip=True)
		positions = [p.get_text(strip=True) for p in row.select("span.pos")]
		nationality = row.select_one("img.flag")["title"]
		overall = row.select_one(".col-oa").get_text(strip=True)
		potential = row.select_one(".col-pt").get_text(strip=True)
		club = row.select_one(".col-name > div > a").get_text(strip=True)

		# sometimes there isn't any club, just country:
		if club == "":
			club = row.select_one(".col-name > div > a")["title"]

		value = row.select_one(".col-vl").get_text(strip=True)
		wage = row.select_one(".col-wg").get_text(strip=True)
		rv.append(
			[
				id_,
				name,
				age,
				", ".join(positions),
				nationality,
				overall,
				potential,
				club,
				value,
				wage,
			]
		)

	return rv

all_data = []
for offset in range(0, 1):  # <--- increase offset here
	print("Offset {}...".format(offset))
	all_data.extend(get_data())

df = pd.DataFrame(
	all_data,
	columns=[
		"ID",
		"Name",
		"Age",
		"Positions",
		"Nationality",
		"Overall",
		"Potential",
		"Club",
		"Value",
		"Wage",
	],
)

print(df)
df.to_csv("data.csv", index=False)

# Now convert to json
csvFilePath = 'data.csv'
jsonFilePath = 'data.json'

data = {}

with open(csvFilePath) as csvFile:
	csvReader = csv.DictReader(csvFile)
	for rows in csvReader:
		id = rows['ID']
		data[id] = rows
# create new json file and write data to it
with open(jsonFilePath, 'w') as jsonFile:
	jsonFile.write(json.dumps(data, indent=2))
