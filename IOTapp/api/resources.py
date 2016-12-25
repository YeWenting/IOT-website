__author__ = 'wzl'

from tastypie.resources import ModelResource
from IOTapp.models import Device
from tastypie.constants import ALL


class DevicelistResource(ModelResource):
    class Meta:
        queryset = Device.objects.all()
        allowed_methods = ['get']
        filtering = {
            "id": ALL
        }