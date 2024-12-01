from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cities_light.models import Country as CountryBase
from cities_light.models import City as CityBase
from django.utils.translation import gettext_lazy as _
from googletrans import Translator


POI_TYPES = (
    ('O', _('Other')),
    ('M', _('Museum')),
    ('E', _('Emblematic Site')),
    ('P', _('Park/Garden')),
    ('T', _('Theater')),
    ('C', _('Church')),
    ('S', _('Street/Square')),
)

POI_TYPES_DICT = {
    'O': 'Other',
    'M': 'Museum',
    'E': 'Emblematic Site',
    'P': 'Park/Garden',
    'T': 'Theater',
    'C': 'Church',
    'S': 'Street/Square',
}

POE_TYPES = (
    ('O', _('Other')),
    ('C', _('Cinema')),
    ('W', _('Bowling Alley')),
    ('N', _('Nightclub')),
    ('M', _('Mall/Shop')),
    ('T', _('Theme Park')),
    ('B', _('Beach')),
)

POE_TYPES_DICT = {
    'O': 'Other',
    'C': 'Cinema',
    'W': 'Bowling Alley',
    'N': 'Nightclub',
    'M': 'Mall/Shop',
    'T': 'Theme Park',
    'B': 'Beach',
}

POG_TYPES = (
    ('O', _('Other')),
    ('R', _('Restaurant')),
    ('B', _('Bar')),
    ('C', _('Cafeteria')),
    ('F', _('Fast Food')),
    ('T', _('Tabern')),
)

POG_TYPES_DICT = {
    'O': 'Other',
    'R': 'Restaurant',
    'B': 'Bar',
    'C': 'Cafeteria',
    'F': 'Fast Food',
    'T': 'Tabern',
}

POA_TYPES = (
    ('O',  _('Other')),
    ('HO', _('Hotel')),
    ('HE', _('Hostel')),
    ('C', _('Camping')),
    ('R', _('Rural House')),
    ('S', _('Shelter')),
)

POA_TYPES_DICT = {
    'O': 'Other',
    'HO': 'Hotel',
    'HE': 'Hostel',
    'C': 'Camping',
    'R': 'Rural House',
    'S': 'Shelter',
}

class Country(models.Model):
    country = models.ForeignKey(CountryBase, on_delete = models.CASCADE, verbose_name=_('Country Base')) 
    lang = models.CharField(verbose_name=_('Information Language'))
    
    name = models.CharField(verbose_name=_('Name'))
    slug = models.SlugField(unique = True, verbose_name=_('Slug'))
    presentation = models.TextField(verbose_name=_('Presentation'))
    
    national_day = models.TextField(verbose_name=_('National Day'))
    population = models.TextField(verbose_name=_('Total Population'))
    density = models.TextField(verbose_name=_('Population Density'))
    age_structure = models.TextField(verbose_name=_('Age Structure'))
    
    languages = models.TextField(verbose_name=_('Languages'))
    currency = models.TextField(verbose_name=_('Currency'))
    
    police = models.TextField(verbose_name=_('Police'))
    firefighter = models.TextField(verbose_name=_('Firefighter'))
    ambulance = models.TextField(verbose_name=_('Ambulance'))
    
    history = models.TextField(verbose_name=_('History'))
    curiosities = models.TextField(verbose_name=_('Curiosities'))

    @property
    def prefix(self):
        return self.country.phone
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Country, self).save(*args, **kwargs) # Para inicializar self.id
        self.slug = slugify(self.country.name) + "-" + str(self.pk)
        t = Translator()
        try:       
            self.name = t.translate(self.country.name, src = 'en', dest = self.lang).text
        except Exception as e:
            self.name = self.country.name
        super(Country, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('country_details', args=[self.slug])
    
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _('Countries')
        unique_together = ('country', 'lang')


class City(models.Model):
    city = models.ForeignKey(CityBase, on_delete = models.CASCADE, verbose_name=_('City Base')) 
    country = models.ForeignKey(Country, on_delete = models.CASCADE, verbose_name=_('Country'))
    lang = models.CharField(verbose_name=_('Information Language'))
    
    name = models.CharField(verbose_name=_('Name'))
    
    slug = models.SlugField(unique = True, verbose_name=_('Slug'))
    presentation = models.TextField(verbose_name=_('Presentation'))
    
    languages = models.TextField(verbose_name=_('Languages'))
    history = models.TextField(verbose_name=_('History'))
    curiosities = models.TextField(verbose_name=_('Curiosities'))
    
    @property
    def complete_name(self):
        return self.city.name +  ", " + self.country.name
    
    @property
    def longitude(self):
        return self.city.longitude
    
    @property
    def latitude(self):
        return self.city.latitude
    
    @property
    def location(self):
        return self.city.display_name
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)
        self.slug = slugify(self.city.name) + "-" + str(self.pk)
        t = Translator()
        try: 
            self.name = t.translate(self.city.name, src = 'en', dest = self.lang).text
        except Exception as e:
            self.name = self.city.name
        super(City, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('city_details', args=[self.country.slug, self.slug])
    
    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _('Cities')
        unique_together = ('city', 'lang')
    

class PointInfo(models.Model):
    point_name = models.TextField(verbose_name=_('Point Identifier Name'))
    city = models.ForeignKey(City, on_delete = models.CASCADE, verbose_name=_('City'))
    lang = models.CharField(verbose_name=_('Information Language'))
        
    name = models.TextField(verbose_name=_('Name'))
        
    slug = models.SlugField(unique = True, verbose_name=_('Slug'))
    presentation = models.TextField(verbose_name=_('Presentation'))
    
    location = models.TextField(verbose_name=_('Location'))
    latitude = models.FloatField(null = True, verbose_name=_('Latitude'))
    longitude = models.FloatField(null = True, verbose_name=_('Latitude'))
    
    price_avg = models.TextField(verbose_name=_('Price Average'))
    shedule_avg = models.TextField(verbose_name=_('Shedule Average'))
    
    image_url = models.URLField(verbose_name=_('Image URL'), null = True, default=None)
    
    @property
    def complete_name(self):
        return self.point_name + ", " + self.city.complete_name
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(PointInfo, self).save(*args, **kwargs)
        self.slug = slugify(self.point_name) + "-" + str(self.pk)
        t = Translator()
        try: 
            self.name = t.translate(self.point_name, src = 'en', dest = self.lang).text
        except Exception as e:
            self.name = self.point_name
        super(PointInfo, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        db_table = 'services_point_info'
        verbose_name = _('Point Information')
        verbose_name_plural = _('Points Information')
        unique_together = ('point_name', 'lang')
        

class Poi(PointInfo):
    history = models.TextField(verbose_name=_('History'))
    
    type = models.TextField(choices = POI_TYPES, default = 'O', verbose_name=_('Type'))
    
    def get_absolute_url(self):
        return reverse('poi_details', args=[self.city.country.slug, self.city.slug, self.slug])
    
    class Meta:
        db_table = 'services_poi'
        verbose_name = _('Point of Information')
        verbose_name_plural = _('Points of Information')
     

class Poe(PointInfo):
    description = models.TextField(verbose_name=_('Description'))
     
    type = models.TextField(choices = POE_TYPES, default = 'O', verbose_name=_('Type'))
    
    def get_absolute_url(self):
        return reverse('poe_details', args=[self.city.country.slug, self.city.slug, self.slug])
    
    class Meta:
        db_table = 'services_poe'
        verbose_name = _('Point of Entertainment')
        verbose_name_plural = _('Points of Entertainment')

class Pog(PointInfo):
    description = models.TextField(verbose_name=_('Description'))
    
    type = models.TextField(choices = POG_TYPES, default = 'O', verbose_name=_('Type'))
    
    def get_absolute_url(self):
        return reverse('pog_details', args=[self.city.country.slug, self.city.slug, self.slug])
    
    class Meta:
        db_table = 'services_pog'
        verbose_name = _('Point of Gastronomy')
        verbose_name_plural = _('Points of Gastronomy')
        
class Poa(PointInfo):
    description = models.TextField(verbose_name=_('Description'))
    
    type = models.TextField(choices = POA_TYPES, default = 'O', verbose_name=_('Type'))
    
    def get_absolute_url(self):
        return reverse('poa_details', args=[self.city.country.slug, self.city.slug, self.slug])
    
    class Meta:
        db_table = 'services_poa'
        verbose_name = _('Point of Accommodation')
        verbose_name_plural = _('Points of Accommodation')
        
def poi_types():
    classification = ""
    for type in POI_TYPES:
        classification += str(type) + ", "
    return classification

def poe_types():
    classification = ""
    for type in POE_TYPES:
        classification += str(type) + ", "
    return classification

def pog_types():
    classification = ""
    for type in POG_TYPES:
        classification += str(type) + ", "
    return classification

def poa_types():
    classification = ""
    for type in POA_TYPES:
        classification += str(type) + ", "
    return classification

