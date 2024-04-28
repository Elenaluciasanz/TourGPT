from .common_prompts import chat_gpt
from services.models import Country, City
from cities_light.models import City as CityBase
from googletrans import Translator
from .country_prompts import country_get_or_create

trans = Translator()
    
def city_languages(c_en, c_oth):
    global trans 
    languages = chat_gpt(f"Common spoken languages of {c_en.complete_name}. An example output for city Barcelona,Spain: Spanish (official), Catalan, French, English")
    c_en.languages = "Languages: " + languages
    c_en.save()
    
    if c_en.presentation != "":
        for c in c_oth:
            c.languages = trans.translate(c_en.languages, src = c_en.lang, dest = c.lang).text
            c.save()

def city_presentation(c_en, c_oth):
    global trans
    presentation = chat_gpt(f"Brief presentation of {c_en.complete_name} of 200 characters")
    c_en.presentation = presentation
    c_en.save()
    
    if c_en.presentation != "":
        for c in c_oth:
            c.presentation = trans.translate(c_en.presentation, src = c_en.lang, dest = c.lang).text
            c.save()

def city_history(c_en, c_oth):
    global trans
    history = chat_gpt(f"Brief summary of the history of {c_en.complete_name} of 500 characters")
    c_en.history = history
    c_en.save()
    
    if c_en.history != "":
        for c in c_oth:
            c.history = trans.translate(c_en.history, src = c_en.lang, dest = c.lang).text
            c.save()
    
def city_curiosities(c_en, c_oth):
    global trans
    curiosities = chat_gpt(f"Three curiosities of {c_en.complete_name}")
    c_en.curiosities = curiosities
    c_en.save()
    
    if c_en.curiosities != "":
        for c in c_oth:
            c.curiosities = trans.translate(c_en.curiosities, src = c_en.lang, dest = c.lang).text
            c.save()

def city_get_or_create(city_id: int):
    cities = City.objects.filter(city_id = city_id)
    
    if len(cities) <= 0:
        city_base = CityBase.objects.get(id = city_id)
        country_en, country_es = country_get_or_create(city_base.country_id)
        
        city_en = City(city_id = city_id, country_id = country_en.id, lang = 'en')
        city_en.save()
        city_es = City(city_id = city_id, country_id = country_es.id, lang = 'es')
        city_es.save()
        
        check_city_presentation(city_id)
        
    else:
        city_en = cities.get(lang = 'en')
        city_es = cities.get(lang = 'es')
        
    return city_en, city_es   
        

def check_city_presentation(city_id: int):
    city_lang = City.objects.filter(city_id = city_id)
    city_en = city_lang.get(lang= 'en')
    city_others = city_lang.exclude(lang='en')
    
    if city_en.presentation == "":
        city_presentation(city_en, city_others)
    
    
def check_city_info(city_id: int):
    city_lang = City.objects.filter(city_id = city_id)
    city_en = city_lang.get(lang= 'en')
    city_others = city_lang.exclude(lang='en')
    
    check_city_presentation(city_id)

    if city_en.languages == "":
        city_languages(city_en, city_others) 
        
    if city_en.history == "":
        city_history(city_en, city_others)
        
    if city_en.curiosities == "":
        city_curiosities(city_en, city_others)