from atrader import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from MAD_factor import extreme_MAD
import statsmodels.api as sm


def get_industry_codes_ending_with_1():
    """
    Get industry codes from sw_industry.csv that end with '1'.
    
    Returns:
        dict: Dictionary with industry Chinese name (行业中文名) as key 
              and industry short code (行业简称) as value
    """
    import os
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the data directory (up two levels from chapter3)
    csv_path = os.path.join(current_dir, '../../data/sw_industry.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Filter rows where 行业简称 ends with '1'
    filtered_df = df[df['行业简称'].str.endswith('1')]
    
    # Convert to dictionary
    result_dict = dict(zip(filtered_df['行业中文名'], filtered_df['行业简称']))
    
    return result_dict

def industry_exposure(target_idx: list):
    shenwan_industry = get_industry_codes_ending_with_1()
    df = pd.DataFrame(index=[x.lower() for x in target_idx], columns=shenwan_industry.keys())
    # print(df.index)
    for industry in df.columns:
        # print(get_code_list(shenwan_industry[industry]).code.tolist())
        temp = list(set(df.index).intersection(set(get_code_list(shenwan_industry[industry]).code.tolist())))
        # print(temp)
        df.loc[temp, industry] = 1
    return df.fillna(0)

def neutralization(factor: DataFrame, mkv: DataFrame, industry=True):
    Y = factor.fillna(0)
    Y.rename(index = str.lower, inplace=True)
    df = pd.DataFrame(index=Y.index, columns=Y.columns)
    lnmkv = None
    if (type(mkv) == DataFrame or type(mkv) == pd.Series):
        mkv.rename(index=str.lower, inplace=True)
        lnmkv = mkv.iloc[:, 0].apply(lambda x: np.log(x))
        lnmkv = lnmkv.fillna(0)
    for i in range(Y.columns.size):
        if (lnmkv is not None):
            if industry:
                dummy_industry = industry_exposure(Y.index.tolist())
                X = pd.concat([dummy_industry, lnmkv], axis=1, sort=False)
            else:
                X = lnmkv
        elif industry:
            dummy_industry = industry_exposure(factor.index.tolist())
            X = dummy_industry
            
        result = sm.OLS(Y.iloc[:, i], X).fit()
        df.iloc[:, i] = result.resid.tolist()
    return df

def standardization(df: DataFrame):
    return (df - df.mean()) / df.std()
            
                
if __name__ == "__main__":
    date = '2025-07-01'
    code_list = list(get_code_list('hs300', date=date).code)
    print('code size: {}'.format(len(code_list)))
    mkv = get_factor_by_day(factor_list=['market_cap_3'], target_list=code_list, date=date)
    mkv.rename(columns={'market_cap_3': 'mkv'}, inplace=True)
    mkv.set_index('code', inplace=True)
    # print(mkv)
    factor = get_factor_by_day(factor_list=['pb_ratio_ttm', 'pe_ratio_ttm', 'ps_ratio_ttm', 'du_return_on_equity_ttm'], target_list=code_list, date=date)
    factor.rename(columns={'pb_ratio_ttm': 'pb', 'pe_ratio_ttm': 'pe', 'ps_ratio_ttm': 'ps', 'du_return_on_equity_ttm': 'roe'}, inplace=True)
    factor.set_index('code', inplace=True)
    # print(factor)
    ind = industry_exposure(factor.index.tolist())
    # print(ind)
    factor_S = standardization(extreme_MAD(factor))
    factor_ID = neutralization(factor_S, 0)
    factor_mkv = neutralization(factor_S, mkv, industry=False)
    factor_IDmkv = neutralization(factor_S, mkv, industry=True)
    
    fig = plt.figure(figsize=(14, 8))
    factor_S.iloc[:, 0].plot(kind='density', label='factor_S')
    factor_ID.iloc[:, 0].plot(kind='density', label='factor_ID')
    factor_mkv.iloc[:, 0].plot(kind='density', label='factor_mkv')
    factor_IDmkv.iloc[:, 0].plot(kind='density', label='factor_IDmkv')
    plt.legend()
    plt.show()
    
    