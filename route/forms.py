from django import forms
from models import Route, RouteGroup


class RouteForm(forms.ModelForm):

    class Meta:
        model = Route
        fields = ['route_group', 'title', 'description', 'route_gpx_xml']


class RouteGroupForm(forms.ModelForm):

    class Meta:
        model = RouteGroup