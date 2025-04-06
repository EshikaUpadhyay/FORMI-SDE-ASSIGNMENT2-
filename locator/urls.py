from django.urls import path
from .views import nearest_property_view

urlpatterns = [
    path('nearest-property/', nearest_property_view)
]