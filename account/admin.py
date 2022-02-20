from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'city', 'phone', 'street']
    search_fields = ['fullname']
