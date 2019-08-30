from django.db import connection
import os

def import_csv(table_name, filepath):
    sql_command = """
            TRUNCATE public."{}";
            COPY public."{}" FROM '{}' DELIMITER ',' CSV HEADER;
        """.format(table_name, table_name, filepath)

    with connection.cursor() as cursor:
        cursor.execute(sql_command)


def import_data(dir_path):
    map_model_to_csv = {
        "Products": "Products.csv",
        "Nutrients": "Nutrients.csv",
        "DerivationCodeDescription": "Derivation_Code_Description.csv",
        "ServingSize": "Serving_size.csv"
    }
    
    for model, csvname in map_model_to_csv.items():
        table_name = "%s_%s"%("bfpd", model.lower())
        filepath = os.path.join(dir_path, csvname)
        import_csv(table_name, filepath)
