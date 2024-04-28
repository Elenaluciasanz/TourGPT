import ast
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, TravelProfileForm
from .models import TravelProfile, User, REASON_LIST, ADVENTURE_LEVELS_LIST
from services.models import Country, City, Poi, Poe, Poa, Pog
from services.models import POI_TYPES, POE_TYPES, POG_TYPES, POA_TYPES
from django.utils.translation import get_language

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def validate_username(request):
    username = request.GET.get('username', None)
    if username is not None:
        data = {
            'is_taken': User.objects.filter(username__iexact=username).exists()
        }
        return JsonResponse(data)
    return JsonResponse({'is_taken': True})


def validate_email(request):
    email = request.GET.get('email', None)
    if email is not None:
        data = {
            'is_taken': User.objects.filter(email__iexact=email).exists()
        }
        return JsonResponse(data)
    return JsonResponse({'is_taken': True})
        

@login_required 
def travel_profile_new(request, pk):
    if request.method == "POST":
        form = TravelProfileForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.reason = form.cleaned_data['reason_selection']
            f.pref_poi = form.cleaned_data['poi_selection']
            f.pref_poe = form.cleaned_data['poe_selection']
            f.pref_pog = form.cleaned_data['pog_selection']
            f.pref_poa = form.cleaned_data['poa_selection']
            f.save()
            return redirect('account_details', pk = request.user.pk)
    else:
        form = TravelProfileForm()
        
    context = {
        'form': form,
        'REASON_LIST': REASON_LIST,
        'POI_TYPES': POI_TYPES,
        'POE_TYPES': POE_TYPES,
        'POG_TYPES': POG_TYPES,
        'POA_TYPES': POA_TYPES,
        'ADVENTURE_LEVELS_LIST': ADVENTURE_LEVELS_LIST,
    }
    
    return render(request, 'travel_profile_editor.html', context=context)

@login_required
def travel_profile_list(request, pk):
    profiles = TravelProfile.objects.filter(user = request.user)
    return render(request, 'travel_profile_list.html', {'travel_profiles': profiles})


class AccountView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'account_details.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['travel_profiles'] = TravelProfile.objects.filter(user = self.request.user)
        return ctx


@login_required  
def travel_profile_view(request, pk, acc):
    
    travel_profile = TravelProfile.objects.get(pk = pk)
    if (request.user != travel_profile.user):
        return render(request, '403.html')
    
    ctx = {}
    ctx['object'] = travel_profile
    ctx['reasons'] = ast.literal_eval(travel_profile.reason)
    ctx['pref_poi'] = ast.literal_eval(travel_profile.pref_poi)
    ctx['pref_poe'] = ast.literal_eval(travel_profile.pref_poe)
    ctx['pref_pog'] = ast.literal_eval(travel_profile.pref_pog)
    ctx['pref_poa'] = ast.literal_eval(travel_profile.pref_poa)
    
    ctx['REASON_LIST'] = REASON_LIST
    ctx['POI_TYPES'] = POI_TYPES
    ctx['POE_TYPES'] = POE_TYPES
    ctx['POG_TYPES'] = POG_TYPES
    ctx['POA_TYPES'] = POA_TYPES
    ctx['ADVENTURE_LEVELS_LIST'] = ADVENTURE_LEVELS_LIST
        
    return render(request, 'travel_profile_details.html', context = ctx)
    
    
@login_required  
def travel_profile_update(request, acc, pk):
    travel_profile = TravelProfile.objects.get(pk = pk)
    
    if (request.user != travel_profile.user):
        return render(request, '403.html')
    
    if request.method == "POST":
        
        form = TravelProfileForm(request.POST, instance = travel_profile)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.reason = form.cleaned_data['reason_selection']
            f.pref_poi = form.cleaned_data['poi_selection']
            f.pref_poe = form.cleaned_data['poe_selection']
            f.pref_pog = form.cleaned_data['pog_selection']
            f.pref_poa = form.cleaned_data['poa_selection']
            f.save()
            return redirect('account_details', pk = request.user.pk)
    else:
        form = TravelProfileForm(instance = travel_profile)
        
    context = {
        'form': form,
        'reasons': ast.literal_eval(travel_profile.reason),
        'pref_poi': ast.literal_eval(travel_profile.pref_poi),
        'pref_poe': ast.literal_eval(travel_profile.pref_poe),
        'pref_pog': ast.literal_eval(travel_profile.pref_pog),
        'pref_poa': ast.literal_eval(travel_profile.pref_poa),
        'REASON_LIST': REASON_LIST,
        'POI_TYPES': POI_TYPES,
        'POE_TYPES': POE_TYPES,
        'POG_TYPES': POG_TYPES,
        'POA_TYPES': POA_TYPES,
        'ADVENTURE_LEVELS_LIST': ADVENTURE_LEVELS_LIST,
    }
    
    return render(request, 'travel_profile_editor.html', context=context)


@login_required
def travel_profile_delete(request, acc, pk):
    travel_profile = TravelProfile.objects.get(pk = pk)
    if (request.user != travel_profile.user):
        return render(request, '403.html')
    travel_profile.delete()
    return redirect('account_details', pk = request.user.pk)
        

class CountriesFavListView(LoginRequiredMixin, ListView):
    model = Country
    context_object_name = 'countries'
    template_name = 'fav_countries.html'

    def get_queryset(self):
        return self.request.user.fav_countries.filter(lang = get_language())
    

class CitiesFavListView(LoginRequiredMixin, ListView):
    model = City
    context_object_name = 'cities'
    template_name = 'fav_cities.html'

    def get_queryset(self):
        return self.request.user.fav_cities.filter(lang = get_language())


class PoisFavListView(LoginRequiredMixin, ListView):
    model = Poi
    context_object_name = 'pois'
    template_name = 'fav_pois.html'

    def get_queryset(self):
        return self.request.user.fav_pois.filter(lang = get_language())
    
    
class PoesFavListView(LoginRequiredMixin, ListView):
    model = Poe
    context_object_name = 'poes'
    template_name = 'fav_poes.html'

    def get_queryset(self):
        return self.request.user.fav_poes.filter(lang = get_language())
    
class PogsFavListView(LoginRequiredMixin, ListView):
    model = Pog
    context_object_name = 'pogs'
    template_name = 'fav_pogs.html'

    def get_queryset(self):
        return self.request.user.fav_pogs.filter(lang = get_language())
    
class PoasFavListView(LoginRequiredMixin, ListView):
    model = Poa
    context_object_name = 'poas'
    template_name = 'fav_poas.html'

    def get_queryset(self):
        return self.request.user.fav_poas.filter(lang = get_language())


@login_required
def country_like(request):
    country = request.GET['country']
    countries = Country.objects.filter(country_id = country)
    if countries[0] in request.user.fav_countries.all():
        for c in countries: request.user.fav_countries.remove(c)
    else:
        for c in countries: request.user.fav_countries.add(c)
        
    request.user.save()
    return JsonResponse({})


@login_required
def city_like(request):
    city = request.GET['city']
    cities = City.objects.filter(city_id = city)
    if cities[0] in request.user.fav_cities.all():
        for c in cities: request.user.fav_cities.remove(c)
    else:
        for c in cities: request.user.fav_cities.add(c)
        
    request.user.save()
    return JsonResponse({})

@login_required
def poi_like(request):
    poi = request.GET['poi']
    pois = Poi.objects.filter(point_name = poi)
    if pois[0] in request.user.fav_pois.all():
        for p in pois: request.user.fav_pois.remove(p)
    else:
        for p in pois: request.user.fav_pois.add(p)
        
    request.user.save()
    return JsonResponse({})

@login_required
def poe_like(request):
    poe = request.GET['poe']
    poes = Poe.objects.filter(point_name = poe)
    if poes[0] in request.user.fav_poes.all():
        for p in poes: request.user.fav_poes.remove(p)
    else:
        for p in poes: request.user.fav_poes.add(p)
        
    request.user.save()
    return JsonResponse({})

@login_required
def pog_like(request):
    pog = request.GET['pog']
    pogs = Pog.objects.filter(point_name = pog)
    if pogs[0] in request.user.fav_pogs.all():
        for p in pogs: request.user.fav_pogs.remove(p)
    else:
        for p in pogs: request.user.fav_pogs.add(p)
        
    request.user.save()
    return JsonResponse({})

@login_required
def poa_like(request):
  
    poa = request.GET['poa']
    poas = Poa.objects.filter(point_name = poa)
    if poas[0] in request.user.fav_poas.all():
        for p in poas: request.user.fav_poas.remove(p)
    else:
        for p in poas: request.user.fav_poas.add(p)
        
    request.user.save()
    return JsonResponse({})

            
