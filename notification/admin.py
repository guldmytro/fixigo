from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'publish']
    search_fields = ['title', 'body']
    list_filter = ['status', 'publish']
