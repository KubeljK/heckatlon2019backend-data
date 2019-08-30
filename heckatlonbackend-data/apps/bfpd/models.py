from django.db import models


class Products(models.Model):
    ndb_no = models.IntegerField(
        help_text="""8-digit Nutrient Database Number (NDB) that
        uniquely identifies a food item. Links to the
        Nutrient file and the Serving Size file.""")

    long_name = models.CharField(
        max_length=255, help_text="200-character description of food item")

    data_source = models.CharField(
        max_length=255, help_text="""A code designating the source of the data:
        GDSN = Global Data Synchronization Network via 1WorldSync
        LI = Label Insight""", null=True)

    gtin_upc = models.CharField(
        max_length=255, help_text="A unique code identifying a specific product:", null=True)

    manufacturer = models.CharField(
        max_length=255, help_text="The company that manufactured the product", null=True)

    date_modified = models.DateField(
        help_text="Date when the food record was last updated by the data provider", null=True)

    date_available = models.DateField(
        help_text="Date when the food record was made available for inclusion in the database", null=True)

    ingredients = models.TextField(
        help_text = "Ingredients of the product", null=True)


class Nutrients(models.Model):
    ndb_no = models.IntegerField()

    nutrient_code = models.IntegerField(
        help_text = "Unique 3-digit identifier code for a nutrient")

    nutrient_name = models.CharField(
        help_text = "Name of nutrient/food component", max_length=255)

    derivation_code = models.CharField(
        help_text = """A code indicating how the Output_Value was
        determined. The codes used are defined in the Derivation Code Description file""",
        null=True, max_length=4)

    output_value = models.DecimalField(
        help_text = """Amount in 100 g, edible portion. This value is
        calculated from the amount per serving value on
        the Nutrition Facts Panel supplied by the data
        provider""", max_digits=10, decimal_places=2)

    output_utom = models.CharField(
        help_text = "Units of measure for the Output Value", max_length=255)


class DerivationCodeDescription(models.Model):
    derivation_code = models.CharField(
        help_text = """A code indicating how the Output Value was
        determined. Links to the Nutrient file.""", max_length=4)

    derivation_code_description = models.CharField(
        help_text = """Description of the derivation code""", max_length=255)

class ServingSize(models.Model):
    ndb_no = models.IntegerField()

    serving_size = models.DecimalField(
        help_text="""Weight of the specified serving""",
        max_digits=10, decimal_places=2, null=True)

    serving_size_uom = models.CharField(
        help_text="""Unit of Measure for the serving size
        g: Serving size reported in grams
        m: Serving size reported in milliliters""", max_length=2,
        null=True)

    household_serving_size = models.DecimalField(
        help_text="""The amount of the
        Household_Serving_Size_UOM, i.e., the number
        of cups, tablespoons, teaspoons in a serving.
        May be a fraction, such as 0.25 or 0.50.""",
        max_digits=10, decimal_places=2, null=True)

    household_serving_size_uom = models.CharField(
        help_text="""The Units of Measure for the Household Serving,
        i.e., cup, tablespoon, teaspoon.""", max_length=255, null=True)

    preparation_state = models.CharField(
        help_text="""Indicates if the information from the Nutrition
        Facts Panel is for the prepared or unprepared
        food. Only included if supplied.""", max_length=255, null=True)
