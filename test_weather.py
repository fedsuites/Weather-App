import pytest
from datetime import datetime
import builtins
import csv
import unittest
import weather
import requests
from unittest.mock import patch,MagicMock
from weather import get_city,parse_weather,fetch_weather,locations,API_KEY,load_locations,save_locations


def test_parse_weather_valid_data():
    mock_data={  
        "cod": 200,
        "name": "Lagos",
        "sys": {"country": "NG", "sunrise": 1697100000, "sunset": 1697143200},
        "main": {"temp": 30.5, "feels_like": 32.0, "temp_min": 28.0, "temp_max": 33.0, "humidity": 65},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 2.5}
    }
    result= parse_weather(mock_data)
    assert result is not None
    assert result["city"]=="Lagos"
    assert result["temperature"]==30.5
    assert result["humidity"]==65
    assert result["country"]=="NG"
    assert result["condition"]=="Clear Sky"

    assert isinstance(result["sunrise"], str)
    assert ":" in result["sunrise"]

def test_parse_weather_invalid_data(capsys):
    invalid_data={
        "cod":"404", "message":"city not found"
    }
    result= parse_weather(invalid_data)
    captured= capsys.readouterr()

    assert result is None
    assert "Location not found, please try again" in captured.out

def test_parse_weather_incomplete_keys():
    incomplete_data={
        "cod":"200", "name":"Lagos"
    }
    with pytest.raises(KeyError):
        parse_weather(incomplete_data)

def test_fetch_weather():
    mock_data={"cod":"200","name":"Lagos"}
    location="Lagos"
    expected_url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={location}"
        f"&appid={API_KEY}&units=metric"
    )
    with patch("weather.requests.get") as mock_get:
       
        mock_response=MagicMock()
        mock_response.json.return_value=mock_data
        mock_get.return_value=mock_response

        result=fetch_weather(location)
        mock_get.assert_called_once_with(expected_url)
        assert result==mock_data

def test_fetch_weather_error(capsys):
    with patch("weather.requests.get", side_effect=requests.exceptions.RequestException):
        location="Lagos"

        result= fetch_weather(location)
        captured= capsys.readouterr()

        assert result is None
        assert "Unable to fetch weather, check your internet connection" in captured.out

def test_load_location(tmp_path):
    test_csv= tmp_path / "weather.csv"
 

    with open(test_csv, "w", newline="") as file:
        writer= csv.DictWriter(file,fieldnames=["Locations"])
        writer.writeheader()
        writer.writerow({"Locations":"Lagos"})
        writer.writerow({"Locations":"Ibadan"})
        
    weather.filename=test_csv

    result=weather.load_locations()
        
    assert len(result)==2
    assert result[0]["Locations"]=="Lagos"
        
def test_empty_csv(tmp_path):
    test_csv=tmp_path/ "location.csv"

    weather.filename=test_csv
    result=weather.load_locations()
 
    assert result==[]

def test_save_locations(tmp_path):
    test_csv=tmp_path / "location.csv"
    weather.filename= test_csv
    
    weather.save_locations("Lagos")

    with open(test_csv, "r", newline="") as file:
        reader= csv.DictReader(file)
        rows= list(reader)
    
    assert len(rows)==1
    assert rows[0]["Locations"]=="Lagos"

def test_save_existing_location(tmp_path,capsys):
    test_csv= tmp_path / "locations.csv"

    weather.filename=test_csv

    with open(test_csv, "w", newline="") as file:
        writer= csv.DictWriter(file, fieldnames=["Locations"])
        writer.writeheader()
        writer.writerow({"Locations":"Lagos"})

    weather.save_locations("Lagos")

    with open(test_csv, "r", newline="") as file:
        reader= csv.DictReader(file)
        rows= list(reader)
    
    captured= capsys.readouterr()
    assert "You already saved this location. Try searching for another one instead." in captured.out
    assert len(rows)==1
    assert rows[0]["Locations"]=="Lagos"
    

def test_get_city():
    mock_api_response = {"cod": "200", "name":"Lagos"}
    mock_parsed_weather={  
        "cod": 200,
        "name": "Lagos",
        "sys": {"country": "NG", "sunrise": 1697100000, "sunset": 1697143200},
        "main": {"temp": 30.5, "feels_like": 32.0, "temp_min": 28.0, "temp_max": 33.0, "humidity": 65},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 2.5}
    }

    inputs=["Lagos","yes","no"]

    with(
        patch("weather.input",side_effect=inputs),
        patch("weather.load_locations", return_value=[]),
        patch("weather.fetch_weather" , return_value=mock_api_response) as mock_fetch,
        patch("weather.parse_weather", return_value=mock_parsed_weather) as mock_parse,
        patch("weather.display_weather" ) as mock_display,
        patch("weather.save_locations") as mock_save
    ):
        result=get_city()

        mock_fetch.assert_called_once_with("Lagos")
        mock_parse.assert_called_once_with(mock_api_response)
        mock_display.assert_called_once_with(mock_parsed_weather)
        mock_save.assert_called_once_with("Lagos")
        
        assert result=="Lagos"

def test_get_city_invalid_location_(capsys):
    inputs=["Gbengbeleku","no"]
    mock_api_response={"cod": "404", "message": "city not found"}

    with (
        patch("weather.input", side_effect=inputs),
        patch("weather.load_locations", return_value=[]),
        patch("weather.fetch_weather", return_value=mock_api_response),
        patch("weather.display_weather") as mock_display,
        patch("weather.save_locations") as mock_save,
    ):
        result=get_city()

        captured=capsys.readouterr()

        assert "❌ Location not found. Please try again." in captured.out
        mock_display.assert_not_called()
        mock_save.assert_not_called()
        assert result == "Gbengbeleku"

def test_get_city_no_save():
    inputs=["Lagos","no","no"]
    mock_api_response = {"cod": "200", "name": "Lagos"}
    mock_parsed_weather={  
        "cod": 200,
        "name": "Lagos",
        "sys": {"country": "NG", "sunrise": 1697100000, "sunset": 1697143200},
        "main": {"temp": 30.5, "feels_like": 32.0, "temp_min": 28.0, "temp_max": 33.0, "humidity": 65},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 2.5}
    }
    with(
        patch("weather.input",side_effect=inputs),
        patch("weather.load_locations", return_value=[]),
        patch("weather.fetch_weather" , return_value=mock_api_response) as mock_fetch,
        patch("weather.parse_weather", return_value=mock_parsed_weather) as mock_parse,
        patch("weather.display_weather" ) as mock_display,
        patch("weather.save_locations") as mock_save
    ):
        result=get_city()

        mock_fetch.assert_called_once_with("Lagos")
        mock_parse.assert_called_once_with(mock_api_response)
        mock_display.assert_called_once_with(mock_parsed_weather)
        mock_save.assert_not_called()

        assert result=="Lagos"
