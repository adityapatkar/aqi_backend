import requests
import pandas as pd
from prophet.serialize import model_to_json, model_from_json
from prophet import Prophet
import json
from env import url, city, state
from database import insert_prediction


def predict_future(periods=48):
    with open('serialized_model.json', 'r') as fin:
        m = model_from_json(json.load(fin))
    future = m.make_future_dataframe(periods=periods, freq='h')
    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    #return future data for given period
    return forecast.tail(periods)


def fit_new_model():
    response = requests.get(f"{url}/retrieve",
                            params={
                                'city': "Mumbai",
                                'state': "Maharashtra"
                            })
    response = response.json()
    if response is not None:
        aqi = []
        date_time = []
        for data in response['data']:
            aqi.append(data['aqi'])
            date_time.append(data['datetime'])

        #convert the lists to pandas dataframe
        df = pd.DataFrame(list(zip(date_time, aqi)), columns=['ds', 'y'])
        #convert the date_time column to datetime
        df['ds'] = pd.to_datetime(df['ds'])
        m = Prophet(changepoint_prior_scale=0.01)
        print("Done")
        model = m.fit(df)
        #delete the old model file
        with open('serialized_model.json', 'w') as fout:

            json.dump(model_to_json(m), fout)  # Save model
            print("Saved successfully")
        #calculate error
        forecast = predict_future(periods=48)
        forecast = forecast[['ds', 'yhat']]
        forecast = forecast.rename(columns={'ds': 'datetime'})
        forecast['city'] = city
        forecast['state'] = state
        #convert to list of dictionaries
        forecast = forecast.to_dict('records')
        print(forecast)
        #insert into database
        insert_prediction(forecast)
        return 0
    return None