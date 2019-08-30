import pandas as pd
import json

def parse_csv_to_json(csv_filepath, sep=",", decimal="."):
    df = pd.read_csv(csv_filepath, sep, decimal)
    return json.loads(df.to_json())
