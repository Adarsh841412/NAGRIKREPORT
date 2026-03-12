from django.urls import path
from .import views 

urlpatterns = [
    path("",views.index,name="index"),
    path('register/',views.register,name='register'),
    path('verify_otp/<int:user_id>',views.verify_otp,name='verify_otp'),
    path('home/',views.home,name='home'),
    path("citizenlogin/",views.login1,name='login'),
    path("officer/",views.officer,name='officer'),
    path('select-role/',views.select_role,name="select_role"),
    path('oficerlogin/',views.Officerlogin,name="officer_login"),
    path('officerpage/',views.OfficerPage,name="officer_page"),
    path("logout/",views.logout_view,name="logout")


]

