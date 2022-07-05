from datetime import timedelta


def resample_30m(parsed_data):
    df_resampled_30m = parsed_data.resample(rule=timedelta(minutes=30), label='right').sum()
    return df_resampled_30m


def resample_2h(parsed_data):
    df_resampled_2h = parsed_data.resample(rule=timedelta(hours=2), label='right').sum()
    return df_resampled_2h
