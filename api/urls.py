from django.urls import path
from .views import *
urlpatterns = [
    path('show/', show_all),
    path('calculate/', calculate_coordinates),
    path('tree_handle/', tree_handle),
    path('valve_trees/<str:pk>/', get_valve_trees),
]