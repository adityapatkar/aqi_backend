
from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from datetime import datetime
from scrape_aqi import scrape_real_time_aqi

app = Flask(__name__)
Swagger(app)

@app.route('/')
def home():
    return redirect('/apidocs')

@app.route('/aqi', methods=['GET'])
def aqi():
    """Example endpoint returning a random number
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
    responses:
        200:
            description: Aqi
    """
    try:
        try:
            city = request.args.get("city")
        except:
            return jsonify({"error": "city not found"}), 400
        try:
            aqi = scrape_real_time_aqi(city)
            if aqi == -1:
                return jsonify({"error": "no info about current aqi found"}), 404
        except:
            return jsonify({"error": "no info about current aqi found"}), 404
        datetime_now = datetime.now()
        return jsonify({"aqi": aqi, "datetime": datetime_now.strftime("%d/%m/%Y %H:%M:%S")}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "something went wrong."}), 500



if __name__ == '__main__':
    app.run(debug=True)
    
