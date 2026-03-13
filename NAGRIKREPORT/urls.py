

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ACCOUNT.urls')),
    path('complaint/', include('COMPLAINT.urls')),
]

handler404 = 'ACCOUNT.views.custom_page_not_found_view'