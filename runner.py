from model_2 import model_30m
from model_3 import model_2h
from parse import parse_raw_data
from configs import scenario_datapaths
from model_1 import model_5m
from resample import resample_30m, resample_2h

parsed = parse_raw_data(links=None, load=scenario_datapaths['load_jan'], price=scenario_datapaths['price_jan'])

model_5m(parsed, False)

model_5m(parsed, True)


# resampled_30m = resample_30m(parsed)
#
# model_30m(resampled_30m, False)
#
# model_30m(resampled_30m, True)
#
#
# resampled_2h = resample_2h(parsed)
#
# model_2h(resampled_2h, False)
#
# model_2h(resampled_2h, True)
