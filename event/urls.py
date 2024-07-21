from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name="event-homepage"),
  path('Detail/', views.detail, name="event-detail"),
  path('Create/', views.create, name="event-create")
]
