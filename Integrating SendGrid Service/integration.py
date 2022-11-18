import requests

url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/alerts/%7Balert_id%7D"

payload = {
	"type": "stats_notification",
	"email_to": "example@test.com",
	"frequency": "daily"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "2c95ef2556msh5cb6a650ce3f37ep1c3100jsn7da8f1761eee",
	"X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
}

response = requests.request("PATCH", url, json=payload, headers=headers)

print(response.text)
