from django.contrib import admin
from .models import UserModel,Officer
# Register your models here.
models_list = [UserModel,Officer]
admin.site.register(models_list)