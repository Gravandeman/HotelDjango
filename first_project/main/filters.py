import django_filters
from django_filters import DateTimeFilter
from .models import *


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = '__all__'


class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = '__all__'


class NumbersFilter(django_filters.FilterSet):
    class Meta:
        model = Numbers
        fields = '__all__'


class ServicesFilter(django_filters.FilterSet):
    class Meta:
        model = Services
        fields = '__all__'


class ServiceBookingFilter(django_filters.FilterSet):
    service_name = django_filters.CharFilter(field_name='service__name', lookup_expr='icontains', label='Наименование услуги')
    guest_name = django_filters.CharFilter(field_name='guest__name', lookup_expr='icontains', label='Гость')
    service_date = django_filters.DateFilter(field_name='service_date', label='Дата оказания услуги')
    service_time = django_filters.TimeFilter(field_name='service_time', label='Время оказания услуги')

    class Meta:
        model = ServiceBooking
        fields = ['service', 'guest', 'service_date', 'service_time']
