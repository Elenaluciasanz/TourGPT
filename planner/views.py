from django.shortcuts import redirect, render
from .models import Route, RouteDay, RouteDayActivity
from cities_light.models import City as CityBase
from users.models import TravelProfile
from services.models import City
from .prompts.planner_prompts import planner_route
from services.prompts.city_prompts import city_get_or_create
from django.contrib.auth.decorators import login_required 
from django.utils.translation import get_language


@login_required
def route_new(request):
    
    # POST
    if request.method == "POST":
        title = request.POST.get('title')
        user = request.user

        origin = int(request.POST.get('origin_id'))
        origin = CityBase.objects.get(pk = origin)
        profile_id = request.POST.get('adventure_level')
        profile = None
        if int(profile_id) > 0:
            profile = TravelProfile.objects.get(pk = int(profile_id))
        destination = int(request.POST.get('destination_id'))
        destination = CityBase.objects.get(pk = destination)
        start_date = request.POST.get('start_date') 
        end_date = request.POST.get('end_date')
        decr = request.POST.get('description')
        
        r = Route(title = title, user = user, start_date = start_date, end_date = end_date, origin = origin, 
                  destination = destination, description = decr, travel_profile = profile)
        r.save()
        
        planner_route(route = r)
        
        return redirect('route_details', pk = r.pk)
    
    # GET
    profiles = TravelProfile.objects.filter(user = request.user)
    city_bases = CityBase.objects.all()
    return render(request, 'route.html', {'city_bases': city_bases, 'profiles': profiles})


@login_required
def route_details(request, pk):

    route = Route.objects.filter(pk = pk)
        
    if len(route) <= 0:
        return render(request, '404.html')
    
    route = route[0]
    
    if (request.user != route.user):
        return render(request, '403.html')
    
    route.update_state()
    days = RouteDay.objects.filter(route = route).order_by('date')
    route_info = []
    for day in days:
        info_day = {}
        info_day['info'] = day
        
        activities = RouteDayActivity.objects.filter(route_day = day, lang = get_language())
        morning_act = activities.filter(moment = 'M')
        info_day['morning'] = []
        for act in morning_act:
            if act.type == 'I':
                info_day['morning'].append(act.routedayactivityinterest)
            elif act.type == 'E':
                info_day['morning'].append(act.routedayactivityentertainment)
            elif act.type == 'G':
                info_day['morning'].append(act.routedayactivitygastronomy)
            else:
                info_day['morning'].append(act)
                
        afternoon_act = activities.filter(moment = 'A')
        info_day['afternoon'] = []
        for act in afternoon_act:
            if act.type == 'I':
                info_day['afternoon'].append(act.routedayactivityinterest)
            elif act.type == 'E':
                info_day['afternoon'].append(act.routedayactivityentertainment)
            elif act.type == 'G':
                info_day['afternoon'].append(act.routedayactivitygastronomy)
            else:
                info_day['afternoon'].append(act)
        
        evening_act = activities.filter(moment = 'E')
        info_day['evening'] = []
        for act in evening_act:
            if act.type == 'I':
                info_day['evening'].append(act.routedayactivityinterest)
            elif act.type == 'E':
                info_day['evening'].append(act.routedayactivityentertainment)
            elif act.type == 'G':
                info_day['evening'].append(act.routedayactivitygastronomy)
            else:
                info_day['evening'].append(act)
        
        
        night_act = activities.filter(moment = 'N')
        info_day['night'] = []
        for act in night_act:
            if act.type == 'I':
                info_day['night'].append(act.routedayactivityinterest)
            elif act.type == 'E':
                info_day['night'].append(act.routedayactivityentertainment)
            elif act.type == 'G':
                info_day['night'].append(act.routedayactivitygastronomy)
            else:
                info_day['night'].append(act)
        
        route_info.append(info_day)
        
    if get_language() == 'es':
        poa = route.poa_es
    else:
        poa = route.poa_en
        
    origin = City.objects.filter(city_id = route.origin.id, lang = get_language())
    if len(origin) <= 0:
        city_en, city_es = city_get_or_create(city_id = route.origin.id)
        if (get_language() == 'es'):
            origin = city_es
        else:
            origin = city_en
    else:
        origin = origin[0]
    
    destination = City.objects.filter(city_id = route.destination.id, lang = get_language())
    if len(destination) <= 0:
        city_en, city_es = city_get_or_create(city_id = route.destination.id)
        if (get_language() == 'es'):
            destination = city_es
        else:
            destination = city_en
    else:
        destination = destination[0]
        
    context = {'route': route, 
               'route_info': route_info,
               'poa': poa,
               'origin': origin,
                'destination': destination,
               }
    
    return render(request, 'route_details.html', context)


@login_required
def route_list(request):
    
    routes = Route.objects.filter(user = request.user)
    
    for route in routes:
        route.update_state()
    context = {
        'routes': routes,
    } 

    return render(request, 'route_list.html', context)


@login_required
def route_cancel(request, pk):
    route = Route.objects.get(pk = pk)
    
    if (request.user != route.user):
        return render(request, '403.html')
    
    route.state = 'C'
    route.save()                   
    return redirect('route_list')

