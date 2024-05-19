from .common_prompts import chat_gpt
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from services.models import Country
from googletrans import Translator

template_population = None
parser_population = None

template_info = None
parser_info = None

template_security = None
parser_security = None

trans = Translator()
                          
def template_country(parser, example, ex_country):
    format_instructions = parser.get_format_instructions()
    
    templ = PromptTemplate(
        template = """Extract the following details of the country {country}.
        {format_instructions}
        An example output for country {ex_country}: {example}""",
        input_variables = ["country"],
        partial_variables = {"format_instructions": format_instructions, 
                             "ex_country": ex_country,
                             "example": example}
    )
    
    return templ


def init_template_population():
    global template_population, parser_population
    response_schemas = [
        ResponseSchema(name = "national_day", description = "national day"),
        ResponseSchema(name = "population", description = "total population"),
        ResponseSchema(name = "density", description = "density population"),
        ResponseSchema(name = "age_structure", description = "short description of age structure")
    ]
    
    example = """
    ```json
    {
        "national_day": "August 1",
        "population": "8,654,622 inhabitants",
        "density": "214 inhabitants per km²",
        "age_structure": "The population of Switzerland is distributed between 15.4% people under 25 years old, 32% people between 25 and 50 years old, 33.9% people between 50 and 75 years old, and 18.7% of people over 75 years of age."
    }
    ```"""
    
    parser_population = StructuredOutputParser.from_response_schemas(response_schemas)
    template_population = template_country(parser_population, example, "Switzerland")


def country_population(c_en, c_oth):
    global template_population, parser_population, trans
    input = template_population.format_prompt(country = c_en.name)
    
    output = chat_gpt(input.to_string())
    
    if output != "":
        try:
            resp = parser_population.parse(output)
            c_en.national_day = resp["national_day"]
            c_en.population = resp["population"]
            c_en. density = resp["density"]
            c_en.age_structure = resp["age_structure"]
            c_en.save()
            
            if c_en.national_day != "":
                for c in c_oth:
                    try:
                        c.national_day = trans.translate(c_en.national_day, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.national_day = c_en.national_day
                    try:
                        c.population = trans.translate(c_en.population, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.population = c_en.population
                    try:
                        c.density = trans.translate(c_en.density, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.density = c_en.density
                    try:
                        c.age_structure = trans.translate(c_en.age_structure, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.age_structure = c_en.age_structure
                    c.save()
            
        except Exception as e:
            print("Error while parsing country_population response")
            print(e)
    
def init_template_info():
    global template_info, parser_info
    response_schemas = [
        ResponseSchema(name = "languages", description = "common spoken languages"),
        ResponseSchema(name = "currency", description = "offical currency")
    ]
    
    example = """
    ```json
    {
        "languages": "German, French, Italian, Romansh",
        "currency": "Swiss franc"
    }
    ```"""
    
    parser_info = StructuredOutputParser.from_response_schemas(response_schemas)
    template_info = template_country(parser_info, example, "Switzerland")


def country_info(c_en, c_oth):
    global template_info, parser_info, trans
    input = template_info.format_prompt(country = c_en.name)
    
    output = chat_gpt(input.to_string())
    
    if output != "":
        try:
            resp = parser_info.parse(output)
            c_en.languages = "Languages: " + resp["languages"]
            c_en.currency = resp["currency"]
            c_en.save()
            if c_en.languages != "":
                for c in c_oth:
                    try:
                        c.languages = trans.translate(c_en.languages, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.languages = c_en.languages
                    try:
                        c.currency = trans.translate(c_en.currency, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                       c.currency = c_en.currency 
                    c.save()
        except Exception as e:
            print("Error while parsing country_info response")
            print(e)

def init_template_security():
    global template_security, parser_security
    response_schemas = [
        ResponseSchema(name = "police", description = "police number"),
        ResponseSchema(name = "firefighter", description = "firefighter number"),
        ResponseSchema(name = "ambulance", description = "ambulance number")
    ]
    
    example = """
    ```json
    {
        "police": "117",
        "firefighter": "118",
        "ambulance": "144"
    }
    ```"""
    
    parser_security = StructuredOutputParser.from_response_schemas(response_schemas)
    template_security = template_country(parser_security, example, "Switzerland")


def country_security(c_en, c_oth):
    global template_security, parser_security, trans
    input = template_security.format_prompt(country = c_en.name)
    
    output = chat_gpt(input.to_string())

    if output != "":
        try:
            resp = parser_security.parse(output)
            c_en.police = resp["police"]
            c_en.firefighter = resp["firefighter"]
            c_en.ambulance = resp["ambulance"] 
            c_en.save()
            
            if c_en.police != "":
                for c in c_oth:
                    try:
                        c.police = trans.translate(c_en.police, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.police = c_en.police
                    try:
                        c.firefighter = trans.translate(c_en.firefighter, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.firefighter = c_en.firefighter
                    try:
                        c.ambulance = trans.translate(c_en.ambulance, src = c_en.lang, dest = c.lang).text
                    except Exception as e:
                        c.ambulance = c_en.ambulance
                    c.save()
            
        except Exception as e:
            print("Error while parsing country_security response")
            print(e)


def country_presentation(c_en, c_oth): 
    global trans
    presentation = chat_gpt(f"Brief presentation of {c_en.name} of 200 characters")
    c_en.presentation = presentation
    c_en.save()
    
    if c_en.presentation != "":
        for c in c_oth:
            try:
                c.presentation = trans.translate(c_en.presentation, src = c_en.lang, dest = c.lang).text
            except Exception as e:
                c.presentation = c_en.presentation
            c.save()

def country_history(c_en, c_oth):
    global trans
    history = chat_gpt(f"History of {c_en.name} of 500 characters")
    c_en.history = history
    c_en.save()
    
    if c_en.history != "":
        for c in c_oth:
            try:
                c.history = trans.translate(c_en.history, src = c_en.lang, dest = c.lang).text
            except Exception as e:
                c.history = c_en.history
            c.save()
    
def country_curiosities(c_en, c_oth):
    global trans
    curiosities = chat_gpt(f"Three curiosities of {c_en.name}")
    c_en.curiosities = curiosities
    c_en.save()
    
    if c_en.curiosities != "":
        for c in c_oth:
            try:
                c.curiosities = trans.translate(c_en.curiosities, src = c_en.lang, dest = c.lang).text
            except Exception as e:
                c.curiosities = c_en.curiosities
            c.save()
   
def country_get_or_create(country_id: int):
    country = Country.objects.filter(country_id = country_id)
    if len(country) <= 0:
        country_en = Country(country_id = country_id, lang = 'en')
        country_en.save()
        country_es = Country(country_id = country_id, lang = 'es')
        country_es.save()
        check_country_presentation(country_id)
    else:
        country_en = country.get(lang = 'en')
        country_es = country.get(lang = 'es')
        
    return country_en, country_es    

def check_country_presentation(country_id: int):
    country_lang = Country.objects.filter(country_id = country_id)
    country_en = country_lang.get(lang= 'en')
    country_others = country_lang.exclude(lang='en')

    if country_en.presentation == "":
        country_presentation(country_en, country_others) 
    
def check_country_info(country_id: int):
    country_lang = Country.objects.filter(country_id = country_id)
    country_en = country_lang.get(lang= 'en')
    country_others = country_lang.exclude(lang='en')

    check_country_presentation(country_id)

    if country_en.national_day == "":
        country_population(country_en, country_others)

    if country_en.languages == "":
        country_info(country_en, country_others)

    if country_en.police == "":
        country_security(country_en, country_others)

    if country_en.history == "":
        country_history(country_en, country_others)

    if country_en.curiosities == "":
        country_curiosities(country_en, country_others)
     

# Inicializar plantillas
init_template_population()
init_template_info()
init_template_security()