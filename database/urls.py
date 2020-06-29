from django.urls import path
from .views import NSDL

urlpatterns = [
    path('NSDL/', NSDL.as_view()),
    
]