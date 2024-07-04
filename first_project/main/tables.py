import django_tables2 as tables
from .models import Numbers, Booking, Person, Services, ServiceBooking


class NumbersTable(tables.Table):
    class Meta:
        model = Numbers
        template_name = "django_tables2/bootstrap.html"
        fields = ("title", "room_type", "price", "count_rooms", "count_person", "status")


class BookingTable(tables.Table):
    titleB = tables.Column(verbose_name='Номер', accessor='titleB.title')
    guest = tables.Column(verbose_name='Гость', accessor='guest.name')
    begin_date = tables.DateColumn(verbose_name='Дата начала бронирования')
    end_date = tables.DateColumn(verbose_name='Дата окончания бронирования')

    class Meta:
        model = Booking
        template_name = "django_tables2/bootstrap.html"
        fields = ("titleB", "guest", "begin_date", "end_date")
        order_by = ("begin_date",)


class PersonTable(tables.Table):
    name = tables.Column(verbose_name='ФИО')
    birth_date = tables.DateColumn(verbose_name='Дата рождения')
    sex = tables.Column(verbose_name='Пол')
    passport = tables.Column(verbose_name='Паспортные данные')
    status = tables.Column(verbose_name='Статус')
    species = tables.Column(verbose_name='Особенности')

    class Meta:
        model = Person
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "birth_date", "sex", "passport", "status", "species")
        order_by = ("name",)


class ServicesTable(tables.Table):
    class Meta:
        model = Services
        template_name = "django_tables2/bootstrap.html"
        fields = ("id_service", "name", "price", "duration")


class ServiceBookingTable(tables.Table):
    class Meta:
        model = ServiceBooking
        template_name = "django_tables2/bootstrap.html"
        fields = ("service", "guest", "service_date", "service_time")
