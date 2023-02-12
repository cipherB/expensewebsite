"""
    _summary_
    Url patterns lists all routes to the authentication app view
"""
from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('register',RegistrationView.as_view(),name='register')
]
