from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/filters/", views.filter_options, name="filter_options"),
    path("api/telemetry/", views.telemetry_data, name="telemetry_data"),
]
