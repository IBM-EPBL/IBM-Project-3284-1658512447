import requests

url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"

querystring = {"ingr":"1 large apple"}

headers = {
	"X-RapidAPI-Key": "2c95ef2556msh5cb6a650ce3f37ep1c3100jsn7da8f1761eee",
	"X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
