from django.forms import ModelForm
from django import forms
from .models import Person, Booking, FilterPerson, FilterBooking, Numbers, FilterNumbers, Services, ServiceBooking
from django.core.exceptions import ValidationError
from .validators import validate_passport


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date', 'sex', 'passport', 'status', 'species']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Введите дату рождения', 'type': 'date'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите паспортные данные в формате ****-******'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите особенности, если нет, укажите - Отсутсвуют'}),
        }

        def clean_passport(self):
            passport = self.cleaned_data.get('passport')
            validate_passport(passport)
            return passport


class NumbersForm(forms.ModelForm):
    class Meta:
        model = Numbers
        fields = ['title', 'room_type', 'price', 'count_rooms', 'count_person', 'status']
        widjets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.Select(attrs={'class': 'form-control'}),
            'count_rooms': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'count_person': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['titleB', 'guest', 'begin_date', 'end_date']
        widgets = {
            'titleB': forms.Select(attrs={'class': 'form-control'}),
            'guest': forms.Select(attrs={'class': 'form-control'}),
            'begin_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        titleB = cleaned_data.get("titleB")
        begin_date = cleaned_data.get("begin_date")
        end_date = cleaned_data.get("end_date")

        if titleB and begin_date and end_date:
            overlapping_bookings = Booking.objects.filter(
                titleB=titleB,
                begin_date__lt=end_date,
                end_date__gt=begin_date
            )

            if overlapping_bookings.exists():
                raise ValidationError("Этот номер уже забронирован на выбранный период.")

        return cleaned_data

class FilterPersonForm(forms.ModelForm):
    class Meta:
        model = FilterPerson
        fields = ['name', 'birth_date', 'sex', 'passport', 'status', 'species']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Введите дату рождения', 'type': 'date'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите паспортные данные'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'species': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите особенности, если нет, укажите - Отсутсвуют'}),
        }


class FilterBookingForm(forms.ModelForm):
    class Meta:
        model = FilterBooking
        fields = ['titleB', 'guest', 'begin_date', 'end_date']
        widgets = {
            'titleB': forms.Select(attrs={'class': 'form-control'}),
            'guest': forms.Select(attrs={'class': 'form-control'}),
            'begin_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class FilterNumbersForm(forms.ModelForm):
    class Meta:
        model = FilterNumbers
        fields = ['title', 'room_type', 'price', 'count_rooms', 'count_person', 'status']
        widjets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.Select(attrs={'class': 'form-control'}),
            'count_rooms': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'count_person': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['id_service', 'name', 'price', 'duration']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }


class ServiceBookingForm(forms.ModelForm):
    service_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label='Дата оказания услуги'
    )
    service_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M'],
        label='Время оказания услуги'
    )

    class Meta:
        model = ServiceBooking
        fields = ['service', 'guest', 'service_date', 'service_time']
