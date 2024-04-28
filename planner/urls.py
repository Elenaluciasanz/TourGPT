from django.urls import path, include
from . import views

urlpatterns = [
    path('new_route/', views.route_new, name='route_new'),
    path('route/<int:pk>/', views.route_details, name='route_details'),
    path('route_list/', views.route_list, name='route_list'),
    path('route/<int:pk>/cancel/', views.route_cancel, name='route_cancel'),  
]