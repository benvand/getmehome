from xml.parsers.expat import ExpatError

import gpxpy
from django.db import models
from django.conf import settings


from api_callers.googlemaps import directions_map_url, postcode_from_lat_long
from api_callers.googlemaps import OverQueryLimit
from api_callers.tfl_tims import get_tims_accidents_ll, get_tims_traffic_ll

import decimal

def twodp(num):
    return decimal.Decimal(str(num)).quantize(decimal.Decimal('0.00'))



class RouteGroup(models.Model):
    created = models.DateTimeField(auto_now_add=True,)
    edited = models.DateTimeField(auto_now=True,)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    embarkation = models.CharField(max_length=255, null = True, blank=True)
    destination = models.CharField(max_length=255, null = True, blank=True)



    def __str__(self):
        if self.embarkation and self.destination:
            return self.embarkation.capitalize() + ' > ' + self.destination.capitalize()
        return self.title

    class Meta:
        ordering = ['-created']


class Route(models.Model):
    route_group = models.ForeignKey(RouteGroup)
    created = models.DateTimeField(auto_now_add=True,)
    edited = models.DateTimeField(auto_now=True,)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.CharField(max_length=10000, null = True, blank=True)
    route_gpx_xml = models.TextField()


    def check_gpx(self):
        try:
            return self.get_gpx()
        except (gpxpy.gpx.GPXXMLSyntaxException, ExpatError) as e:
            return False

    #TODO cached_property please
    def get_gpx(self):
        if not hasattr(self, 'gpx'):
            self.gpx = gpxpy.parse(self.route_gpx_xml)
        return self.gpx

    def get_gpx_points(self):
        gpx = self.get_gpx()
        points = [[str(i[0].latitude), str(i[0].longitude)] for i in gpx.walk()]
        return [(float(i[0]),float(i[1])) for i in points]


    #TODO datetime me please
    def get_time_kmh(self):
        return twodp((self.length/1000)/settings.ROUTE_CONTSTANT_SPEED)

    def get_time(self):
        #TODO default get_time
        #Have user option for kmh/ mph and pick method to calc time based on that
        #Do that logic here
        return self.get_time_kmh()

    #TODO cached_property
    @property
    def length(self):
        gpx = self.get_gpx()
        return gpx.length_3d()

    def points_vs_trouble(self, points, coords):
        for point in points:
            for trouble in incident_coords:
                if trouble[1][0]< point[1] < trouble[0][0] and \
                        trouble[0][1]< point[0] < trouble[1][1]:
                    return True
        return False

    #TODO extrapolate

    def get_incident(self):
        points=self.get_gpx_points()
        incident_coords = get_tims_accidents_ll()
        return self.points_vs_trouble(self, points, incident_coords)




    def get_traffic(self):
        points=self.get_gpx_points()
        traffic_coords = get_tims_traffic_ll()
        return self.points_vs_trouble(self, points, traffic_coords)


    def get_map(self):
        gpx = self.get_gpx()
        points = [[str(i[0].latitude), str(i[0].longitude)] for i in gpx.walk()]
        return directions_map_url(points)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

