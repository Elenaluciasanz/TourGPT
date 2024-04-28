from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('account_details/<int:pk>/', views.AccountView.as_view(), name='account_details'),
    path('account_details/<int:pk>/travel_profile_new/', views.travel_profile_new, name='travel_profile_new'),
    path('account_details/<int:acc>/travel_profile_details/<int:pk>', views.travel_profile_view, name='travel_profile_details'),
    path('account_details/<int:pk>/travel_profile_list/', views.travel_profile_list, name='travel_profile_list'),
    path('account_details/<int:acc>/travel_profile_update/<int:pk>', views.travel_profile_update, name='travel_profile_update'),
    path('account_details/<int:acc>/travel_profile_delete/<int:pk>', views.travel_profile_delete, name='travel_profile_delete'),
    path('country/like', views.country_like, name = "country_like"),
    path('city/like', views.city_like, name = "city_like"),
    path('poi/like', views.poi_like, name = "poi_like"),
    path('poe/like', views.poe_like, name = "poe_like"),
    path('pog/like', views.pog_like, name = "pog_like"),
    path('poa/like', views.poa_like, name = "poa_like"),
    path('fav_countries/', views.CountriesFavListView.as_view(), name = "fav_countries"),
    path('fav_cities/', views.CitiesFavListView.as_view(), name = "fav_cities"),
    path('fav_pois/', views.PoisFavListView.as_view(), name = "fav_pois"),
    path('fav_poes/', views.PoesFavListView.as_view(), name = "fav_poes"),
    path('fav_pogs/', views.PogsFavListView.as_view(), name = "fav_pogs"),
    path('fav_poas/', views.PoasFavListView.as_view(), name = "fav_poas"),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_email/', views.validate_email, name='validate_email')
]