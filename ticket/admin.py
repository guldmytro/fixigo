from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'status', 'created', 'updated']
    search_fields = ['subject', 'body']
    list_filter = ['status', 'created', 'updated']
