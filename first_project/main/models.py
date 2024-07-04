from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import post_init
from django.dispatch import receiver
from .validators import validate_passport
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class Person(models.Model):
    SEX_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    STATUS_CHOICES = [
        ('O', 'Обычный'),
        ('V', 'ВИП'),
    ]

    name = models.TextField('ФИО')
    birth_date = models.DateField('Дата рождения')
    sex = models.CharField('Пол', max_length=1, choices=SEX_CHOICES)
    passport = models.CharField('Паспортные данные', max_length=11, validators=[validate_passport])
    status = models.CharField('Статус', max_length=1, choices=STATUS_CHOICES)
    species = models.TextField('Особенности')

    def __str__(self):
        return self.name


class Numbers(models.Model):
    STATUS_TYPE = [
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
    ]
    title = models.CharField('Номер', max_length=50)
    room_type = models.TextField('Класс номера')
    price = models.TextField('Стоимость в баксах')
    count_rooms = models.IntegerField('Количество комнат')
    count_person = models.IntegerField('Местность')
    status = models.CharField('Статус', max_length=20, choices=STATUS_TYPE)

    def __str__(self):
        return self.title

class FilterNumbers(models.Model):
    STATUS_TYPE2 = [
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
    ]
    title = models.CharField('Номер', max_length=50)
    room_type = models.TextField('Класс номера')
    price = models.TextField('Стоимость в баксах')
    count_rooms = models.IntegerField('Количество комнат')
    count_person = models.IntegerField('Местность')
    status = models.CharField('Статус', max_length=20, choices=STATUS_TYPE2)

    def __str__(self):
        return self.title


class Booking(models.Model):
    titleB = models.ForeignKey(Numbers, on_delete=models.CASCADE, related_name='bookings', verbose_name='Номер')
    guest = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='bookings', verbose_name='Гость')
    begin_date = models.DateField('Дата начала бронирования')
    end_date = models.DateField('Дата окончания бронирования')

    def __str__(self):
        return f'Бронирование номера {self.titleB.title} для {self.guest.name} с {self.begin_date} по {self.end_date}'


@receiver(post_save, sender=Booking)
def update_room_status(sender, instance, created, **kwargs):
    if created:
        room = instance.titleB
        current_date = timezone.now().date()
        bookings = Booking.objects.filter(
            titleB=room,
            begin_date__lte=current_date,
            end_date__gte=current_date
        )

        if bookings.exists():
            room.status = 'Занят'
        else:
            room.status = 'Свободен'

        room.save(update_fields=['status'])


@receiver(pre_save, sender=Booking)
def update_room_status(sender, instance, **kwargs):
    if instance.pk:
        room = instance.titleB
        current_date = timezone.now().date()
        bookings = Booking.objects.filter(
            titleB=room,
            begin_date__lte=current_date,
            end_date__gte=current_date
        )

        if bookings.exists():
            room.status = 'Занят'
        else:
            room.status = 'Свободен'

        room.save(update_fields=['status'])


class Services(models.Model):
    id_service = models.IntegerField('ID')
    name = models.TextField('Наименование')
    price = models.IntegerField('Стоимость')
    duration = models.DurationField('Продолжительность')

    def __str__(self):
        return self.name


class ServiceBooking(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="Услуга")
    guest = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Гость")
    service_date = models.DateField(verbose_name="Дата оказания услуги")
    service_time = models.TimeField(verbose_name="Время оказания услуги")

    def __str__(self):
        return f'{self.service} для {self.guest} на {self.service_date} в {self.service_time}'

    def clean(self):
        # Получить дату и время начала услуги
        start_datetime = datetime.combine(self.service_date, self.service_time)

        # Получить дату и время окончания услуги
        end_datetime = start_datetime + self.service.duration

        # Найти бронирования, которые пересекаются с текущим бронированием
        overlapping_bookings = ServiceBooking.objects.filter(
            service=self.service,
            service_date=self.service_date
        ).exclude(id=self.id)

        overlap_count = 0
        for booking in overlapping_bookings:
            booking_start_datetime = datetime.combine(booking.service_date, booking.service_time)
            booking_end_datetime = booking_start_datetime + booking.service.duration

            # Проверка на пересечение интервалов
            if not (end_datetime <= booking_start_datetime or start_datetime >= booking_end_datetime):
                overlap_count += 1

        if overlap_count >= 3:
            raise ValidationError(
                f"На {self.service_date} в {self.service_time} уже забронировано 3 услуги '{self.service}'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class FilterPerson(models.Model):
    SEX_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    STATUS_CHOICES = [
        ('O', 'Обычный'),
        ('V', 'ВИП'),
    ]

    name = models.TextField('ФИО')
    birth_date = models.DateField('Дата рождения')
    sex = models.CharField('Пол', max_length=1, choices=SEX_CHOICES)
    passport = models.CharField('Паспортные данные', max_length=11, validators=[validate_passport])
    status = models.CharField('Статус', max_length=1, choices=STATUS_CHOICES)
    species = models.TextField('Особенности')

    def __str__(self):
        return self.name


class FilterBooking(models.Model):
    titleB = models.ForeignKey(Numbers, on_delete=models.CASCADE, related_name='filerBookings', verbose_name='Номер')
    guest = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='filterBookings', verbose_name='Гость')  # Изменение здесь
    begin_date = models.DateField('Дата начала бронирования')
    end_date = models.DateField('Дата окончания бронирования')

    def __str__(self):
        return self.titleB