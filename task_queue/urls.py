from django.urls import path
from . import views

urlpatterns = [
    path('submit-task/', views.submit_task)
]
