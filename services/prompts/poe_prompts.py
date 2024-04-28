from .common_prompts import chat_gpt
from .point_info_prompts import check_point_info_info, check_point_info_presentation
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from services.models import Poe, poe_types
from cities_light.models import City as CityBase
from .city_prompts import city_get_or_create
from googletrans import Translator

template_recommendations = None
parser_recommendations = None
hist_recommendations = {}

trans = Translator()

def template_poe(parser, example, ex_city, ex_num, classification):
    format_instructions = parser.get_format_instructions()
    
    templ = PromptTemplate(
        template = """List {num} points of entertainment and leisure of {city}.
        Classify them using the classification {classification} and add the letter of the classification after the point name followed by '??'.
        Suggest places to spend time with family and friends, entertain and relax, as the classification indicates.
        {format_instructions}.
        Do not repeat answers. Previous points of entertainment: {hist}
        An example output for {ex_num} points of entertainment of {ex_city}: {example}""",
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
    
    example = "[La Vaguada??M, Parque Warner??T, Cines Callao??C]"
    classification = poe_types()
    
    parser_recommendations = CommaSeparatedListOutputParser()
    template_recommendations = template_poe(parser_recommendations, example, "Madrid, Spain", 3, classification)

def poe_recommendations(num: int, c_en, c_oth):
    global template_recommendations, parser_recommendations, hist_recommendations, trans
    if not c_en.id in hist_recommendations:
        hist_recommendations[c_en.id] = []
        prev_poe = Poe.objects.filter(city_id = c_en.id, lang = 'en')
        for prev in prev_poe:
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
            for poe in resp:
                poe_split = poe.split('??')
                p = Poe(point_name = poe_split[0],name = poe_split[0], type = poe_split[1] , city = c_en, lang = 'en')
                p.save()
                hist_recommendations[c_en.id].append(poe_split[0])
                
                for c in c_oth:
                    name = trans.translate(p.point_name, src = p.lang, dest = 'es').text
                    p = Poe(point_name = poe_split[0], name = name, type = poe_split[1] , city = c, lang = c.lang)
                    p.save()
                
        except Exception as e:
            print("Error while parsing poe_recommendations response")
            print(e)
        

def poe_description(p_en, p_oth): 
    global trans 
    description = chat_gpt(f"Give a brief description, activities and facilities of the entertainment point {p_en.complete_name} of 300 characters.")
    p_en.description = description
    p_en.save()
    
    if p_en.description != "":
        for p in p_oth:
            p.description = trans.translate(p_en.description, src = p_en.lang, dest = p.lang).text
            p.save()

def poe_get_or_create(point_name: str, city: CityBase, type: str = 'O'):
    poes = Poe.objects.filter(point_name = point_name)
    
    if len(poes) <= 0:
        city_en, city_es = city_get_or_create(city.id)
        
        poe_en = Poe(point_name=point_name, city=city_en, lang='en', type = type)
        poe_en.save()
        poe_es = Poe(point_name=point_name, city=city_es, lang='es', type = type)
        poe_es.save()
        
        if not city_en.id in hist_recommendations:
            hist_recommendations[city_en.id] = []
            prev_poe = Poe.objects.filter(city_id = city_en.id, lang = 'en')
            for prev in prev_poe:
                hist_recommendations[city_en.id].append(prev.point_name)
            
        hist_recommendations[city_en.id].append(point_name)
        
        check_poe_presentation(point_name)
        
    else:
        poe_en = poes.get(lang= 'en')
        poe_es = poes.get(lang = 'es')
        
    return poe_en, poe_es     

    
def check_poe_presentation(point_name: str):
    poe_lang = Poe.objects.filter(point_name = point_name)
    poe_en = poe_lang.get(lang= 'en')
    poe_others = poe_lang.exclude(lang='en')
    check_point_info_presentation(poe_en, poe_others)
    
def check_poe_info(point_name: str):
    poe_lang = Poe.objects.filter(point_name = point_name)
    poe_en = poe_lang.get(lang= 'en')
    poe_others = poe_lang.exclude(lang='en')
    
    check_point_info_info(poe_en, poe_others)

    if poe_en.description == "":
        poe_description(poe_en, poe_others)

def get_hist_poe(city: CityBase):
    global hist_recommendations
    
    city_en, _ = city_get_or_create(city.id)
    if not city_en.id in hist_recommendations:
        hist_recommendations[city_en.id] = []
        prev_poi = Poe.objects.filter(city_id = city_en.id, lang = 'en')
        for prev in prev_poi:
            hist_recommendations[city_en.id].append(prev.point_name)
    
    if len(hist_recommendations[city_en.id]) > 0:
        return str(hist_recommendations[city_en.id])     
    
    return ""       

# Inicializar plantillas
init_template_recommendations()