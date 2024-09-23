from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('vehicles/<int:vehicle_id>/', vehicle),
    path('productions/<int:production_id>/', production),
]