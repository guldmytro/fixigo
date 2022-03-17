from django.contrib import admin
from .models import Rate
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Rate)
class RateAdmin(SummernoteModelAdmin):
    list_display = ['title', 'status']
    summernote_fields = ('description',)
    list_filter = ['status']
