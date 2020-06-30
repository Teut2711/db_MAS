from django.urls import path
from .views import NSDLView, SuccessView

urlpatterns = [
    path('nsdl/', NSDLView.as_view()),
    path('success/', SuccessView.as_view()),
]