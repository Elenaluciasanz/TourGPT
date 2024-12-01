from services.constants import SPARQL_ENDPOINT
from .common_prompts import chat_gpt
from geopy.geocoders import Nominatim
from googletrans import Translator
import requests

trans = Translator()

def point_info_location(p_en, p_oth): 
    try:
        geo = Nominatim(user_agent = "geopy")
        location = geo.geocode(p_en.complete_name)
        if location:
            p_en.location = location.address
            p_en.longitude = location.longitude
            p_en.latitude = location.latitude
            p_en.save()            
            for p in p_oth:
                try:
                    p.location = trans.translate(p_en.location, src = p_en.lang, dest = p.lang).text
                except Exception as e:
                    p.location = p_en.location
                p.longitude = p_en.longitude
                p.latitude = p_en.latitude
                p.save()        
        else:
            p_en.location = "NF"
            p_en.save()  
            for p in p_oth:
                p.location = "NF"
                p.save()   
    except Exception as e:
        print("Error while connecting with Geopy, Nominantim.")
        print(e)

def point_info_presentation(p_en, p_oth): 
    presentation = chat_gpt(f"Brief presentation of {p_en.complete_name} of 100 characters. It must be attractive. Includes emojis.")
    p_en.presentation = presentation
    p_en.save()
    
    if p_en.presentation != "":
        for p in p_oth:
            try:
                p.presentation = trans.translate(p_en.presentation, src = p_en.lang, dest = p.lang).text
            except Exception as e:
                p.presentation = p_en.presentation
            p.save()

def point_info_price_avg(p_en, p_oth): 
    price_avg = chat_gpt(f"Approximate average price of {p_en.complete_name}")
    p_en.price_avg = price_avg
    p_en.save()
    
    if p_en.price_avg != "":
        for p in p_oth:
            try:
                p.price_avg = trans.translate(p_en.price_avg, src = p_en.lang, dest = p.lang).text
            except Exception as e:
                p.price_avg = p_en.price_avg
            p.save()
    
def point_info_shedule_avg(p_en, p_oth): 
    shedule_avg = chat_gpt(f"Approximate average schedule of {p_en.complete_name}")
    p_en.shedule_avg = shedule_avg
    p_en.save()
    
    if p_en.shedule_avg != "":
        for p in p_oth:
            try:
                p.shedule_avg = trans.translate(p_en.shedule_avg, src = p_en.lang, dest = p.lang).text
            except Exception as e:
                p.shedule_avg = p_en.shedule_avg
            p.save()

def point_info_image_url(p_en, p_oth): 
    dbpedia_url = chat_gpt(f"Give me the dbpedia URL of the resource associated with {p_en.complete_name}. Provide only the URL. Do not provide any additional text to the URL.")
    print(dbpedia_url)
    
    dbpedia_url = dbpedia_url.replace("page", "resource")
    
    # Consulta SPARQL para obtener la entidad y la imagen
    query = """
    SELECT ?thumbnail WHERE {            
        <""" + dbpedia_url + """> dbo:thumbnail ?thumbnail.
    }
    """
    # Parámetros para la consulta
    params = {
        'query': query,
        'format': 'application/json'
    }
    
    # Realizamos la consulta SPARQL
    response = requests.get(SPARQL_ENDPOINT, params=params)
        
    if response.status_code == 200:
        data = response.json()
        if data['results']['bindings']:
            # Si encontramos un resultado, extraemos la URI de la entidad y la URL de la imagen
            # entidad_uri = data['results']['bindings'][0]['entity']['value']
            image_url = data['results']['bindings'][0]['thumbnail']['value']
       
            if image_url:
                p_en.image_url = image_url
                p_en.save()
            
                for p in p_oth:
                    p.image_url = image_url
                    p.save()
    

def check_point_info_presentation(p_en, p_oth):
    if p_en.location == "":
        point_info_location(p_en, p_oth)
        
    if p_en.presentation == "":
        point_info_presentation(p_en, p_oth)
    
    if p_en.image_url == None or p_en.image_url == "":
        point_info_image_url(p_en, p_oth)

   
def check_point_info_info(p_en, p_oth):
    check_point_info_presentation(p_en, p_oth)

    if p_en.price_avg == "":
        point_info_price_avg(p_en, p_oth) 
        
    if p_en.shedule_avg == "":
        point_info_shedule_avg(p_en, p_oth)
