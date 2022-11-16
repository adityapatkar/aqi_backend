
from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from datetime import datetime
from scrape_aqi import scrape_real_time_aqi
from database import insert, retrieve

app = Flask(__name__)
Swagger(app)

@app.route('/')
def home():
    return redirect('/apidocs')

@app.route('/aqi', methods=['GET'])
def aqi():
    """Example endpoint returning the aqi of a city
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
      - name: state
        in: query
        type: string
        required: true
    responses:
        200:
            description: Aqi
        400:
            description: Bad Request
        404:
            description: Not Found
        500:
            description: Internal Server Error
    """
    try:
        try:
            #get city and state
            city = request.args.get('city')
            state = request.args.get('state')
            state = state.replace(" ", "-")
            city = city.replace(" ", "-")
        except:
            return jsonify({"error": "city not found"}), 400
        try:
            aqi = scrape_real_time_aqi(city, state)
            if aqi == -1:
                return jsonify({"error": "not found", "message": "No info about current api found", "code": "FAILURE"}), 404
        except:
            return jsonify({"message": "no info about current aqi found", "error": "not found", "code": "FAILURE"}), 404
        datetime_now = datetime.now()
        return jsonify({"aqi": aqi, "datetime": datetime_now.strftime("%d/%m/%Y %H:%M:%S"), "message": "Real Time AQI Retrieved Successfully", "code": "SUCCESS", "city": city.lower(), "state":state.lower()}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "something went wrong.", "error": "internal server error", "code":"FAILURE"}), 500

@app.route('/insert', methods=['POST'])
def insert_aqi():
    '''
    Example endpoint to insert aqi data
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
      - name: state
        in: query
        type: string
        required: true
      - name: aqi
        in: query
        type: string
        required: true
      - name: datetime
        in: query
        type: string
        required: true
    responses:
        200:
            description: AQI Inserted Successfully
    '''
    try:
        city = request.args.get('city')
        state = request.args.get('state')
        aqi = float(request.args.get('aqi'))
        datetime = request.args.get('datetime') 
        if city is None or state is None or aqi is None or datetime is None:
            return jsonify({"message": "missing parameters", "error": "bad request", "code": "FAILURE"}), 400
        data = {
            "city": city.lower(),
            "state": state.lower(),
            "aqi": aqi,
            "datetime": datetime
        }
        success, error = insert(data)
        if success:
            return jsonify({"message": "data inserted successfully", "code": "SUCCESS"}), 200
        else:
            return jsonify({"message": f"{error} not found", "error": "bad request", "code": "FAILURE"}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": "something went wrong.", "error": "internal server error", "code":"FAILURE"}), 500

@app.route('/retrieve', methods=['GET'])
def retrieve_aqi():
    '''
    Example endpoint to retrieve aqi data
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
      - name: state
        in: query
        type: string
        required: true
    responses:
        200:
            description: AQI Retrieved Successfully
    '''
    try:
        city = request.args.get('city')
        state = request.args.get('state')
        if city is None or state is None:
            return jsonify({"message": "missing parameters", "error": "bad request", "code": "FAILURE"}), 400
        city = city.replace(" ", "-")
        state = state.replace(" ", "-")
        data = retrieve(city, state)
        
        if data is None:
            return jsonify({"message": "no data found", "error": "not found", "code": "FAILURE"}), 404

        return jsonify({"data": data, "message": "data retrieved successfully", "code": "SUCCESS"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "something went wrong.", "error": "internal server error", "code":"FAILURE"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
