from django.urls import path
from . import views

app_name = 'nucleo'

urlpatterns = [
    path ('', views.index, name='nucleo'),
]