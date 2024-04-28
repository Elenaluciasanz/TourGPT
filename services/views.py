
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _,get_language
from .models import Country, City, Poi, Poe, Poa, Pog
from cities_light.models import Country as CountryBase
from cities_light.models import City as CityBase
from services.constants import NUM_POI, NUM_POE, NUM_POA, NUM_POG
import services.prompts.country_prompts as country_pr
import services.prompts.city_prompts as city_pr
import services.prompts.poi_prompts as poi_pr
import services.prompts.poe_prompts as poe_pr
import services.prompts.poa_prompts as poa_pr
import services.prompts.pog_prompts as pog_pr
import folium

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countries = Country.objects.filter(lang = get_language())
        cities = City.objects.filter(lang = get_language())
        country_bases = CountryBase.objects.all()
        city_bases = CityBase.objects.all()
        context['countries'] = countries
        context['cities'] = cities
        context['country_bases'] = country_bases
        context['city_bases'] = city_bases
        return context


def country_list(request):
    context = {
        'countries': Country.objects.filter(lang = get_language()),
        'country_bases': CountryBase.objects.all(),
    } 
    return render(request, 'country_list.html', context)           

def country_search(request):
    country_id = request.GET['country_id']
    country_pr.country_get_or_create(country_id)                                               
    return JsonResponse({})

class CountryDetails(DetailView):
    model = Country
    template_name = 'country_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = context['object']
        
        country_pr.check_country_info(c.country.id)
        
        cities = City.objects.filter(city__country_id = c.country.id, lang = get_language())
        city_bases = CityBase.objects.filter(country_id = c.country.id)
        context = {
            'country': c,
            'cities': cities,
            'city_bases': city_bases,
        }
        return context
 
def city_list(request):
    context = {
        'cities': City.objects.filter(lang = get_language()),
        'city_bases': CityBase.objects.all(),
    } 

    return render(request, 'city_list.html', context)                  

def city_search(request):
    city_id = request.GET['city_id']
    city_pr.city_get_or_create(city_id)                                               
    return JsonResponse({})

class CityDetails(DetailView):
    model = City
    template_name = 'city_details.html'
    
    @classmethod
    def get_city_context(cls, context):
        c = context['city']
         
        city_pr.check_city_info(c.city.id)
    
        map = None
        if c.latitude and c.longitude:
            map = folium.Map(location=(c.latitude, c.longitude), zoom_start=14)
            folium.Marker((c.latitude, c.longitude), popup = c.name, icon=folium.Icon(color='darkpurple',prefix='fa', icon='flag')).add_to(map)
        
        pois = Poi.objects.filter(city = c, lang = get_language())
        for p in pois:
            poi_pr.check_poi_presentation(p.point_name)
            
        pois = Poi.objects.filter(city = c, lang = get_language())
        for p in pois:
            if map != None and p.location and p.latitude and p.longitude:
                folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='green',prefix='fa', icon='landmark')).add_to(map)
                    
        poes = Poe.objects.filter(city = c, lang = get_language())
        for p in poes:
            poe_pr.check_poe_presentation(p.point_name)
            
        poes = Poe.objects.filter(city = c, lang = get_language())
        for p in poes:
            if map != None and p.location and p.latitude and p.longitude:
                folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='red',prefix='fa', icon='ticket')).add_to(map)
        
        pogs = Pog.objects.filter(city = c, lang = get_language())
        for p in pogs:
            pog_pr.check_pog_presentation(p.point_name)
            
        pogs = Pog.objects.filter(city = c, lang = get_language())
        for p in pogs:
            if map != None and p.location and p.latitude and p.longitude:
                folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='blue',prefix='fa', icon='utensils')).add_to(map)
        
        poas = Poa.objects.filter(city = c, lang = get_language())
        for p in poas:
            poa_pr.check_poa_presentation(p.point_name)
            
        poas = Poa.objects.filter(city = c, lang = get_language())
        for p in poas:
            if map != None and p.location and p.latitude and p.longitude:
                folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='orange',prefix='fa', icon='house')).add_to(map)
     
        context['map'] = map._repr_html_()
        context['pois'] = pois
        context['poes'] = poes
        context['pogs'] = pogs
        context['poas'] = poas
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = context['object']  
        CityDetails.get_city_context(context)
        return context
    
    def new_poi(request, slug_country, slug_city):
        c = City.objects.get(slug = slug_city)
        c_en = City.objects.get(city_id = c.city.id, lang='en')
        c_oth = City.objects.filter(city_id = c.city.id).exclude(lang='en')
        poi_pr.poi_recommendations(NUM_POI,c_en, c_oth)
        return JsonResponse({})

    def new_poe(request, slug_country, slug_city):
        c = City.objects.get(slug = slug_city)
        c_en = City.objects.get(city_id = c.city.id, lang='en')
        c_oth = City.objects.filter(city_id = c.city.id).exclude(lang='en')
        poe_pr.poe_recommendations(NUM_POE,c_en, c_oth)
        return JsonResponse({})
    
    def new_pog(request, slug_country, slug_city):
        c = City.objects.get(slug = slug_city)
        c_en = City.objects.get(city_id = c.city.id, lang='en')
        c_oth = City.objects.filter(city_id = c.city.id).exclude(lang='en')
        pog_pr.pog_recommendations(NUM_POG,c_en, c_oth)
        return JsonResponse({})

    
    def new_poa(request, slug_country, slug_city):
        c = City.objects.get(slug = slug_city)
        c_en = City.objects.get(city_id = c.city.id, lang='en')
        c_oth = City.objects.filter(city_id = c.city.id).exclude(lang='en')
        poa_pr.poa_recommendations(NUM_POA,c_en, c_oth)
        return JsonResponse({})

class PoiDetails(DetailView):
    model = Poi
    template_name = 'poi_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = context['object']  
        poi_pr.check_poi_info(p.point_name)
        p = Poi.objects.get(slug = p.slug)
        map = None
        if p.longitude and p.latitude:
            map = folium.Map(location = (p.latitude, p.longitude),zoom_start=10)
            folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='green',prefix='fa', icon='landmark')).add_to(map)
            map = map._repr_html_()
        context['poi'] = p
        context['map'] = map
        return context
    
class PoeDetails(DetailView):
    model = Poe
    template_name = 'poe_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = context['object']  
        poe_pr.check_poe_info(p.point_name)
        p = Poe.objects.get(slug = p.slug)
        map = None
        if p.latitude and p.longitude:
            map = folium.Map(location = (p.latitude, p.longitude),zoom_start=10)
            folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='red',prefix='fa', icon='ticket')).add_to(map)
            map = map._repr_html_()
        context['poe'] = p
        context['map'] = map
        return context
    
class PogDetails(DetailView):
    model = Pog
    template_name = 'pog_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = context['object']  
        pog_pr.check_pog_info(p.point_name)
        p = Pog.objects.get(slug = p.slug)
        map = None
        if p.latitude and p.longitude:
            map = folium.Map(location = (p.latitude, p.longitude),zoom_start=10)
            folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='blue',prefix='fa', icon='utensils')).add_to(map)
            map = map._repr_html_()
        context['pog'] = p
        context['map'] = map
        return context
    
class PoaDetails(DetailView):
    model = Poa
    template_name = 'poa_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = context['object']  
        poa_pr.check_poa_info(p.point_name)
        p = Poa.objects.get(slug = p.slug)
        map = None
        if p.latitude and p.longitude:
            map = folium.Map(location = (p.latitude, p.longitude),zoom_start=10)
            folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='orange',prefix='fa', icon='house')).add_to(map)
            map = map._repr_html_()
        context['poa'] = p
        context['map'] = map
        return context
    
