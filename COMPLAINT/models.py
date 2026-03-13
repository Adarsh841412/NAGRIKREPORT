from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


class Complaint(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('in_progress', 'In Progress'),
        ('invalid', 'Invalid'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(
        'ACCOUNT.UserModel',
        related_name='complaints',
        on_delete=models.CASCADE
    )

    assigned_officer = models.ForeignKey(
        'ACCOUNT.Officer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )

    category = models.ForeignKey(
        'DEPARTMENT.Category',
        on_delete=models.PROTECT,
        related_name='complaints'
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    location_address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        errors = {}

        if not self.user:
            errors['user'] = 'User is required.'
        elif self.user.role != 'citizen':
            errors['user'] = 'User must be a citizen.'

        if not self.title or len(self.title.strip()) < 5:
            errors['title'] = 'Title must contain at least 5 characters.'

        if not self.description or len(self.description.strip()) < 20:
            errors['description'] = 'Description must contain at least 20 characters.'

        if not self.location_address or len(self.location_address.strip()) == 0:
            errors['location_address'] = 'Address cannot be empty.'

        if not self.category:
            errors['category'] = 'Category is required.'

        if self.latitude < -90 or self.latitude > 90:
            errors['latitude'] = 'Latitude must be between -90 and 90.'

        if self.longitude < -180 or self.longitude > 180:
            errors['longitude'] = 'Longitude must be between -180 and 180.'

        if self.assigned_officer:
            if self.assigned_officer.user_id.role != 'officer':
                errors['assigned_officer'] = 'Assigned user must be an officer.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ComplaintMedia(models.Model):

    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='media_files'
    )

    media_file = CloudinaryField('media')

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = {}

        if not self.complaint:
            errors['complaint'] = 'Complaint is required.'

        if not self.media_file:
            errors['media_file'] = 'Media file is required.'

        if not self.media_type:
            errors['media_type'] = 'Media type is required.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Media for {self.complaint}"


class ComplaintStatusHistory(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('in_progress', 'In Progress'),
        ('invalid', 'Invalid'),
    ]

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='status_history'
    )

    changed_by = models.ForeignKey(
        'ACCOUNT.UserModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='changed_complaint_statuses'
    )

    old_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=True,
        blank=True
    )

    new_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    changed_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = {}

        if not self.complaint:
            errors['complaint'] = 'Complaint is required.'

        if not self.new_status:
            errors['new_status'] = 'New status is required.'

        if self.old_status and self.old_status == self.new_status:
            errors['new_status'] = 'Old status and new status cannot be the same.'

        if self.changed_by:
            if self.changed_by.role not in ['officer', 'admin']:
                errors['changed_by'] = 'Only officer or admin can change complaint status.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint.title} : {self.old_status} → {self.new_status}"