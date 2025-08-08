import joblib
import numpy as np
from config.base_config import get_config
from flask import Flask, render_template, request

config = get_config()
paths = config.paths

app = Flask(__name__)

loaded_model = joblib.load(paths.model_output_filepath)

@app.route("/", methods=["POST", "GET"])
def index():
    if "POST" == request.method:
        lead_time = int(request.form["lead_time"])
        no_of_special_requests = int(request.form["no_of_special_requests"])
        avg_price_per_room = float(request.form["avg_price_per_room"])
        arrival_month = int(request.form["arrival_month"])
        arrival_date = int(request.form["arrival_date"])
        market_segment_type = int(request.form["market_segment_type"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
        type_of_meal_plan = int(request.form["type_of_meal_plan"])
        room_type_reserved = int(request.form["room_type_reserved"])

        features = np.array([[lead_time, no_of_special_requests, avg_price_per_room, 
                              arrival_month, arrival_date, market_segment_type, no_of_week_nights, 
                              no_of_weekend_nights, type_of_meal_plan, room_type_reserved]])
        
        prediction = loaded_model.predict(features)

        return render_template("index.html", prediction = prediction[0])
    
    return render_template("index.html", predition=None)

if "__main__" == __name__:
    app.run(host=str(config.application.host), port=config.application.port, debug=config.application.debug)
