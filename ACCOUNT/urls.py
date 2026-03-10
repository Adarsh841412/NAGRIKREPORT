from django.urls import path
from .import views 

urlpatterns = [
    path("",views.index,name="index"),
    path('register/',views.register,name='register'),
    path('verify_otp/<int:user_id>',views.verify_otp,name='verify_otp'),
    path('home/',views.home,name='home'),
    path("login/",views.login1,name='login'),
    path("officer/",views.officer,name='officer')
]

