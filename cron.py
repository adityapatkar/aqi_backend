import requests
from env import city, state, url

response = requests.get(url + f"aqi?city={city}&state={state}")
if response.status_code == 200:
    print("Successfully fetched data")
    response = response.json()
    aqi = response["aqi"]
    city = response["city"]
    state = response["state"]
    date_time = response["datetime"]

    #insert into database
    response = requests.post(url + "insert",
                             params={
                                 "city": city,
                                 "state": state,
                                 "aqi": aqi,
                                 "datetime": date_time
                             })
    print(response.json())
else:
    print("Error in fetching data")
    print(response)
