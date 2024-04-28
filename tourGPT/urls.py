from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='tourGPT/services/home/', permanent=True)),
    path('tourGPT/services/',include('services.urls')),
    path('tourGPT/users/',include('users.urls')),
    path('tourGPT/planner/',include('planner.urls')),
)
