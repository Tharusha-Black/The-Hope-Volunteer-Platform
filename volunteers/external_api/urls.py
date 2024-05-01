# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/events/', views.EventListView.as_view(), name='event-list'),
]