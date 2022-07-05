from datetime import timedelta, datetime

import pandas as pd


def parse_raw_data(links, load, price):
    # WATT WATCHERS LOAD DATA
    # api_key = 'key_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    # headers = {
    #    'Authorization': 'Bearer %s' % api_key
    # }
    # response = requests.get('https://api-v3.wattwatchers.com.au/long-energy/{device-id}', headers=headers)
    # Load JSON: json_data
    # with open("sample_ww_data.json") as json_file:
    #    json_data = json.load(json_file)
    # energy_data = pd.read_json(load)
    # energy_data['datetime'] = pd.to_datetime(energy_data['timestamp'], format='%d/%m/%Y %H:%M')
    # energy_data.set_index('datetime', inplace=True)
    # energy_data['energy_kwh'] = energy_data['eReal'].iloc[0][0]
    # energy_data['energy_kwh'] = energy_data['energy_kwh'] / 3600000

    energy_data = pd.read_csv(load)
    energy_data['datetime'] = pd.to_datetime(energy_data['datetime'], format='%d/%m/%Y %H:%M')
    energy_data.set_index('datetime', inplace=True)

    # AEMO NEMWEB PRICE DATA
    price_data = pd.read_csv(price)
    price_data['datetime'] = pd.to_datetime(price_data['SETTLEMENTDATE'], format='%d/%m/%Y %H:%M')
    price_data.set_index('datetime', inplace=True)
    price_data['$/kwh'] = price_data['RRP']/1000

    # ALIGN DATETIME
    start = price_data.index[0]
    end = price_data.index[2015]
    energy_data = energy_data.loc[start:end]
    print('First period:', start, 'Last period:', end)

    # CONCATENATE AND CALCULATE COST
    time_index = pd.date_range(start=start, freq=timedelta(minutes=5), periods=2016)
    energy = pd.DataFrame(index=time_index)
    energy['energy_kwh'] = energy_data['energy_kwh']
    price = pd.DataFrame(index=time_index)
    price['price_$/kwh'] = price_data['$/kwh']
    df_concated = pd.concat([energy, price], axis=1)
    df_concated['cost'] = energy['energy_kwh'] * price['price_$/kwh']

    print('-----------------MODEL READY DATA-----------------')
    print(df_concated)
    print('--------------------------------------------------')
    return df_concated
