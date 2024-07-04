
from . models import Numbers
from . models import Booking
from . models import Person
from . models import Services
from . models import ServiceBooking
from django.contrib import admin


admin.site.register(Numbers)
admin.site.register(Booking)
admin.site.register(Person)
admin.site.register(Services)
admin.site.register(ServiceBooking)



# Register your models here.
