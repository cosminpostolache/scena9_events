import requests

url = "https://fgestrapi.filarmonicaenescu.ro/api/events"

params = {
   # "populate[0]": "media",
   # "sort[0]": "endDateAndTime:asc",
   #"locale": "ro",
    #"pagination[page]": 1,
    "pagination[pageSize]": 10
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://filarmonicaenescu.ro/",
    "Origin": "https://filarmonicaenescu.ro",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Bearer 0443569bc94038f8aaa3e17cbd634d89b18536c71aafb14ed1ad61f8550b7ef4abd03ffa1bc139aece82ce77801493aa15c1e5b2ee0c61264da873b08e40e8bebfde46d319ab07b868cfcb61c1745372bf217536214f41cb5de295cbab75624ba397659345f48895536ee74086eac12382fec094ea6cf4806cec59e2e9cdb071"
}

response = requests.get(url, params=params)

data = response.json()
print(data)
print(data.keys())
#for event in data["data"]:
  #  print(event.keys())