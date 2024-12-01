from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='gpttp/services/home/', permanent=True)),
    path('gpttp/services/',include('services.urls')),
    path('gpttp/users/',include('users.urls')),
    path('gpttp/planner/',include('planner.urls')),
)
