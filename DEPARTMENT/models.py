from django.db import models
from django.core.validators import (
    MinLengthValidator,
    RegexValidator
)



class Department(models.Model):

    DEPARTMENT_CHOICES = [
        ("Water Department", "Water Department"),
        ("Road Department", "Road Department"),
        ("Electricity Department", "Electricity Department"),
        ("Sanitation Department", "Sanitation Department"),
        ("Drainage Department", "Drainage Department"),
        ("Street Light Department", "Street Light Department"),
    ]

    dep_id = models.AutoField(primary_key=True)

    department_name = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES
    )

    department_code = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(2, message="Department code must be at least 2 characters long."),
            RegexValidator(
                regex=r'^[A-Z0-9]+$',
                message="Department code must be uppercase and alphanumeric."
            )
        ]
    )

    department_email = models.EmailField(unique=True)

    contact_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Contact number must be exactly 10 digits."
            )
        ]
    )

    office_address = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(10, message="Office address must be at least 10 characters long.")
        ]
    )

    officer = models.ForeignKey(
        "ACCOUNT.Officer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.department_name


class Category(models.Model):

    CATEGORY_CHOICES = [
        ("Water Leakage", "Water Leakage"),
        ("No Water Supply", "No Water Supply"),
        ("Pothole Issue", "Pothole Issue"),
        ("Broken Road", "Broken Road"),
        ("Power Cut", "Power Cut"),
        ("Street Light Not Working", "Street Light Not Working"),
        ("Garbage Issue", "Garbage Issue"),
        ("Drain Blockage", "Drain Blockage"),
    ]

    category_name = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField(
        validators=[
            MinLengthValidator(5, message="Description must be at least 5 characters long.")
        ]
    )

    is_active = models.BooleanField(default=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name