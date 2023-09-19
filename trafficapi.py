import requests

url = "https://waze.p.rapidapi.com/alerts-and-jams"

querystring = {"bottom_left":"53.8014739 -1.5465407","top_right":"53.7925515 -1.7580275","max_alerts":"20","max_jams":"20"}

headers = {
	"X-RapidAPI-Key": "8f4903e1a3mshf8781849e3ccaaep1cdf5cjsn9944317a9d62",
	"X-RapidAPI-Host": "waze.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())