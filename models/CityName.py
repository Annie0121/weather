import json
import os

current_dir = os.path.dirname(__file__)
city_towns_file = os.path.join(current_dir, '..', 'docs', 'city_towns.json')
with open(city_towns_file, 'r', encoding='utf-8') as f:
  city_towns = json.load(f)

class CityName:

  @staticmethod
  def get_city_names():
    return list(city_towns.keys())

  @staticmethod
  def get_towns(city_name):
    try:
      return city_towns[city_name]
    except KeyError:
      return []


aaa = CityName.get_city_names()
print(aaa)