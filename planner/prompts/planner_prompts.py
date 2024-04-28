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
import json

template_route = None
trans = Translator()
                          
def init_template_route():
    global template_route

    ex_days = 2
    ex_city = "Madrid, Spain"
    example = """
    {
        "accommodation": "Hotel Ritz Madrid??HO",
        "route": {
            "1": {
                "presentation": "Arrival and Exploration",
                "morning": {
                    "activity": "Start your day with a visit to the Royal Palace of Madrid to explore its stunning architecture and history",
                    "point": "Royal Palace of Madrid??I??E"
                },
                "afternoon": {
                    "activity": "Enjoy traditional Spanish dishes in a historic setting",
                    "point": "La Carmencita??G??R"
                },
                "evening": {
                    "activity": "Enjoy a leisurely stroll through Retiro Park, where you can relax by the lake or wander through the beautiful gardens",
                    "point": "Retiro Park??I??P"
                },
                "night": {
                    "activity": "Have dinner at a Michelin-starred restaurant for a memorable dining experience",
                    "point": "DiverXO??G??R"
                }
            },
            "2": {
                "presentation": "Gastronomic Delights and Entertainment",
                "morning": {
                    "activity": "Explore the historic neighborhood of Lavapiés, known for its multicultural atmosphere and street art"
                },
                "afternoon": {
                    "activity": "Casa Revuelta - Try their famous cod fritters and other traditional Spanish tapas",
                    "point": "Casa Revuelta??G??R"
                },
                "evening": {
                    "activity": "Enjoy a game of bowling at Bowling Chamartín, a popular bowling alley in Madrid",
                    "point": "Bowling Chamartín??E??B"
                },
                "night": {
                    "activity": "Head back to your accommodation to pack and prepare for your departure the next day"
                }
            }
        }
    }
    """
    
    templ = PromptTemplate(
        template = """Return a JSON object with the route for {days} days in {city}.
        The route is designed to provide a balance of cultural exploration, gastronomic delights, and entertainment.
        For each day include a short presentation of 3/5 words to set the tone for the experience.
        Each day is divided into 4 parts: morning, afternoon, evening, and night.
        Each part includes a suggested activity and, if applicable, the name of the point to visit.
        Each point is classified as either an interest site (I) or an experience/Entertainment (E) or a gastronomic site (G).
        Each interest site is classified  as {poi_types}.
        Each entertainment site is classified as {poe_types}.
        Each gastronomic site is classified as {pog_types}.
        Suggest an accommodation point for the full duration of the route.
        The accommodation point is classified as {poa_types}.
        Point's name should unique, so if the point already exists, return the name of the existing point.
        Previous points of interest: {hist_poi}, entertainment: {hist_poe}, gastronomy: {hist_pog}, accommodation: {hist_poa}.
        {travel_profile}
        An example of the JSON object for {ex_days} in {ex_city} is provided below.
        {example}""",
        input_variables = ["hist_poi", "hist_poe", "hist_pog", "hist_poa", "days", "city", "travel_profile"],
        partial_variables = {"poi_types": poi_types(),
                            "poe_types": poe_types(),
                            "pog_types": pog_types(),
                            "poa_types": poa_types(),
                            "ex_days": ex_days,
                            "ex_city": ex_city,
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
    
    if route.travel_profile is not None:
        travel_profile = "Choose points based on the following travel profile:\n"
        travel_profile += str(route.travel_profile )
        travel_profile += ".\n"
  
    else:
        travel_profile = ""
    
    
    input = template_route.format_prompt(hist_poi = hist_poi, hist_poe = hist_poe, hist_pog = hist_pog, 
                                         hist_poa = hist_poa, days = days, city = city.display_name,
                                         travel_profile = travel_profile)

    output = chat_gpt(input.to_string())

    if output != "":
        try:
            resp = json.loads(output)
            
            accommodation = resp["accommodation"]
            accommodation = accommodation.split("??")
            poa_en, poa_es = poa_get_or_create(accommodation[0], city, accommodation[1])
            route.poa_en = poa_en
            route.poa_es = poa_es
            route.save()
            
            for day in resp["route"]:
                d = RouteDay(route = route, date = route.start_date + timedelta(days = int(day) - 1), day = int(day), presentation = resp["route"][day]["presentation"])
                d.presentation_es = trans.translate(d.presentation, src = 'en', dest = 'es').text
                d.save()
                         
                for moment in [('morning', 'M'), ('afternoon', 'A'), ('evening','E'), ('night','N')]:
                    activity = resp["route"][day][moment[0]]["activity"]
                    act = trans.translate(activity, src = 'en', dest = 'es').text
                    
                    if "point" in resp["route"][day][moment[0]]:
                        point = resp["route"][day][moment[0]]["point"]
                        point = point.split("??")
                        point_name = point[0]
                        type = point[1]
                        type_point = point[2]

                        # Punto de Interés
                        if type == 'I':
                            poi_en, poi_es = poi_get_or_create(point_name, city, type_point)
                            RouteDayActivityInterest(route_day = d, activity = activity, moment = moment[1], type = 'I', lang = 'en', point = poi_en).save()
                            RouteDayActivityInterest(route_day = d, activity = act, moment = moment[1], type = 'I', lang = 'es', point = poi_es).save()
                            
                        # Punto de Entretenimiento   
                        elif type == 'E':
                            poe_en, poe_es = poe_get_or_create(point_name, city, type_point)
                            RouteDayActivityEntertainment(route_day = d, activity = activity, moment = moment[1], type = 'E', lang = 'en', point = poe_en).save()
                            RouteDayActivityEntertainment(route_day = d, activity = act, moment = moment[1], type = 'E', lang = 'es', point = poe_es).save()
                        
                        # Punto Gastronómico
                        elif type == 'G':
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
        
        except Exception as e:
            print("Error while parsing route planner response")
            print(e)
    
    
def check_route_info():
    # Comprobar info pais, ciudades y puntos de la ruta
    pass

     
# Inicializar plantilla
init_template_route()