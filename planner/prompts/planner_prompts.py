from datetime import timedelta
from services.prompts.common_prompts import chat_gpt
from langchain.prompts import PromptTemplate
from planner.models import Route, RouteDay, RouteDayActivity, RouteDayActivityInterest, RouteDayActivityEntertainment, RouteDayActivityGastronomy
from services.models import poi_types, poe_types, poa_types, pog_types
from services.prompts.poi_prompts import poi_get_or_create, get_hist_poi
from services.prompts.poe_prompts import poe_get_or_create, get_hist_poe
from services.prompts.poa_prompts import poa_get_or_create, get_hist_poa
from services.prompts.pog_prompts import pog_get_or_create, get_hist_pog
from googletrans import Translator
from django.db import transaction
import json

template_route = None
trans = Translator()
                          
def init_template_route():
    global template_route

    ex_days = 2
    ex_city = "Madrid, Spain"
    ex_profile = """
    Adults: 2
    Children: 1
    Reason: Family Vacation, Turism
    Adventure Level: Medium
    Favorite interest points: Emblematic Site, Park/Garden
    Favorite entertainment points: Bowling Alley
    Favorite gastronomy points: Restaurant
    Favorite accommodation points: Hotel
    Observations: We love spending time outdoors and enjoying nature. We would like to visit historical places and try local cuisine.
    """
    example = """
    {
        "accommodation": {
            "point": "Hotel Ritz Madrid",
            "subclass": "HO"  
        },
        "route": {
            "1": {
                "presentation": "Arrival and Exploration",
                "morning": {
                    "activity": "Start your day with a visit to the Royal Palace of Madrid to explore its stunning architecture and history",
                    "point": "Royal Palace of Madrid",
                    "class": "I",
                    "subclass": "E"
                },
                "afternoon": {
                    "activity": "Enjoy traditional Spanish dishes in a historic setting",
                    "point": "La Carmencita",
                    "class": "G",
                    "subclass": "R"
                },
                "evening": {
                    "activity": "Enjoy a leisurely stroll through Retiro Park, where you can relax by the lake or wander through the beautiful gardens",
                    "point": "Retiro Park",
                    "class": "I",
                    "subclass": "P"
                },
                "night": {
                    "activity": "Have dinner at a Michelin-starred restaurant for a memorable dining experience",
                    "point": "DiverXO",
                    "class": "G",
                    "subclass": "R"
                }
            },
            "2": {
                "presentation": "Gastronomic Delights and Entertainment",
                "morning": {
                    "activity": "Explore the historic neighborhood of Lavapiés, known for its multicultural atmosphere and street art"
                },
                "afternoon": {
                    "activity": "Casa Revuelta - Try their famous cod fritters and other traditional Spanish tapas",
                    "point": "Casa Revuelta",
                    "class": "G",
                    "subclass": "R"
                },
                "evening": {
                    "activity": "Enjoy a game of bowling at Bowling Chamartín, a popular bowling alley in Madrid",
                    "point": "Bowling Chamartín",
                    "class": "E",
                    "subclass": "B"
                },
                "night": {
                    "activity": "Head back to your accommodation to pack and prepare for your departure the next day"
                }
            }
        },
        "explanation": "This itinerary is perfect for a family of two adults and one child, offering a mix of cultural experiences, family-friendly activities, and culinary delights. Retiro Park provides ample space for the kids to run around while you enjoy the tranquil surroundings. A visit to the Royal Palace of Madrid adds a touch of royalty to your trip, with its grandeur and picturesque gardens. In addition, both children and adults would enjoy an afternoon with the family playing bowling."
    }
    """
    
    templ = PromptTemplate(
        template = """Return a JSON object with the route for {days} days in {city}.
        The route is designed to provide a balance of cultural exploration, gastronomic delights, and entertainment.
        For each day include a short presentation of 3/5 words to set the tone for the experience.
        Each day is divided into 4 parts: morning, afternoon, evening, and night.
        Each part includes a suggested activity and, if applicable, the name of the point to visit.
        Each point is classified as either an interest site (I) or an experience/Entertainment (E) or a gastronomic site (G).
        Each interest site is subclassified  as {poi_types}.
        Each entertainment site is subclassified as {poe_types}.
        Each gastronomic site is subclassified as {pog_types}.
        Suggest an accommodation point for the full duration of the route.
        The accommodation point is subclassified as {poa_types}.
        Point's name should unique, so if the point already exists, return the name of the existing point.
        Previous points of interest: {hist_poi}, entertainment: {hist_poe}, gastronomy: {hist_pog}, accommodation: {hist_poa}.
        If a travel profile is given, choose points based on the profile and include in the json an explanation of why the itinerary is perfect for the profile.
        Travel Profile: {travel_profile}
        An example of the JSON object for {ex_days} in {ex_city} and the travel profile: {ex_profile} ,is provided below.
        {example}""",
        input_variables = ["hist_poi", "hist_poe", "hist_pog", "hist_poa", "days", "city", "travel_profile"],
        partial_variables = {"poi_types": poi_types(),
                            "poe_types": poe_types(),
                            "pog_types": pog_types(),
                            "poa_types": poa_types(),
                            "ex_days": ex_days,
                            "ex_city": ex_city,
                            "ex_profile": ex_profile,
                            "example": example}
    )
    
    template_route = templ
    return

def get_hist_points(city):
    hist_poi = get_hist_poi(city)
    hist_poe = get_hist_poe(city)
    hist_pog = get_hist_pog(city)
    hist_poa = get_hist_poa(city)
    return hist_poi, hist_poe, hist_pog, hist_poa


def planner_route(route: Route):
    global template_route, trans
    city = route.destination
    days = route.days
    
    hist_poi, hist_poe, hist_pog, hist_poa = get_hist_points(city)
    
    travel_profile=""
    if route.travel_profile is not None:
        travel_profile += str(route.travel_profile)
  
    else:
        travel_profile = "No travel profile."
    
    input = template_route.format_prompt(hist_poi = hist_poi, hist_poe = hist_poe, hist_pog = hist_pog, 
                                         hist_poa = hist_poa, days = days, city = city.display_name,
                                         travel_profile = travel_profile)

    output = chat_gpt(input.to_string())
        
    if output != "":
        try:
            resp = json.loads(output)
            with transaction.atomic():
                if "accommodation" in resp:                
                    if "point" in resp["accommodation"]:
                        point = resp["accommodation"]["point"]
                        if "subclass" in resp["accommodation"]:
                            subclass = resp["accommodation"]["subclass"]
                        else:
                            subclass = "O"
                        
                        poa_en, poa_es = poa_get_or_create(point, city, subclass)
                    
                        route.poa_en = poa_en
                        route.poa_es = poa_es
                        route.save()
                
                for day in resp["route"]:
                    if "presentation" in resp["route"][day]:
                        presentation = resp["route"][day]["presentation"]
                    else:
                        presentation = "Day " + day 
                    d = RouteDay(route = route, date = route.start_date + timedelta(days = int(day) - 1), day = int(day), presentation = presentation)
                    d.presentation_es = trans.translate(d.presentation, src = 'en', dest = 'es').text
                    d.save()
                            
                    for moment in [('morning', 'M'), ('afternoon', 'A'), ('evening','E'), ('night','N')]:
                        if moment[0] in resp["route"][day] and "activity" in resp["route"][day][moment[0]]:
                        
                            activity = resp["route"][day][moment[0]]["activity"]
                            act = trans.translate(activity, src = 'en', dest = 'es').text
                            
                            if "point" in resp["route"][day][moment[0]]:
                                point_name = resp["route"][day][moment[0]]["point"]
                                
                                if "class" in resp["route"][day][moment[0]]:
                                    type = resp["route"][day][moment[0]]["class"]
                                    
                                    if "subclass" in resp["route"][day][moment[0]]:
                                        type_point = resp["route"][day][moment[0]]["subclass"]
                                    else:
                                        type_point = "O"
                                else:
                                    type = "O"
                                    type_point = "O"
                                
                                # Punto de Interés
                                if type == "I":
                                    poi_en, poi_es = poi_get_or_create(point_name, city, type_point)
                                    RouteDayActivityInterest(route_day = d, activity = activity, moment = moment[1], type = 'I', lang = 'en', point = poi_en).save()
                                    RouteDayActivityInterest(route_day = d, activity = act, moment = moment[1], type = 'I', lang = 'es', point = poi_es).save()
                                    
                                # Punto de Entretenimiento   
                                elif type == "E":
                                    poe_en, poe_es = poe_get_or_create(point_name, city, type_point)
                                    RouteDayActivityEntertainment(route_day = d, activity = activity, moment = moment[1], type = 'E', lang = 'en', point = poe_en).save()
                                    RouteDayActivityEntertainment(route_day = d, activity = act, moment = moment[1], type = 'E', lang = 'es', point = poe_es).save()
                                
                                # Punto Gastronómico
                                elif type == "G":
                                    pog_en, pog_es = pog_get_or_create(point_name, city, type_point)
                                    RouteDayActivityGastronomy(route_day = d, activity = activity, moment = moment[1], type = 'G', lang = 'en', point = pog_en).save() 
                                    RouteDayActivityGastronomy(route_day = d, activity = act, moment = moment[1], type = 'G', lang = 'es', point = pog_es).save()
                                else:
                                    RouteDayActivity(route_day = d, activity = activity, moment = moment[1], type = 'O', lang = 'en').save() 
                                    RouteDayActivity(route_day = d, activity = act, moment = moment[1], type = 'O', lang = 'es').save()
                            
                            # Actividad Genérica    
                            else:
                                RouteDayActivity(route_day = d, activity = activity, moment = moment[1], type = 'O', lang = 'en').save() 
                                RouteDayActivity(route_day = d, activity = act, moment = moment[1], type = 'O', lang = 'es').save()
                
                if "explanation" in resp:
                    route.explanation_en = resp["explanation"]
                    route.explanation_es = trans.translate(resp["explanation"], src = 'en', dest = 'es').text
                    route.save()
                    
        except Exception as e:
            print("Error while parsing route planner response")
            print(e)
            route.delete()
            return False
        
    return True
     
# Inicializar plantilla
init_template_route()