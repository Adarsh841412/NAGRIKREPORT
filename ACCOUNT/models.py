from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re
from django.utils import timezone



class UserModel(AbstractUser):

    ROLE_CHOICES = (
        ('citizen','Citizen'),
        ('officer','Officer'),
        ('admin','Admin')
    )
    
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default="citizen")
    address = models.CharField(max_length=1000,blank=True,null=True)

    mobile_number = models.CharField(max_length=15, unique=True)

    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)

    email_otp = models.CharField(max_length=6,null=True,blank=True)
    mobile_otp = models.CharField(max_length=6,null=True,blank=True)

    otp_created_at = models.DateTimeField(null=True,blank=True)

    def clean(self):

        errors = {}

        # Username validation
        if len(self.username) < 3:
            errors['username'] = ["Username must be at least 3 characters"]

        # Email validation
        if not self.email:
            errors['email'] = ["Email required"]

        # Mobile validation
        if not self.mobile_number.isdigit():
            errors['mobile_number'] = ["Mobile must contain digits only"]

        if len(self.mobile_number) != 10:
            errors['mobile_number'] = ["Mobile must be 10 digits"]

        # Password validation
        if self.password:
            if len(self.password) < 6:
                errors['password'] = ["Password must be 6+ characters"]

        # Role validation
        if self.role not in ['citizen','officer','admin']:
            errors['role'] = ["Invalid role"]

        if errors:
            raise ValidationError(errors)

    def save(self,*args,**kwargs):
        self.full_clean()
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = "UserModel"



class Officer(models.Model):

    user_id = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE
    )

    designation = models.CharField(max_length=100)

    lon = models.FloatField()

    lat = models.FloatField()
    assigned_date = models.DateField(default=timezone.now)
    landmark = models.CharField(max_length=255)

    def clean(self):

        errors = {}

        # User role validation
        if self.user_id.role != "officer":
            errors['user_id'] = "User must have officer role"

        # Latitude validation
        if self.lat < -90 or self.lat > 90:
            errors['lat'] = "Latitude must be between -90 and 90"

        # Longitude validation
        if self.lon < -180 or self.lon > 180:
            errors['lon'] = "Longitude must be between -180 and 180"

        # Landmark validation
        if not self.landmark:
            errors['landmark'] = "Landmark required"

        if errors:
            raise ValidationError(errors)

    def save(self,*args,**kwargs):

        # Run model validation automatically
        self.full_clean()

        super().save(*args,**kwargs)

    def __str__(self):
        return self.user_id.name