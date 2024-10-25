from django_filters import FilterSet
from .models import Hotel,Room


class HotelFilter(FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'address': ['exact'],
            'name': ['exact'],


         }


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'price': ['gt', 'lt'],
            'number': ['exact'],

        }