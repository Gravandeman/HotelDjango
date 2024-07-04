from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Numbers, Booking, Person, FilterPerson, FilterBooking, FilterNumbers, Services, ServiceBooking
from .forms import PersonForm, BookingForm, FilterPersonForm, FilterBookingForm, NumbersForm, FilterNumbersForm, ServicesForm, ServiceBookingForm
from django_tables2 import SingleTableView
from .tables import NumbersTable, BookingTable, PersonTable, ServicesTable, ServiceBookingTable
from .filters import PersonFilter, BookingFilter, NumbersFilter, ServicesFilter, ServiceBookingFilter
from django_tables2 import RequestConfig


# def index(request):
#     numbers = Numbers.objects.all()
#     return render(request, 'main/numbers.html', {'numbers': numbers})


def booking(request):
    bookings = Booking.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            form = BookingForm()
    else:
        form = BookingForm()

    FilterBooking = BookingFilter(request.GET, queryset=bookings)
    bookings = FilterBooking.qs
    table = BookingTable(bookings)
    RequestConfig(request).configure(table)

    return render(request, 'main/booking.html', {'form': form, 'FilterBooking': FilterBooking, 'table': table})


def numbers(request):
    if request.method == 'POST':
        form = NumbersForm(request.POST)
        if form.is_valid():
            form.save()
            form = NumbersForm()  # Пересоздаем форму, чтобы очистить поля
        else:
            numbers = Numbers.objects.all()
            FilterNumbers = NumbersFilter(request.GET, queryset=numbers)
            numbers = NumbersFilter.qs
            return render(request, 'main/numbers.html', {'numbers': numbers, 'form': form, 'FilterNumbers': FilterNumbers})
    else:
        form = NumbersForm()
        numbers = Numbers.objects.all()
        FilterNumbers = NumbersFilter(request.GET, queryset=numbers)
        numbers = NumbersFilter.qs
    return render(request, 'main/numbers.html', {'numbers': numbers, 'form': form, 'FilterNumbers': FilterNumbers})


def person_view(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')  # Redirect to the same view after saving
    else:
        form = PersonForm()

    persons = Person.objects.all()
    FilterPerson = PersonFilter(request.GET, queryset=persons)
    persons = FilterPerson.qs
    table = PersonTable(persons)
    RequestConfig(request).configure(table)

    return render(request, 'main/person.html', {'persons': persons, 'form': form, 'FilterPerson': FilterPerson, 'table': table})


def Sign_Up(request):
    return render(request, 'main/Sign_Up.html')


class NumbersListView(SingleTableView):
    model = Numbers
    table_class = NumbersTable
    template_name = 'main/numbers.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = NumbersFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class ServicesListView(SingleTableView):
    model = Services
    table_class = ServicesTable
    template_name = 'main/services.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = ServicesFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

def services(request):
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            form = ServicesForm()  # Пересоздаем форму, чтобы очистить поля
        else:
            services = Services.objects.all()
            FilterServices = ServicesFilter(request.GET, queryset=services)
            services = FilterServices.qs
            return render(request, 'main/services.html', {'services': services, 'form': form, 'FilterServices': FilterServices})
    else:
        form = ServicesForm()
        services = Services.objects.all()
        FilterServices = ServicesFilter(request.GET, queryset=services)
        services = FilterServices.qs
    return render(request, 'main/services.html', {'services': services, 'form': form, 'FilterServices': FilterServices})


def service_booking(request):
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form = ServiceBookingForm()  # Очистка формы после сохранения
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ServiceBookingForm()

    filter_ = ServiceBookingFilter(request.GET, queryset=ServiceBooking.objects.all())
    table = ServiceBookingTable(filter_.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    return render(request, 'main/service_booking.html', {
        'form': form,
        'filter': filter_,
        'table': table,
    })



