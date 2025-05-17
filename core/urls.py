from django.urls import path
from . import views

urlpatterns = [
    path("", views.patient_list, name="list"),
    path("p/add/", views.patient_add, name="patient_add"),
    path("p/<int:pk>/", views.patient_detail, name="detail"),
    path("p/<int:pk>/add/", views.add_temp, name="add"),
]