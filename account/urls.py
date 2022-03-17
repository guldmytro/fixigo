from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<str:unread>/', views.notifications_list, name='notifications_unread'),
    path('notification/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('tickets/', views.tickets_list, name='tickets_list'),
    path('tickets/add/', views.tickets_add, name='tickets_add'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('subscribe/add/', views.subscribe_add, name='subscribe_add'),
]