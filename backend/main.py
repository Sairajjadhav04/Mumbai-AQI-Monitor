import csv
from aqi_category import get_aqi_category
from sort import sort_by_aqi
def load_aqi_data():
    file_path = "backend/data/aqi_data.csv"
    aqi_data = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            aqi_data.append(row)
    return aqi_data
aqi_data = load_aqi_data()

def aqi_location(aqi_data) :
    #Take the location and Station from the user 
    station = input("Enter the Station name : ")
    #For searching the data 
    f = False 
    for data in aqi_data : 
        if((data["station"].lower()==station.lower())):
            category = get_aqi_category(data["aqi"])
            print("\t\nAQI details as follows\n")
            print("City : ",data["city"])
            print("Station : ",data["station"])
            print("AQI :", data["aqi"])
            print("PM25 :", data["pm25"])
            print("PM10 :", data["pm10"])
            print("SO2 :", data["so2"])
            print("NO2 :", data["no2"])
            print("CO :", data["co"])
            print("O3 :", data["o3"])
            print("NH3 :", data["nh3"])
            print("Category : ",category)
            f = True 
            break 
    if not f :
        print("\n Station not found for your location !!!")

def show_all_stations(aqi_data):
    print("\n\t MUMBAI AQI STATIONS \n")
    for data in aqi_data:
        category = get_aqi_category(data["aqi"])
        print("\t\nAQI details as follows\n")
        print("City : ",data["city"])
        print("Station : ",data["station"])
        print("AQI :", data["aqi"])
        print("PM25 :", data["pm25"])
        print("PM10 :", data["pm10"])
        print("SO2 :", data["so2"])
        print("NO2 :", data["no2"])
        print("CO :", data["co"])
        print("O3 :", data["o3"])
        print("NH3 :", data["nh3"])
        print("Category : ",category)

def highest_aqi(aqi_data):
    sorted_data = sort_by_aqi(aqi_data)
    highest = sorted_data[-1]
    category = get_aqi_category(highest["aqi"])
    print("\t\nAQI details as follows\n")
    print("City : ",highest["city"])
    print("Station : ",highest["station"])
    print("PM25 :", highest["pm25"])
    print("PM10 :", highest["pm10"])
    print("AQI :", highest["aqi"])
    print("SO2 :", highest["so2"])
    print("NO2 :", highest["no2"])
    print("CO :", highest["co"])
    print("O3 :", highest["o3"])
    print("NH3 :", highest["nh3"])
    print("Category : ",category)

def show_lowest_aqi(aqi_data):
    sorted_data = sort_by_aqi(aqi_data)
    lowest = sorted_data[0]
    category = get_aqi_category(lowest["aqi"])
    print("\t\nAQI details as follows\n")
    print("City : ",lowest["city"])
    print("Station : ",lowest["station"])
    print("PM25 :", lowest["pm25"])
    print("PM10 :", lowest["pm10"])
    print("AQI :", lowest["aqi"])
    print("SO2 :", lowest["so2"])
    print("NO2 :", lowest["no2"])
    print("CO :", lowest["co"])
    print("O3 :", lowest["o3"])
    print("NH3 :", lowest["nh3"])
    print("Category : ",category)

def main():
    aqi_data = load_aqi_data()
    while True:
        print("\n")
        print("\t\tMUMBAI AQI MONITOR\n")
        print("1. Search AQI by Location and Station")
        print("2. Show All Stations")
        print("3. Show Highest AQI")
        print("4. Show Lowest AQI")
        print("5. Exit\n")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            aqi_location(aqi_data)
        elif choice == "2":
            show_all_stations(aqi_data)
        elif choice == "3":
            highest_aqi(aqi_data)
        elif choice == "4":
            show_lowest_aqi(aqi_data)
        elif choice == "5":
            print("\nThank you for using Mumbai AQI Monitor!")
            break
        else:
            print("\nInvalid choice. Please enter 1 to 5.")
main()