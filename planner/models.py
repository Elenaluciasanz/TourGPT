from django.db import models
from django.urls import reverse
from users.models import User, TravelProfile
from services.models import Poi, Poe, Poa, Pog
from cities_light.models import City as CityBase
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date

ROUTE_STATES = (
    ('P', _('Planned')),
    ('I', _('In Progress')),
    ('F', _('Finished')),
    ('C', _('Cancelled')),
)

ROUTE_ACTIVITY_MOMENT = (
    ('M', _('Morning')),
    ('A', _('Afternoon')),
    ('E', _('Evening')),
    ('N', _('Night')),
)

ROUTE_ACTIVITY_TYPE = (
    ('I', _('Interest')), 
    ('E', _('Entertainment')),
    ('G', _('Gastronomy')),
    ('O', _('Other')),
)

class Route(models.Model):
    title = models.CharField(max_length = 100, verbose_name=_('Title'))
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name=_('User'))
    travel_profile = models.ForeignKey(TravelProfile, on_delete = models.CASCADE, verbose_name=_('Travel Profile'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateField(verbose_name=_('Start Date')) 
    end_date = models.DateField(verbose_name=_('End Date'))
    days = models.IntegerField(verbose_name=_('Days'), default = 0)
    state = models.CharField(choices = ROUTE_STATES ,max_length = 1, verbose_name=_('State'))
    origin = models.ForeignKey(CityBase, on_delete = models.CASCADE, related_name = 'origin', verbose_name=_('Origin'))
    destination = models.ForeignKey(CityBase, on_delete = models.CASCADE, related_name = 'destination', verbose_name=_('Destination'))
    poa_en = models.ForeignKey(Poa, on_delete = models.CASCADE, related_name = 'poa_en', verbose_name=_('Accommodation Point EN'), null = True, blank = True)
    poa_es = models.ForeignKey(Poa, on_delete = models.CASCADE, related_name = 'poa_es', verbose_name=_('Accommodation Point ES'), null = True, blank = True)
    explanation_es = models.TextField(verbose_name=_('Explanation ES'), null = True, blank = True)
    explanation_en = models.TextField(verbose_name=_('Explanation EN'), null = True, blank = True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.start_date = datetime.strptime(str(self.start_date), '%Y-%m-%d').date()
        self.end_date = datetime.strptime(str(self.end_date), '%Y-%m-%d').date()
        self.days = (self.end_date - self.start_date).days + 1
        
        now = date.today()
        if self.state != 'C':
            if now < self.start_date:
                self.state = 'P'
                
            elif self.start_date <= now and now <= self.end_date:
                self.state = 'I'
                
            else:
                self.state = 'F'
        super(Route, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('route_details', args=[str(self.pk)])
    
    def update_state(self):
        now = date.today()
        if self.state == 'C':
            return 
        
        if now < self.start_date:
            self.state = 'P'
            
        elif self.start_date <= now and now <= self.end_date:
            self.state = 'I'
            
        else:
            self.state = 'F'
        
        super(Route, self).save()
        return
    
    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _('Routes')
    
    
class RouteDay(models.Model):
    route = models.ForeignKey(Route, on_delete = models.CASCADE, verbose_name=_('Route'))
    date = models.DateField(verbose_name=_('Date'))
    day = models.IntegerField(verbose_name=_('Day'))
    presentation = models.TextField(verbose_name=_('Presentation'))
    presentation_es = models.TextField(verbose_name=_('Presentation ES'))

    def __str__(self):
        return self.route.title + " - " + str(self.date)
    
    def get_absolute_url(self):
        return reverse('route_day_details', args=[str(self.pk)])
    
    class Meta:
        unique_together = ('route', 'date')
        verbose_name = _('Route Day')
        verbose_name_plural = _('Route Days')
        ordering = ['date']
        
        
class RouteDayActivity(models.Model):
    route_day = models.ForeignKey(RouteDay, on_delete = models.CASCADE, verbose_name=_('Route Day'))
    activity = models.TextField(verbose_name=_('Activity'))
    moment = models.CharField(choices = ROUTE_ACTIVITY_MOMENT, verbose_name=_('Moment of the day'))
    type = models.CharField(choices = ROUTE_ACTIVITY_TYPE, verbose_name=_('Activity Type'))
    lang = models.CharField(verbose_name=_('Information Language'))
    
    def __str__(self):
        return self.activity
    
    class Meta:
        db_table = 'planner_route_day_activity'
        verbose_name = _('Generic Activity')
        verbose_name_plural = _('Generic Activities')
        
class RouteDayActivityInterest(RouteDayActivity):
    point = models.ForeignKey(Poi, on_delete = models.CASCADE, verbose_name=_('Point of Interest'), null = True, blank = True)
    
    class Meta:
        db_table = 'planner_route_day_activity_interest'
        verbose_name = _('Interest Activity')
        verbose_name_plural = _('Interest Activities')
        
class RouteDayActivityEntertainment(RouteDayActivity):
    point = models.ForeignKey(Poe, on_delete = models.CASCADE, verbose_name=_('Point of Entertainment'), null = True, blank = True)
    
    class Meta:
        db_table = 'planner_route_day_activity_entertainment'
        verbose_name = _('Entertainment Activity')
        verbose_name_plural = _('Entertainment Activities')
        
class RouteDayActivityGastronomy(RouteDayActivity):
    point = models.ForeignKey(Pog, on_delete = models.CASCADE, verbose_name=_('Point of Gastronomy'), null = True, blank = True)
    
    class Meta:
        verbose_name = _('Gastronomic Activity')
        verbose_name_plural = _('Gastronomic Activities')
