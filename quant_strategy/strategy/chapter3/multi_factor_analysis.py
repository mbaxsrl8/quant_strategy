from atrader import *
from pandas import DataFrame
from neutralization import standardization
from MAD_factor import extreme_MAD
import matplotlib.pyplot as plt
import seaborn as sns

def factor_corr(factors: DataFrame):
    factors = factors.set_index('code')
    factors_process = standardization(extreme_MAD(factors.fillna(0)))
    result = factors_process.fillna(0).corr()
    return result

if __name__ == "__main__":
    factor_names = ['aroon_down', 'cci', 'adxr', 'atr']
    date = '2025-07-01'
    code_list = list(get_code_list('hs300', date=date).code)
    factors_1 = get_factor_by_day(factor_list=factor_names, target_list=code_list, date='2025-02-28')
    factors_2 = get_factor_by_day(factor_list=factor_names, target_list=code_list, date='2025-03-31')
    factors_3 = get_factor_by_day(factor_list=factor_names, target_list=code_list, date='2025-04-30')
    factors_4 = get_factor_by_day(factor_list=factor_names, target_list=code_list, date='2025-05-30')
    
    # print(factors_1.head())
    
    factors_corr1 = factor_corr(factors_1)
    factors_corr2 = factor_corr(factors_2)
    factors_corr3 = factor_corr(factors_3)  
    factors_corr4 = factor_corr(factors_4)
    
    factors_corr = (factors_corr1 + factors_corr2 + factors_corr3 + factors_corr4).div(4)
    print(factors_corr)
    
    mean_abs = abs(factors_corr).mean()
    print('mean abs corr: \n{}'.format(mean_abs))
    median_abs = abs(factors_corr).median()
    print('median abs corr: \n{}'.format(median_abs))
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(factors_corr, annot=True, cmap='CMRmap_r', vmin=-1, vmax=1, square=True)
    plt.show()
    