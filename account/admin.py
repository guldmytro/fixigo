from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'city', 'street', 'phone']
    search_fields = ['fullname', 'city', 'street']
