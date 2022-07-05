import pandas as pd
from ts_tariffs.billing import Bill, BillCompare
from ts_tariffs.meters import MeterData
from ts_tariffs.tariffs import (
    ConnectionTariff,
    TouTariff,
    DemandTariff,
)
from ts_tariffs.ts_utils import SampleRate, TouBins
from datetime import timedelta, datetime
import numpy as np

# Notes:
# Below is an example of how to calculate the tariffs we found on the bill you have
# Make sure you install ts_tariffs: pip install ts-tariffs

# The create_mock_scenario_bill() function creates random consumption data (modify magnitude with the multiplier)
# It then puts defines some tariffs
# It then returns the associated bill for the collection of tariffs

# At the bottom of this file there is a script which calls this function to create a bunch bills for different scenarios
# It then puts them in a BillCompare object which makes it simple to compare everything in a dataframe
from configs import scenario_datapaths


def create_mock_scenario_bill(load, scenario_name: str, multiplier: float) -> Bill:
    # Create mock energy data (1 year, 5 min increments)

    year_worth_of_periods = 288 * 7
    consumption_sample_rate = timedelta(minutes=5)
    time_index = pd.date_range(start=datetime(2022, 1, 1, 0, 5), freq=consumption_sample_rate,
                               periods=year_worth_of_periods)
    consumption_df = pd.DataFrame(index=time_index)
    energy_data = pd.read_csv(load)
    energy_data['datetime'] = pd.to_datetime(energy_data['datetime'], format='%d/%m/%Y %H:%M')
    energy_data.set_index('datetime', inplace=True)
    consumption_df['energy_kwh'] = multiplier * energy_data['energy_kwh']
    print(consumption_df)

    # Create energy meter object
    meter_data_kwh = MeterData(
        name='example',
        tseries=consumption_df['energy_kwh'],
        sample_rate=consumption_sample_rate,
        units='kWh'
    )
    # To create power meter object (for demand charge) there's a handy method
    # that world with any kWh meter data
    meter_data_kw = meter_data_kwh.kwh_to_kw()

    # Create time of use bins - note, the code below means that
    # hours 0 to 7 are $0.06, hours 7 to 21 are $0.1, etc
    # source: https://www.agl.com.au/content/dam/digital/agl/documents/terms-and-conditions/energy/rates-and-contracts
    # /standard-retail-contracts/nsw/agl-nsw-elec-my-pcp-website-pricing-20210701.pdf
    tou_bins = TouBins(
        time_bins=[7, 14, 20, 22, 24],
        bin_rates=[0.1201, 0.2167, 0.2619, 0.2167, 0.1201],
        bin_labels=["off-peak", "shoulder", "peak", "shoulder", "off-peak"]
    )

    # Create time of use tariff for kWh consumption
    # Note that the sample rate in tariffs is the timestep at which
    # the retailer measures consumption, so 30mins in most cases where
    # there's a standard smart meter
    charge_sample_rate = timedelta(minutes=30)
    time_of_use_tariff = TouTariff(
        name='tou_charge',
        charge_type='TouTariff',
        consumption_unit='kWh',
        rate_unit='$/kWh',
        sample_rate=charge_sample_rate,  # or use timedelta(minutes=30)
        adjustment_factor=1.0,  # Ignore this - on some tariffs they adjust for various network efficiency issues
        tou=tou_bins,
    )

    # Create demand tariff
    # Note that you need at least a month worth of data for this to work
    demand_tariff = DemandTariff(
        name='demand_charge',
        charge_type='DemandCharge',
        consumption_unit='kW',
        rate_unit='$/kW',
        sample_rate=charge_sample_rate,
        adjustment_factor=1.0,
        rate=0.335489,
        frequency_applied='month',
        time_window=None  # Ignore this - only used if demand charge applies to certain hours of the day
    )

    connection_tariff = ConnectionTariff(
        name='connection_charge',
        charge_type='ConnectionTariff',
        consumption_unit='day',
        rate_unit='$/day',
        sample_rate=charge_sample_rate,
        adjustment_factor=1.0,
        rate=0.3,
        frequency_applied='day'  # i.e. this is a daily fee
    )

    # Create AppliedCharge objects - these contain the cost calc results in various forms
    # and are used by the Bill objects
    applied_tou_tariff = time_of_use_tariff.apply(meter_data_kwh)
    applied_demand_tariff = demand_tariff.apply(meter_data_kw)
    applied_connection_tariff = connection_tariff.apply(
        meter_data_kwh)  # Either meter data works here as it's applied to the times, not the consumption

    # Create bill - this bundles everything together conveniently
    return Bill(
        scenario_name,
        charges=[
            applied_tou_tariff,
            applied_demand_tariff,
            applied_connection_tariff
        ]
    )


if __name__ == '__main__':
    # Create list of scenario bills for comparison
    bills_list = [
        create_mock_scenario_bill(scenario_datapaths['load_jan'], 's1', multiplier=1.5),
        create_mock_scenario_bill(scenario_datapaths['load_jan'], 's2', multiplier=1.0),
        create_mock_scenario_bill(scenario_datapaths['load_jan'], 's3', multiplier=2.5),
        create_mock_scenario_bill(scenario_datapaths['load_jan'], 's4', multiplier=4.8),
    ]

    # Create comparison object and print dataframe
    bill_comparison = BillCompare(bills_list)
    print(bill_comparison.as_dataframe)
