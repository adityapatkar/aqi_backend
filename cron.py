import requests
from env import city, state, url

response = requests.get(url + "api", params={"city": city, "state": state})
if response.status_code == 200:
    print("Successfully fetched data")
    response = response.json()
    aqi = response["aqi"]
    city = response["city"]
    state = response["state"]
    date_time = response["date_time"]

    #insert into database
    response = requests.post(url + "insert",
                             params={
                                 "city": city,
                                 "state": state,
                                 "aqi": aqi,
                                 "datetime": date_time
                             })
else:
    print("Error in fetching data")
