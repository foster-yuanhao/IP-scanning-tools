import requests


def getname(mac):
	url = "https://mac-address-lookup1.p.rapidapi.com/static_rapid/mac_lookup/"
	querystring = {"query": mac}
	headers = {
		"X-RapidAPI-Key": "506d86e23dmsh13333778ed1a51fp16afbfjsnf8eb6dbe2fd8",
		"X-RapidAPI-Host": "mac-address-lookup1.p.rapidapi.com"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return response.text
