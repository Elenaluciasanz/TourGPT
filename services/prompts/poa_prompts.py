from .common_prompts import chat_gpt
from .point_info_prompts import check_point_info_info, check_point_info_presentation
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from services.models import Poa, poa_types
from cities_light.models import City as CityBase
from .city_prompts import city_get_or_create
from googletrans import Translator

template_recommendations = None
parser_recommendations = None
hist_recommendations = {}

trans = Translator()

def template_poa(parser, example, ex_city, ex_num, classification):
    format_instructions = parser.get_format_instructions()
    
    templ = PromptTemplate(
        template = """List {num} accommodation points of {city}.
        Classify them using the classification {classification} and add the letter of the classification after the point name followed by '??'.
        {format_instructions}.
        Do not repeat answers. Previous accommodation points: {hist}
        An example output for {ex_num} accommodation points of {ex_city}: {example}""",
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
    
    example = "`Hotel Wellington??HO, Cats Hostel Madrid Sol??HE, Camping Osuna??C`"
    classification = poa_types()
    
    parser_recommendations = CommaSeparatedListOutputParser()
    template_recommendations = template_poa(parser_recommendations, example, "Madrid, Spain", 3, classification)

def poa_recommendations(num: int, c_en, c_oth):
    global template_recommendations, parser_recommendations, hist_recommendations, trans
    if not c_en.id in hist_recommendations:
        hist_recommendations[c_en.id] = []
        prev_poa = Poa.objects.filter(city_id = c_en.id, lang = 'en')
        for prev in prev_poa:
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
            for poa in resp:
                poa_split = poa.split('??')
                p = Poa(point_name = poa_split[0],name = poa_split[0], type = poa_split[1] , city = c_en, lang = 'en')
                p.save()
                hist_recommendations[c_en.id].append(poa_split[0])
                
                for c in c_oth:
                    name = trans.translate(p.point_name, src = p.lang, dest = 'es').text
                    p = Poa(point_name = poa_split[0], name = name, type = poa_split[1] , city = c, lang = c.lang)
                    p.save()
        
        except Exception as e:
            print("Error while parsing poa_recommendations response")
            print(e)
        

def poa_description(p_en, p_oth): 
    global trans 
    description = chat_gpt(f"Give a brief description, activities and facilities of the accomodation point {p_en.complete_name} of 300 characters")
    p_en.description = description
    p_en.save()
    
    if p_en.description != "":
        for p in p_oth:
            p.description = trans.translate(p_en.description, src = p_en.lang, dest = p.lang).text
            p.save()
    
    
def poa_get_or_create(point_name: str, city: CityBase, type: str = 'O'):
    global hist_recommendations
    poas = Poa.objects.filter(point_name = point_name)
    
    if len(poas) <= 0:
        city_en, city_es = city_get_or_create(city.id)
        
        poa_en = Poa(point_name=point_name, city=city_en, lang='en', type = type)
        poa_en.save()
        poa_es = Poa(point_name=point_name, city=city_es, lang='es', type = type)
        poa_es.save()
        
        if not city_en.id in hist_recommendations:
            hist_recommendations[city_en.id] = []
            prev_poa = Poa.objects.filter(city_id = city_en.id, lang = 'en')
            for prev in prev_poa:
                hist_recommendations[city_en.id].append(prev.point_name)
            
        hist_recommendations[city_en.id].append(point_name)
        
        check_poa_presentation(point_name)
        
    else:
        poa_en = poas.get(lang= 'en')
        poa_es = poas.get(lang = 'es')
        
    return poa_en, poa_es 

    
def check_poa_presentation(point_name: str):
    poa_lang = Poa.objects.filter(point_name = point_name)
    poa_en = poa_lang.get(lang= 'en')
    poa_others = poa_lang.exclude(lang='en')
    check_point_info_presentation(poa_en, poa_others)
    
def check_poa_info(point_name: str):
    poa_lang = Poa.objects.filter(point_name = point_name)
    poa_en = poa_lang.get(lang= 'en')
    poa_others = poa_lang.exclude(lang='en')
    
    check_point_info_info(poa_en, poa_others)

    if poa_en.description == "":
        poa_description(poa_en, poa_others)
        

def get_hist_poa(city: CityBase):
    global hist_recommendations
    
    city_en, _ = city_get_or_create(city.id)
    if not city_en.id in hist_recommendations:
        hist_recommendations[city_en.id] = []
        prev_poi = Poa.objects.filter(city_id = city_en.id, lang = 'en')
        for prev in prev_poi:
            hist_recommendations[city_en.id].append(prev.point_name)
    
    if len(hist_recommendations[city_en.id]) > 0:
        return str(hist_recommendations[city_en.id])     
    
    return ""

# Inicializar plantillas
init_template_recommendations()