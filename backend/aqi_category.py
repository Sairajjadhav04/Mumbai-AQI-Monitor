def get_aqi_category(aqi):
    aqi = int(aqi)
    if aqi <=50 :
        return "Good"
    elif aqi > 50 and aqi <=100:
        return "Satisfactory"
    elif aqi >100 and aqi <= 200:
        return "Moderate"
    elif aqi >200 and aqi <= 300 :
        return "Poor"
    elif aqi >300 and aqi <= 400 :
        return "Very Poor"
    elif aqi >400 and aqi <=500 :
        return "Severe"
    else:
        return "beyond AQI scale"