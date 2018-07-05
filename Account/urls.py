"""
Definition of urls for MachLab.
"""

from Account import views as account_view
from django.conf.urls import include, url

urlpatterns = [
    # Account Pages #
    url('login/', account_view.login, name='login'),
    url('register/', account_view.register, name='register'),
    url('lost-password/', account_view.lost_password, name='lost-password'),
    url('logout/', account_view.logout, name='logout'),
    url('profile/', account_view.profile, name='profile'),
]

