from .common_prompts import chat_gpt
from geopy.geocoders import Nominatim
from googletrans import Translator

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
                p.location = trans.translate(p_en.location, src = p_en.lang, dest = p.lang).text
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
            p.presentation = trans.translate(p_en.presentation, src = p_en.lang, dest = p.lang).text
            p.save()

def point_info_price_avg(p_en, p_oth): 
    price_avg = chat_gpt(f"Approximate average price of {p_en.complete_name}")
    p_en.price_avg = price_avg
    p_en.save()
    
    if p_en.price_avg != "":
        for p in p_oth:
            p.price_avg = trans.translate(p_en.price_avg, src = p_en.lang, dest = p.lang).text
            p.save()
    
def point_info_shedule_avg(p_en, p_oth): 
    shedule_avg = chat_gpt(f"Approximate average schedule of {p_en.complete_name}")
    p_en.shedule_avg = shedule_avg
    p_en.save()
    
    if p_en.shedule_avg != "":
        for p in p_oth:
            p.shedule_avg = trans.translate(p_en.shedule_avg, src = p_en.lang, dest = p.lang).text
            p.save()

def check_point_info_presentation(p_en, p_oth):
    if p_en.location == "":
        point_info_location(p_en, p_oth)
        
    if p_en.presentation == "":
        point_info_presentation(p_en, p_oth)

   
def check_point_info_info(p_en, p_oth):
    check_point_info_presentation(p_en, p_oth)

    if p_en.price_avg == "":
        point_info_price_avg(p_en, p_oth) 
        
    if p_en.shedule_avg == "":
        point_info_shedule_avg(p_en, p_oth)
