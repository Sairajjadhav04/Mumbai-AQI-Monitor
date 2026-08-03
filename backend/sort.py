def sort_by_aqi(aqi_data):
    data = aqi_data.copy()
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if int(data[j]["aqi"]) > int(data[j + 1]["aqi"]):
                data[j], data[j + 1] = data[j + 1], data[j] 
    return data