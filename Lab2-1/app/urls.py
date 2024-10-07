from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('vehicles/<int:vehicle_id>/', vehicle_details, name="vehicle_details"),
    path('vehicles/<int:vehicle_id>/add_to_production/', add_vehicle_to_draft_production, name="add_vehicle_to_draft_production"),
    path('productions/<int:production_id>/delete/', delete_production, name="delete_production"),
    path('productions/<int:production_id>/', production)
]
