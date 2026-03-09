from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):

    ROLE_CHOICES = (('citizen','Citizen'),('officer','Officer'),('admin','Admin'))
    
    role = models.CharField(max_length=10,choices=ROLE_CHOICES ,blank=False,null=False)
    phone_number = models.IntegerField(blank=True , null= True)
    address = models.CharField(max_length=1000,blank=False,null=False)
    last_login = models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        verbose_name = "UserModel"
        verbose_name_plural = "UserModels"


class Officer(models.Model):
    DESIGNATION_CHOICES = [
        ('commissioner', 'Commissioner'),
        ('deputy_commissioner', 'Deputy Commissioner'),
        ('municipal_officer', 'Municipal Officer'),
        ('sanitation_officer', 'Sanitation Officer'),
        ('health_officer', 'Health Officer'),
        ('water_supply_officer', 'Water Supply Officer'),
        ('electricity_officer', 'Electricity Officer'),
        ('road_transport_officer', 'Road & Transport Officer'),
        ('environment_officer', 'Environment Officer'),
        ('fire_department_officer', 'Fire Department Officer'),
        ('police_officer', 'Police Officer'),
        ('traffic_officer', 'Traffic Officer'),
        ('housing_officer', 'Housing Officer'),
        ('public_works_officer', 'Public Works Officer'),
        ('education_officer', 'Education Officer'),
        ('it_officer', 'IT Officer'),
        ('maintenance_officer', 'Maintenance Officer'),
        ('waste_management_officer', 'Waste Management Officer'),
        ('zonal_officer', 'Zonal Officer'),
        ('ward_officer', 'Ward Officer'),
    ]
    user_id = models.OneToOneField(UserModel,on_delete=models.SET_NULL,null=True)
    designation = models.CharField(max_length=200,choices=DESIGNATION_CHOICES)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    landmark = models.CharField(max_length=50)
    assigned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass 