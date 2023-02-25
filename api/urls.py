from django.urls import path
from .views import *
urlpatterns = [

    #valve management APIs
    path('valves/all/', valve_handle),
    path('valve/', valve_details),
    path('valve/<str:pk>/', valve_details),

    #tree management API
    path('tree_handle/', tree_handle),

    #assign valves to trees
    path('assign/', calculate_coordinates),
    
    #valve/tree quering APIs
    path('show/', show_assigned),
    path('valve_trees/<str:pk>/', get_valve_trees),
]