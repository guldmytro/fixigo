from django.contrib import admin
from .models import Profile, Subscription


class ProfileAdminInline(admin.StackedInline):
    model = Subscription
    list_display = ['title', 'paid', 'status']
    list_filter = ['paid', 'status']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'city', 'street', 'phone']
    search_fields = ['fullname', 'city', 'street']
    inlines = [ProfileAdminInline,]



