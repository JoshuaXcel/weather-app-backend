import json
import csv
import io
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from models import WeatherRecord


def record_to_dict(record: WeatherRecord) -> dict:
    #Converts a SQLAlchemy record into a plain dict, safe for any export format
    return {
        "id": record.id,
        "location_input": record.location_input,
        "resolved_name": record.resolved_name,
        "latitude": record.latitude,
        "longitude": record.longitude,
        "start_date": record.start_date.isoformat(),
        "end_date": record.end_date.isoformat(),
        "weather_data": record.weather_data,
        "created_at": record.created_at.isoformat(),
        "updated_at": record.updated_at.isoformat()
    }


def export_as_json(record: WeatherRecord) -> str:
    return json.dumps(record_to_dict(record), indent=2)


def export_as_csv(record: WeatherRecord) -> str:
    #One row per day of weather data, with location info repeated per row
    data = record_to_dict(record)
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["id", "resolved_name", "latitude", "longitude", "date", "temp_max", "temp_min"])

    for day in data["weather_data"]:
        writer.writerow([
            data["id"], data["resolved_name"], data["latitude"], data["longitude"],
            day["date"], day["temp_max"], day["temp_min"]
        ])

    return output.getvalue()


def export_as_xml(record: WeatherRecord) -> str:
    data = record_to_dict(record)

    root = Element("WeatherRecord")
    SubElement(root, "id").text = str(data["id"])
    SubElement(root, "location_input").text = data["location_input"]
    SubElement(root, "resolved_name").text = data["resolved_name"]
    SubElement(root, "latitude").text = data["latitude"]
    SubElement(root, "longitude").text = data["longitude"]
    SubElement(root, "start_date").text = data["start_date"]
    SubElement(root, "end_date").text = data["end_date"]

    daily = SubElement(root, "weather_data")
    for day in data["weather_data"]:
        entry = SubElement(daily, "day")
        SubElement(entry, "date").text = day["date"]
        SubElement(entry, "temp_max").text = str(day["temp_max"])
        SubElement(entry, "temp_min").text = str(day["temp_min"])

    rough_xml = tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")

    return pretty_xml