import requests

url = "https://waze.p.rapidapi.com/alerts-and-jams"

querystring = {"bottom_left":"40.66615391742187,-74.13732147216798","top_right":"40.772787404902594,-73.76818084716798","max_alerts":"20","max_jams":"20"}

headers = {
	"X-RapidAPI-Key": "8f4903e1a3mshf8781849e3ccaaep1cdf5cjsn9944317a9d62",
	"X-RapidAPI-Host": "waze.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())