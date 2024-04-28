from django.contrib import admin
from .models import Route, RouteDay, RouteDayActivityInterest, RouteDayActivityEntertainment, RouteDayActivityGastronomy

admin.site.register(Route)
admin.site.register(RouteDay)
admin.site.register(RouteDayActivityInterest)
admin.site.register(RouteDayActivityEntertainment)
admin.site.register(RouteDayActivityGastronomy)