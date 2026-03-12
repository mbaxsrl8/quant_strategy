from atrader import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

def extreme_MAD(df: DataFrame, n=5.2) -> DataFrame:
    # get median
    median = df.median()
    # get median absolute deviation
    mad = abs(df - median).quantile(0.5)
    # uppper and lower bound is not necessary to be symmetric
    df_up = median + n * mad
    df_down = median - n * mad  
    return df.clip(lower=df_down, upper=df_up, axis=1)

if __name__ == "__main__":
    date='2025-07-01'
    code_list = list(get_code_list('hs300', date=date).code)
    print(code_list)
    factor = get_factor_by_day(factor_list=['pe_ratio_ttm','pb_ratio_ttm'], target_list=code_list, date='2025-07-01')
    print(factor)
    factors = factor.set_index('code')
    factors = factors.fillna(0)
    # factors = extreme_MAD(factors)
    # print(factors)
    
    fig = plt.figure(figsize=(14, 8))
    factors.iloc[:, 0].plot(kind='kde', label='pe_ratio_ttm')
    extreme_MAD(factors).iloc[:, 0].plot(kind='kde', label='pe_ratio_ttm_MAD')
    plt.legend()
    plt.title('PE Ratio TTM Distribution Before and After MAD')
    plt.show()