from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_complaint, name="create_complaint"),
    path("my-complaints/", views.my_complaints, name="my_complaints"),
]