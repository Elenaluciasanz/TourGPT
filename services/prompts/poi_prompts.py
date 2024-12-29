from .common_prompts import chat_gpt
from .point_info_prompts import check_point_info_info, check_point_info_presentation
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from services.models import Poi, poi_types
from cities_light.models import City as CityBase
from .city_prompts import city_get_or_create
from googletrans import Translator

template_recommendations = None
parser_recommendations = None
hist_recommendations = {}

trans = Translator()

def template_poi(parser, example, ex_city, ex_num, classification):
    format_instructions = parser.get_format_instructions()
    
    templ = PromptTemplate(
        template = """List {num} points of interest of {city}.
        Classify them using the classification {classification} and add the letter of the classification after the point name followed by '??'.
        {format_instructions}.
        Do not repeat answers. Previous points of interest: {hist}
        An example output for {ex_num} points of interest of {ex_city}: {example}""",
        input_variables = ["num", "city", "hist"],
        partial_variables = {"format_instructions": format_instructions, 
                             "classification": classification,
                             "ex_num": ex_num,
                             "ex_city": ex_city,
                             "example": example}
    )
    
    return templ

def init_template_recommendations():
    global template_recommendations, parser_recommendations
    
    example = "`Museo del Prado??M, Parque del Retiro??P, Plaza Mayor??S`"
    classification = poi_types()
    
    parser_recommendations = CommaSeparatedListOutputParser()
    template_recommendations = template_poi(parser_recommendations, example, "Madrid, Spain", 3, classification)

def poi_recommendations(num: int, c_en, c_oth):
    global template_recommendations, parser_recommendations, hist_recommendations, trans
    if not c_en.id in hist_recommendations:
        hist_recommendations[c_en.id] = []
        prev_poi = Poi.objects.filter(city_id = c_en.id, lang = 'en')
        for prev in prev_poi:
            hist_recommendations[c_en.id].append(prev.point_name)
            
    if len(hist_recommendations[c_en.id]) == 0:
        hist = ""
    else: 
        hist = str(hist_recommendations[c_en.id])

    input = template_recommendations.format_prompt(num = num, city = c_en.complete_name, hist = hist)
    output = chat_gpt(input.to_string())
    
    if output != "":
        try:
            resp = parser_recommendations.parse(output)
            for poi in resp:
                poi_split = poi.split('??')
                if not Poi.objects.filter(point_name = poi_split[0], city = c_en).exists():
                    p = Poi(point_name = poi_split[0],name = poi_split[0], type = poi_split[1] , city = c_en, lang = 'en')
                    p.save()
                    hist_recommendations[c_en.id].append(poi_split[0])
                    
                    for c in c_oth:
                        try:
                            name = trans.translate(p.point_name, src = p.lang, dest = 'es').text
                        except Exception as e:
                            name = p.point_name
                        p = Poi(point_name = poi_split[0], name = name, type = poi_split[1] , city = c, lang = c.lang)
                        p.save()
                      
        except Exception as e:
            print("Error while parsing poi_recommendations response")
            print(e)
        

def poi_history(p_en, p_oth):
    global trans 
    history = chat_gpt(f"As an expert tourist guide give a brief summary of the history of {p_en.complete_name} of 300 characters")
    p_en.history = history
    p_en.save()
    
    if p_en.history != "":
        for p in p_oth:
            try:
                p.history = trans.translate(p_en.history, src = p_en.lang, dest = p.lang).text
            except Exception as e:
                p.history = p_en.history
            p.save()
            
    
def poi_get_or_create(point_name: str, city: CityBase, type: str = 'O'):
    global hist_recommendations
    pois = Poi.objects.filter(point_name = point_name)
    
    if len(pois) <= 0:
        city_en, city_es = city_get_or_create(city.id)
        
        poi_en = Poi(point_name=point_name, city=city_en, lang='en', type = type)
        poi_en.save()
        poi_es = Poi(point_name=point_name, city=city_es, lang='es', type = type)
        poi_es.save()
        
        if not city_en.id in hist_recommendations:
            hist_recommendations[city_en.id] = []
            prev_poi = Poi.objects.filter(city_id = city_en.id, lang = 'en')
            for prev in prev_poi:
                hist_recommendations[city_en.id].append(prev.point_name)
            
        hist_recommendations[city_en.id].append(point_name)
        
        check_poi_presentation(point_name)
        
    else:
        poi_en = pois.get(lang= 'en')
        poi_es = pois.get(lang = 'es')
        
    return poi_en, poi_es   
    
    
def check_poi_presentation(point_name: str):
    poi_lang = Poi.objects.filter(point_name = point_name)
    poi_en = poi_lang.get(lang= 'en')
    poi_others = poi_lang.exclude(lang='en')
    check_point_info_presentation(poi_en, poi_others)
    
def check_poi_info(point_name: str):
    poi_lang = Poi.objects.filter(point_name = point_name)
    poi_en = poi_lang.get(lang= 'en')
    poi_others = poi_lang.exclude(lang='en')
    
    check_point_info_info(poi_en, poi_others)

    if poi_en.history == "":
        poi_history(poi_en, poi_others)
        

def get_hist_poi(city: CityBase):
    global hist_recommendations
    
    city_en, _ = city_get_or_create(city.id)
    if not city_en.id in hist_recommendations:
        hist_recommendations[city_en.id] = []
        prev_poi = Poi.objects.filter(city_id = city_en.id, lang = 'en')
        for prev in prev_poi:
            hist_recommendations[city_en.id].append(prev.point_name)
    
    if len(hist_recommendations[city_en.id]) > 0:
        return str(hist_recommendations[city_en.id])     
    
    return ""

# Inicializar plantillas
init_template_recommendations()