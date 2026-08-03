# Mumbai AQI Monitor 🌫️

Mumbai AQI Monitor is a Python-based application that allows users to search and analyze Air Quality Index (AQI) data for different monitoring stations in Mumbai.

## Features

- Search AQI using station name
- Display highest AQI
- Display lowest AQI
- Classify AQI into different categories
- Store AQI data using CSV
- Menu-based Python application

## AQI Categories

| AQI Range | Category |
|-----------|----------|
| 0 - 50 | Good |
| 51 - 100 | Satisfactory |
| 101 - 200 | Moderate |
| 201 - 300 | Poor |
| 301 - 400 | Very Poor |
| 401 - 500 | Severe |

## Technologies Used

- Python
- CSV
- File Handling
- Functions
- Lists
- Dictionaries

## Project Structure

```text
Mumbai-AQI-Monitor/
│
├── backend/
│   ├── main.py
│   ├── aqi_category.py
│   │
│   └── data/
│       └── aqi_data.csv
│
├── README.md
├── requirements.txt
└── .gitignore
