from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_complaint, name="create_complaint"),
    path("my-complaints/", views.my_complaints, name="my_complaints"),
    path("view_complaint_officer",views.view_complaint_officer,name="view_complaint_officer"),
    path(
        "officer/complaint/<int:complaint_id>/start/",
        views.start_complaint_work,
        name="start_complaint_work"
    ),
    path(
        "officer/complaint/<int:complaint_id>/resolve/",
        views.resolve_complaint_work,
        name="resolve_complaint_work"
    ),
]