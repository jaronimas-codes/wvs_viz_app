import pandas as pd

def load_all_data():
    env_data = pd.read_csv("pre_data/precomputed_env_data.csv")
    age_data = pd.read_csv("pre_data/precomputed_age_data.csv")
    co2_data = pd.read_csv("pre_data/co2-data.csv")
    tax_data = pd.read_csv("pre_data/tax_summary.csv")
    return env_data, age_data, co2_data, tax_data

def get_country_mapping():
    from country_mapping import country_info
    return {info["country_3"]: info["country_name"] for info in country_info}

def get_question_options(env_data):
    from variable_mappings_env import variable_mappings
    return {k: v for d in variable_mappings for k, v in d.items() if k in env_data.columns}
