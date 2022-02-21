from account.models import Profile


def notification_processor(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            notifications_count = profile.notifications.filter(status='unread').count()
            return {
                'notifications_count': notifications_count
            }
        except Profile.DoesNotExist:
            return {}
    return {}
