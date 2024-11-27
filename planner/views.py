from django.shortcuts import redirect, render
import folium
from geopy.distance import geodesic
from .models import Route, RouteDay, RouteDayActivity
from cities_light.models import City as CityBase
from users.models import TravelProfile
from services.models import City
from .prompts.planner_prompts import planner_route
from services.prompts.city_prompts import city_get_or_create
from django.contrib.auth.decorators import login_required 
from django.utils.translation import get_language, gettext_lazy as _


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
        
        res = planner_route(route = r)
        
        if res == False:
            profiles = TravelProfile.objects.filter(user = request.user)
            city_bases = CityBase.objects.all()
            return render(request, 'route.html', {'city_bases': city_bases, 'profiles': profiles, 'error': 'T'})
        
        return redirect('route_details', pk = r.pk)
    
    # GET
    profiles = TravelProfile.objects.filter(user = request.user)
    city_bases = CityBase.objects.all()
    return render(request, 'route.html', {'city_bases': city_bases, 'profiles': profiles, 'error': 'F'})


@login_required
def route_details(request, pk):

    route = Route.objects.filter(pk = pk)
        
    if len(route) <= 0:
        return render(request, '404.html')
    
    route = route[0]
    
    if (request.user != route.user):
        return render(request, '403.html')
    
    
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
    
    map = folium.Map(location=(destination.latitude, destination.longitude))
    point_locations = {}

    route.update_state()
    days = RouteDay.objects.filter(route = route).order_by('date')
    route_info = []
    for day in days:
        info_day = {}
        info_day['info'] = day
        
        point_locations[day.day] = []
        
        activities = RouteDayActivity.objects.filter(route_day = day, lang = get_language())
        morning_act = activities.filter(moment = 'M')
        info_day['morning'] = []
        for act in morning_act:
            if act.type == 'I':
                info_day['morning'].append(act.routedayactivityinterest)
                if (act.routedayactivityinterest.point.latitude != None and act.routedayactivityinterest.point.longitude != None):
                    p = act.routedayactivityinterest.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='green',prefix='fa', icon='landmark')).add_to(map)

            elif act.type == 'E':
                info_day['morning'].append(act.routedayactivityentertainment)
                if (act.routedayactivityentertainment.point.latitude != None and act.routedayactivityentertainment.point.longitude != None):
                    p = act.routedayactivityentertainment.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='red',prefix='fa', icon='ticket')).add_to(map)
            elif act.type == 'G':
                info_day['morning'].append(act.routedayactivitygastronomy)
                if (act.routedayactivitygastronomy.point.latitude != None and act.routedayactivitygastronomy.point.longitude != None):
                    p = act.routedayactivitygastronomy.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='blue',prefix='fa', icon='utensils')).add_to(map)   
            else:
                info_day['morning'].append(act)
                
        afternoon_act = activities.filter(moment = 'A')
        info_day['afternoon'] = []
        for act in afternoon_act:
            if act.type == 'I':
                info_day['afternoon'].append(act.routedayactivityinterest)
                if (act.routedayactivityinterest.point.latitude != None and act.routedayactivityinterest.point.longitude != None):
                    p = act.routedayactivityinterest.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='green',prefix='fa', icon='landmark')).add_to(map)
            elif act.type == 'E':
                info_day['afternoon'].append(act.routedayactivityentertainment)
                if (act.routedayactivityentertainment.point.latitude != None and act.routedayactivityentertainment.point.longitude != None):
                    p = act.routedayactivityentertainment.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='red',prefix='fa', icon='ticket')).add_to(map)
            elif act.type == 'G':
                info_day['afternoon'].append(act.routedayactivitygastronomy)
                if (act.routedayactivitygastronomy.point.latitude != None and act.routedayactivitygastronomy.point.longitude != None):
                    p = act.routedayactivitygastronomy.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='blue',prefix='fa', icon='utensils')).add_to(map)
            else:
                info_day['afternoon'].append(act)
        
        evening_act = activities.filter(moment = 'E')
        info_day['evening'] = []
        for act in evening_act:
            if act.type == 'I':
                info_day['evening'].append(act.routedayactivityinterest)
                if (act.routedayactivityinterest.point.latitude != None and act.routedayactivityinterest.point.longitude != None):
                    p = act.routedayactivityinterest.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='green',prefix='fa', icon='landmark')).add_to(map)
            elif act.type == 'E':
                info_day['evening'].append(act.routedayactivityentertainment)
                if (act.routedayactivityentertainment.point.latitude != None and act.routedayactivityentertainment.point.longitude != None):
                    p = act.routedayactivityentertainment.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='red',prefix='fa', icon='ticket')).add_to(map)
            elif act.type == 'G':
                info_day['evening'].append(act.routedayactivitygastronomy)
                if (act.routedayactivitygastronomy.point.latitude != None and act.routedayactivitygastronomy.point.longitude != None):
                    p = act.routedayactivitygastronomy.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='blue',prefix='fa', icon='utensils')).add_to(map)
            else:
                info_day['evening'].append(act)
        
        
        night_act = activities.filter(moment = 'N')
        info_day['night'] = []
        for act in night_act:
            if act.type == 'I':
                info_day['night'].append(act.routedayactivityinterest)
                if (act.routedayactivityinterest.point.latitude != None and act.routedayactivityinterest.point.longitude != None):
                    p = act.routedayactivityinterest.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='green',prefix='fa', icon='landmark')).add_to(map)
            elif act.type == 'E':
                info_day['night'].append(act.routedayactivityentertainment)
                if (act.routedayactivityentertainment.point.latitude != None and act.routedayactivityentertainment.point.longitude != None):
                    p = act.routedayactivityentertainment.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='red',prefix='fa', icon='ticket')).add_to(map)
            elif act.type == 'G':
                info_day['night'].append(act.routedayactivitygastronomy)
                if (act.routedayactivitygastronomy.point.latitude != None and act.routedayactivitygastronomy.point.longitude != None):
                    p = act.routedayactivitygastronomy.point
                    point_locations[day.day].append([p.latitude, p.longitude])
                    folium.Marker((p.latitude, p.longitude), popup = p.name, icon=folium.Icon(color='blue',prefix='fa', icon='utensils')).add_to(map)
            else:
                info_day['night'].append(act)
        
        route_info.append(info_day)
        
    colors = [
        '#0000FF',
        '#FF0000',
        '#00FF00', 
        '#FF00FF',
        '#00FFFF',
    ]
          
    for day in point_locations.items():
        distance = 0
        for i in range(0, len(day[1]) - 1):
            latitude1 = day[1][i][0]
            longitude1 = day[1][i][1]
            latitude2 = day[1][i + 1][0]
            longitude2 = day[1][i + 1][1]
            distance+= geodesic((latitude1, longitude1), (latitude2, longitude2)).kilometers
        
        folium.PolyLine(
        locations=day[1],
        color=colors[(day[0] - 1) % 5],
        weight=5,
        tooltip=_("Day") + " " + str(day[0]) + ". " + _("Distance") + " " + str(round(distance, 2)) + " " + "Km").add_to(map)
        
        
    if get_language() == 'es':
        poa = route.poa_es
        explanation = route.explanation_es
    else:
        poa = route.poa_en
        explanation = route.explanation_en
        
    if (poa != None and poa.latitude != None and poa.longitude != None):
        folium.Marker((poa.latitude, poa.longitude), popup = poa.name, icon=folium.Icon(color='orange',prefix='fa', icon='house')).add_to(map)
                
    context = {'route': route, 
               'route_info': route_info,
               'poa': poa,
               'explanation': explanation,
               'origin': origin,
               'destination': destination,
               'map': map._repr_html_(),
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

