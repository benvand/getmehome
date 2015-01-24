import requests
__author__ = 'benvandersteen'
DIR_API_KEY = 'AIzaSyDbAut7LmWCtUQ-OmLETLRdZYqrCZ89g7k'
GEOCODE_API_KEY = 'AIzaSyAGF5TboOh6h5t5q0ZN5HU2ouBawx9cgEk'

#TODO hacky url builders

class OverQueryLimit(Exception):
    def __str__(self):
        return 'You have exceeded your daily request quota for the Google reverse geocode api. :/'

def directions_map_url(points):
    if len(points) > 20:
        points = points[::len(points)/18]
    a, b = points.pop(0), points.pop(-1)
    base = '''https://www.google.com/maps/embed/v1/directions'''
    key = '?key=%s' % DIR_API_KEY
    mode = 'mode=bicycling'
    units = 'units=metric'
    origin = 'origin='+formatted_address_for_api_request(*a)
    destination = 'destination='+formatted_address_for_api_request(*b)
    waypoints = 'waypoints=' +'|'.join([formatted_address_for_api_request(*i) for i in points])
    return base + '&'.join([key, mode, units, origin, destination, waypoints])


def geocode_url(lat, long):
    base = '''https://maps.googleapis.com/maps/api/geocode/json?'''
    key= 'key=%s' % GEOCODE_API_KEY
    latlong= 'latlng=' + ','.join([lat,long])
    result = '''result_type=street_address'''
    return base + '&'.join([latlong, result, key])



def address_dict_from_lat_long(lat, long):
    #TODO lol at this
    r = requests.get(geocode_url(lat, long)).json()
    if r['status'] == 'OVER_QUERY_LIMIT':
        raise OverQueryLimit
    return {i['types'][0]: i['long_name'] for i in r['results'][0]['address_components'] if i.has_key('types')}

def postcode_from_lat_long(lat, long):
    return address_dict_from_lat_long['postal_code']

def formatted_address_for_api_request(lat, long):
    ad = address_dict_from_lat_long(lat, long)
    return ','.join([i.replace(' ','+') for i in ad.values()])

