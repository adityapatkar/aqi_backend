from prophet.serialize import model_from_json
import prophet
import json
with open('serialized_model.json', 'r') as fin:
    m = model_from_json(json.load(fin))  # Load model


def predict_future(periods):
    future = m.make_future_dataframe(periods=periods, freq='h')
    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    #return future data for given period
    return forecast.tail(periods)