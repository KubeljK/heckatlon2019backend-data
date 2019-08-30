import requests, json

from django.db import connection

from apps.bfpd.models import Products, Nutrients, DerivationCodeDescription, ServingSize


def create_joined_tables():
    sql_command = """
        -- Cleaned ingredients table
        DROP TABLE IF EXISTS public.ingredients;
        CREATE TABLE public.ingredients AS
        SELECT
            PROD.id as id,
            PROD.long_name as name,
            null as description,
            null as ingredient_category
        
        FROM public.bfpd_products PROD;

        -- Cleaned nutrients table
        DROP TABLE IF EXISTS public.nutrients;
        CREATE TABLE public.nutrients AS
        SELECT
            NUTR.id as id,
            NUTR.nutrient_name as name,
            null as desciption,
            NUTR.output_value as value,
            NUTR.output_utom as unit,
            PROD.id as ingredient_id
        
        FROM public.bfpd_nutrients NUTR
            LEFT JOIN public.bfpd_products PROD ON (PROD.ndb_no = NUTR.ndb_no);
        """

    with connection.cursor() as cursor:
        cursor.execute(sql_command)

def send_to_dataimport_api(urlport):
    # Construct products data.
    ingredients_data = []
    for product in Products.objects.all():
        obj = {
            "name": product.long_name.lower() if product.long_name is not None else None,
            "description": None,
            "manufacturer": product.manufacturer.lower() if product.manufacturer is not None else None,
        }
        ingredients_data.append(obj)

    # Construct nutrients data.
    nutrients_data = []
    for nutrient in Nutrients.objects.all()[:20]:
        ingredient = Products.objects.get(ndb_no=nutrient.ndb_no)
        obj = {
            "ingredient_id": ingredient.id,
            "name": nutrient.nutrient_name.lower() if nutrient.nutrient_name is not None else None,
            "description": None,
            "value": float(nutrient.output_value) if nutrient.output_value is not None else None,
            "unit": nutrient.output_utom.lower() if nutrient.output_utom is not None else None
        }
        nutrients_data.append(obj)

    exporter = Dataexporter(
        modelname="ingredient",target_urlport=urlport,debug=True)
    exporter.export(ingredients_data)

    exporter = Dataexporter(
        modelname="nutrients",target_urlport=urlport,debug=True)
    exporter.export(nutrients_data)

class Dataexporter:
    def __init__(self, modelname, target_urlport, debug=False):
        self.modelname = modelname
        self.target_urlport = target_urlport
        self.debug = debug

    def export(self, data, size=100):
        i = 0
        while i < len(data):
            _data = data[i:i+size:1]
            self.make_post_request(_data)
            i = i+size

    def make_post_request(self, data):
        response = requests.post(self.target_urlport, 
            data={
                "model":self.modelname,
                "data": json.dumps(data)
            }
        )
