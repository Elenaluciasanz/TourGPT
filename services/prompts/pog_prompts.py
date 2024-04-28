from .common_prompts import chat_gpt
from .point_info_prompts import check_point_info_info, check_point_info_presentation
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from services.models import Pog, pog_types
from cities_light.models import City as CityBase
from .city_prompts import city_get_or_create
from googletrans import Translator

template_recommendations = None
parser_recommendations = None
hist_recommendations = {}

trans = Translator()

def template_pog(parser, example, ex_city, ex_num, classification):
    format_instructions = parser.get_format_instructions()
    
    templ = PromptTemplate(
        template = """List {num} gastronomy points of {city}.
        Classify them using the classification {classification} and add the letter of the classification after the point name followed by '??'.
        {format_instructions}.
        Do not repeat answers. Previous gastronomy points: {hist}
        An example output for {ex_num} gastronomy points of {ex_city}: {example}""",
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
    
    example = "[DiverXO??R, Taberna La Concha??T, Intruso Bar??B]"
    classification = pog_types()
    
    parser_recommendations = CommaSeparatedListOutputParser()
    template_recommendations = template_pog(parser_recommendations, example, "Madrid, Spain", 3, classification)

def pog_recommendations(num: int, c_en, c_oth):
    global template_recommendations, parser_recommendations, hist_recommendations, trans
    if not c_en.id in hist_recommendations:
        hist_recommendations[c_en.id] = []
        prev_pog = Pog.objects.filter(city_id = c_en.id, lang = 'en')
        for prev in prev_pog:
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
            for pog in resp:
                pog_split = pog.split('??')
                p = Pog(point_name = pog_split[0],name = pog_split[0], type = pog_split[1] , city = c_en, lang = 'en')
                p.save()
                hist_recommendations[c_en.id].append(pog_split[0])
                
                for c in c_oth:
                    name = trans.translate(p.point_name, src = p.lang, dest = 'es').text
                    p = Pog(point_name = pog_split[0], name = name, type = pog_split[1] , city = c, lang = c.lang)
                    p.save()
                
        except Exception as e:
            print("Error while parsing pog_recommendations response")
            print(e)
        

def pog_description(p_en, p_oth): 
    global trans 
    description = chat_gpt(f"Give a brief description, dishes and typical drinks of the gastronomy point {p_en.complete_name} of 300 characters")
    p_en.description = description
    p_en.save()
    
    if p_en.description != "":
        for p in p_oth:
            p.description = trans.translate(p_en.description, src = p_en.lang, dest = p.lang).text
            p.save()

def pog_get_or_create(point_name: str, city: CityBase, type: str = 'O'):
    pogs = Pog.objects.filter(point_name = point_name)
    
    if len(pogs) <= 0:
        city_en, city_es = city_get_or_create(city.id)
        
        pog_en = Pog(point_name=point_name, city=city_en, lang='en', type = type)
        pog_en.save()
        pog_es = Pog(point_name=point_name, city=city_es, lang='es', type = type)
        pog_es.save()
        
        if not city_en.id in hist_recommendations:
            hist_recommendations[city_en.id] = []
            prev_pog = Pog.objects.filter(city_id = city_en.id, lang = 'en')
            for prev in prev_pog:
                hist_recommendations[city_en.id].append(prev.point_name)
            
        hist_recommendations[city_en.id].append(point_name)
        
        check_pog_presentation(point_name)
        
    else:
        pog_en = pogs.get(lang= 'en')
        pog_es = pogs.get(lang = 'es')
        
    return pog_en, pog_es     

    
def check_pog_presentation(point_name: str):
    pog_lang = Pog.objects.filter(point_name = point_name)
    pog_en = pog_lang.get(lang= 'en')
    pog_others = pog_lang.exclude(lang='en')
    check_point_info_presentation(pog_en, pog_others)
    
def check_pog_info(point_name: str):
    pog_lang = Pog.objects.filter(point_name = point_name)
    pog_en = pog_lang.get(lang= 'en')
    pog_others = pog_lang.exclude(lang='en')
    
    check_point_info_info(pog_en, pog_others)

    if pog_en.description == "":
        pog_description(pog_en, pog_others)
        
def get_hist_pog(city: CityBase):
    global hist_recommendations
    
    city_en, _ = city_get_or_create(city.id)
    if not city_en.id in hist_recommendations:
        hist_recommendations[city_en.id] = []
        prev_poi = Pog.objects.filter(city_id = city_en.id, lang = 'en')
        for prev in prev_poi:
            hist_recommendations[city_en.id].append(prev.point_name)
    
    if len(hist_recommendations[city_en.id]) > 0:
        return str(hist_recommendations[city_en.id])     
    
    return ""

# Inicializar plantillas
init_template_recommendations()