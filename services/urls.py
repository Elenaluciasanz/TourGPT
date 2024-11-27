from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('home/country_search/', views.country_search, name='country_search'),
    path('home/city_search/', views.city_search, name='city_search'),
    path('home/country_list/', views.country_list, name='country_list'),
    path('home/city_list/', views.city_list, name='city_list'),
    path('countries/<str:slug>/', views.CountryDetails.as_view(), name='country_details'),
    path('countries/<str:slug_country>/cities/<str:slug>/', views.CityDetails.as_view(), name='city_details'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/new_poi/', views.CityDetails.new_poi, name='poi_new'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/new_poe/', views.CityDetails.new_poe, name='poe_new'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/new_poa/', views.CityDetails.new_poa, name='poa_new'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/new_pog/', views.CityDetails.new_pog, name='pog_new'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/poi/<str:slug>/', views.PoiDetails.as_view(), name='poi_details'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/poe/<str:slug>/', views.PoeDetails.as_view(), name='poe_details'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/pog/<str:slug>/', views.PogDetails.as_view(), name='pog_details'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/poa/<str:slug>/', views.PoaDetails.as_view(), name='poa_details'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/poi/<str:slug>/modal', views.get_poi_modal, name='poi_modal'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/poe/<str:slug>/modal', views.get_poe_modal, name='poe_modal'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/pog/<str:slug>/modal', views.get_pog_modal, name='pog_modal'),
    path('countries/<str:slug_country>/cities/<str:slug_city>/poa/<str:slug>/modal', views.get_poa_modal, name='poa_modal'),
]