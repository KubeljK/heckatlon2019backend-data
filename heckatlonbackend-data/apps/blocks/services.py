import csv

from apps.helpers import datahelpers


class DataExportService:
    """Manages data import and export for this app."""

    @staticmethod
    def send_to_dataimport_api(filepath):
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]

        # Construct ingredients and nutrients data.
        ingredients_data = []
        nutrients_data = []
        for row in data:
            ing_obj = {
                "name": row["name"],
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