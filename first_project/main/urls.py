from django.urls import path
from . import views
from .views import NumbersListView, ServicesListView, services

urlpatterns = [
    path('booking', views.booking, name='booking'),
    path('person', views.person_view, name='person'),
    # path('', views.numbers, name='numbers'),
    path('', NumbersListView.as_view(), name='numbers'),
    path('person_list', views.person_view, name='person_list'),
    path('Sign_Up', views.Sign_Up, name='Sign_Up'),
    path('services', ServicesListView.as_view(), name='services'),
    path('service_booking', views.service_booking, name='service_booking'),
]
