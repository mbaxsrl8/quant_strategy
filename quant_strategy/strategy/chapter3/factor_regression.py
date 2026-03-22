from atrader import *
import numpy as np
import pandas as pd
from pandas import DataFrame
from MAD_factor import extreme_MAD
from neutralization import neutralization
import statsmodels.api as sm
import matplotlib.pyplot as plt


def standardization(df: DataFrame):
    return (df - df.mean()) / df.std()


def factortest_regression(factor: DataFrame, stock: DataFrame):
    factor_return = list()
    t_value = list()
    stock_return = -stock.diff(-1, axis=1).div(stock)
    factor = factor.fillna(0)
    stock_return = stock_return.fillna(0)

    for i in range(factor.columns.size - 1):
        result = sm.OLS(stock_return.iloc[:, i], factor.iloc[:, i]).fit()
        factor_return.append(list(result.params))
        t_value.append(list(result.tvalues))

    return np.c_[np.array(factor_return), np.array(t_value)]


if __name__ == "__main__":
    start_date = "2025-04-01"
    end_date = "2026-03-01"
    code_list = list(get_code_list("hs300", date=start_date).code)
    factor = get_factor_by_factor(
        factor="pb_ratio_ttm",
        target_list=code_list,
        begin_date=start_date,
        end_date=end_date,
    )
    mkv = get_factor_by_factor(
        factor="market_cap_3",
        target_list=code_list,
        begin_date=start_date,
        end_date=end_date,
    )
    mkv.rename(columns={"market_cap_3": "mkv"}, inplace=True)
    mkv = mkv.set_index(["date"]).T
    factor = factor.set_index(["date"]).T

    trading_days = get_trading_days("SSE", start_date, end_date)
    months = np.vectorize(lambda x: x.month)(trading_days)
    month_end = trading_days[pd.Series(months) != pd.Series(months).shift(-1)]
    months_end_Timestamp = [pd.Timestamp(x) for x in month_end]
    # print(months_end_Timestamp)

    factor = factor[months_end_Timestamp].rename(index=str.lower)
    mkv = mkv[months_end_Timestamp].rename(index=str.lower)

    data = get_kdata(
        target_list=code_list,
        frequency="month",
        fre_num=1,
        begin_date=start_date,
        end_date=end_date,
        fq=1,
        fill_up=True,
        df=True,
        sort_by_date=False,
    )
    close = data.pivot_table(values="close", index="code", columns="time")
    code = sorted(set(list(data["code"])), key=list(data["code"]).index)
    stock_close = close.loc[code]
    # print(stock_close)

    # remove extreame value and standardize factor
    factor_S = standardization(extreme_MAD(factor, 5.2))
    # print(factor_S)

    # neutralization
    factor_ID = neutralization(factor_S, mkv)
    # print(factor_ID)

    # build regression model
    fr = factortest_regression(factor_S, stock_close)
    df = pd.DataFrame(
        data=fr, index=factor_S.columns[0:-1], columns=["factor_return", "t_value"]
    )

    # evaluate factor effectiveness
    t_ma = df["t_value"].abs().mean()
    print("t value abs mean: {}".format(t_ma))
    t_ratio = len(df[(df["t_value"].abs() > 2)]) / len(df["t_value"])
    print("t value > 2 ratio: {}".format(t_ratio))
    t_div = abs(df["t_value"].mean()) / df["t_value"].std()
    print("t value mean / std: {}".format(t_div))
    factor_ma = df['factor_return'].mean()
    print("factor return mean: {}".format(factor_ma))
    
    fig = plt.figure(figsize=(14, 8))
    df['factor_return'].cumsum().plot(kind='line', label='factor_return')
    plt.legend()
    plt.show()