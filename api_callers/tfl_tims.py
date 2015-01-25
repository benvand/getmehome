import keys
import requests

from xml.dom import minidom
import xml.etree.ElementTree as ET

response = requests.get('http://data.tfl.gov.uk/tfl/syndication/feeds/tims_feed.xml?app_id=%s&app_key=%s' % (keys.TFL_APP_ID, keys.TFL_APP_KEY))

def get_tims_data():
    global response
    # response = response # requests.get('http://data.tfl.gov.uk/tfl/syndication/feeds/tims_feed.xml?app_id=%s&app_key=%s' % (keys.TFL_APP_ID, keys.TFL_APP_KEY))
    tree = ET.fromstring(response.content)
    tree = minidom.parseString(response.content)

    return tree


#from api_callers.tfl_tims import get_tims_accidents_ll
#TODO extrapolate
#TODO minimise api calls
def get_tims_accidents_ll():
    xml = get_tims_data()
    active_dis = [i for i in xml.getElementsByTagName('Disruption') if i.getElementsByTagName('status')[0].firstChild.wholeText == 'Active']
    active_crash_dis  = [i for i in active_dis if i.getElementsByTagName('category')[0].firstChild.wholeText == 'Traffic Incidents']
    #TODO enough of the bs list comprehentions
    slist= [i.getElementsByTagName('coordinatesLL')[1].firstChild.wholeText.split(',') for i in active_crash_dis]
    return [[(float(i[0]),float(i[1])), (float(i[2]),float(i[3]))] for i in slist]

def get_tims_traffic_ll():
    xml = get_tims_data()
    active_dis = [i for i in xml.getElementsByTagName('Disruption') if i.getElementsByTagName('status')[0].firstChild.wholeText == 'Active']
    active_crash_dis  = [i for i in active_dis if i.getElementsByTagName('category')[0].firstChild.wholeText == 'Traffic Volume']
    #TODO enough of the bs list comprehentions
    slist = [i.getElementsByTagName('coordinatesLL')[1].firstChild.wholeText.split(',') for i in active_crash_dis]
    return [[(float(i[0]),float(i[1])), (float(i[2]),float(i[3]))] for i in slist]
