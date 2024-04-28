import ast
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from services.models import Country, City, Poi, Poe, Pog, Poa
from services.models import POI_TYPES_DICT, POE_TYPES_DICT, POG_TYPES_DICT, POA_TYPES_DICT
from django.utils.translation import gettext_lazy as _

ADVENTURE_LEVELS_LIST = [
    ('E',_('Extreme')),
    ('H',_('High')),
    ('M',_('Medium')),
    ('L',_('Low')),
    ('N',_('None')),  
]

ADVENTURE_LEVELS_DICT = {
    'E': 'Extreme',
    'H': 'High',
    'M': 'Medium',
    'L': 'Low',
    'N': 'None',  
}

REASON_LIST = [
    ('FV',_('Family Vacation')),
    ('VF',_('Vacation With Friends')),
    ('WO',_('Work')),
    ('ST',_('Studies')),
    ('RJ',_('Romantic Journey')),
    ('AD',_('Adventure')),
    ('LE',_('Leisure')),
    ('TU',_('Turism')),
    ('CO',_('Chill Out')),
    ('SP',_('Sport')),
    ('WE',_('Wedding/Honeymoon/Anniversary')),
    ('RE',_('Religion')),
    ('GA',_('Gastronomy')),
    ('VO',_('Volunteering')),
    ('CC',_('Conferences/Conventions')),
    ('OT',_('Other')),
]


REASON_DICT = {
    'FV': 'Family Vacation',
    'VF': 'Vacation With Friends',
    'WO': 'Work',
    'ST': 'Studies',
    'RJ': 'Romantic Journey',
    'AD': 'Adventure',
    'LE': 'Leisure',
    'TU': 'Turism',
    'CO': 'Chill Out',
    'SP': 'Sport',
    'WE': 'Wedding/Honeymoon/Anniversary',
    'RE': 'Religion',
    'GA': 'Gastronomy',
    'VO': 'Volunteering',
    'CC': 'Conferences/Conventions',
    'OT': 'Other',
}

class User(AbstractUser):
    birth = models.DateField(default = timezone.now, null=True, blank=True, verbose_name=_('Birth Date'))
    number = models.CharField(max_length = 9, null = True, blank = True, verbose_name=_('Phone Number'))
    fav_countries = models.ManyToManyField(Country, verbose_name=_('Favorite Countries'))
    fav_cities = models.ManyToManyField(City, verbose_name=_('Favorite Cities'))
    fav_pois = models.ManyToManyField(Poi, verbose_name=_('Favorite Interest Points'))
    fav_poes = models.ManyToManyField(Poe, verbose_name=_('Favorite Entertainment Points'))
    fav_pogs = models.ManyToManyField(Pog, verbose_name=_('Favorite Gastronomy Points'))
    fav_poas = models.ManyToManyField(Poa, verbose_name=_('Favorite Accommodation Points'))
    
    def get_absolute_url(self):
        return reverse('account_details', args=[str(self.pk)])
    
    
class TravelProfile(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name=_('User'))
    title = models.CharField(max_length = 40, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    
    n_adults = models.IntegerField(default = 0, verbose_name=_('Number of Adults'))
    n_teenagers = models.IntegerField(default = 0, verbose_name=_('Number of Teenagers'))
    n_children = models.IntegerField(default = 0, verbose_name=_('Number of Children'))
    n_babies = models.IntegerField(default = 0, verbose_name=_('Number of Babies'))
    n_elderly = models.IntegerField(default = 0, verbose_name=_('Number of Elderly'))
    
    reason = models.CharField(verbose_name=_('Reason'), default='[]')
    adventure_level = models.CharField(choices = ADVENTURE_LEVELS_LIST, default = 'N', verbose_name=_('Adventure Level'))
    
    reduced_mobility = models.BooleanField(default = False, verbose_name=_('Reduced Mobility'))
    animals = models.BooleanField(default = False, verbose_name=_('Animals'))
    
    reason = models.CharField(verbose_name=_('Reason'), default='[]')
    adventure_level = models.CharField(choices = ADVENTURE_LEVELS_LIST, default = 'N', verbose_name=_('Adventure Level'))
    
    pref_poi = models.CharField(verbose_name=_('Point of Interest'), default = '[]')
    pref_poe = models.CharField(verbose_name=_('Point of Entertainment'), default = '[]')
    pref_pog = models.CharField(verbose_name=_('Point of Gastronomy'), default = '[]')
    pref_poa = models.CharField(verbose_name=_('Point of Accommodation'), default='[]')
    
    food_restrictions = models.CharField(max_length = 200, verbose_name=_('Food Restrictions'), default="")
    observations = models.TextField(max_length = 400, verbose_name=_('Observations'), default="")
 

    def __str__(self):
        profile = ""
        
        if self.n_adults > 0:
            profile += "Adults: " + str(self.n_adults) + "\n"
        
        if self.n_teenagers > 0:
            profile += "Teenagers: " + str(self.n_teenagers) + "\n"
            
        if self.n_children > 0:
            profile += "Children: " + str(self.n_children) + "\n"
            
        if self.n_babies > 0:
            profile += "Babies: " + str(self.n_babies) + "\n"
                
        if self.n_elderly > 0:
            profile += "Elderly: " + str(self.n_elderly) + "\n"
              
        if self.reduced_mobility:
            profile += "With Reduced Mobility\n"
                        
        if self.animals:
            profile += "With Animals. Search accommodation and activities where animals are admitted\n"
                
        reasons = ""
        list_reason = ast.literal_eval(self.reason)
        for reason in list_reason:
            reasons += REASON_DICT[reason] + ", "
        profile += "Reason: " + reasons + "\n"
        
        if self.adventure_level:
            profile += "Adventure Level: " + ADVENTURE_LEVELS_DICT[self.adventure_level] + "\n"
                 
        pois = ""
        list_poi = ast.literal_eval(self.pref_poi)
        for poi in list_poi:
            pois += POI_TYPES_DICT[poi] + ", "
        profile += "Favorite interest points: " + pois + "\n"
        
        poes = ""
        list_poe = ast.literal_eval(self.pref_poe)
        for poe in list_poe:
            poes += POE_TYPES_DICT[poe] + ", "
        profile += "Favorite entertainment points: " + poes + "\n"
        
        pogs = ""
        list_pog = ast.literal_eval(self.pref_pog)
        for pog in list_pog:
            pogs += POG_TYPES_DICT[pog] + ", "
        profile += "Favorite gastronomy points: " + pogs + "\n"
        
        if self.food_restrictions != "":
            profile += "Consider these food restrictions when suggesting gastronomy points: " + self.food_restrictions + "\n"
        
        poas = ""
        list_poa = ast.literal_eval(self.pref_poa)
        for poa in list_poa:
            poas += POA_TYPES_DICT[poa] + ", "
        profile += "Favorite accommodation points: " + poas + "\n"
        
        if self.observations != "":
            profile += "Observations: " + self.observations + "\n"
        
        return profile
