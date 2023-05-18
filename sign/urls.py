from django.urls import path

from .views import login_view, logout_view, register_view, email_confirmation_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('email-confirmation/', email_confirmation_view, name='email_confirmation')
]
