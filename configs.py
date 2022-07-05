import os
from local_project_data.local_data import local_path

# month must match
scenario_datapaths = {
    'price_jan': os.path.join(local_path, 'price', 'PRICE_AND_DEMAND_202201_NSW1.csv'),
    'sample': os.path.join(local_path, 'load', 'sample_ww_data.json'),
    'load_jan': os.path.join(local_path, 'load', 'LOAD_15.12.2021_16.01.2022.csv'),
    'price_feb': os.path.join(local_path, 'price', 'PRICE_AND_DEMAND_202202_NSW1.csv'),
    'price_mar': os.path.join(local_path, 'price', 'PRICE_AND_DEMAND_202203_NSW1.csv'),
    'price_apr': os.path.join(local_path, 'price', 'PRICE_AND_DEMAND_202204_NSW1.csv'),
    'price_may': os.path.join(local_path, 'price', 'PRICE_AND_DEMAND_202205_NSW1.csv')
}
