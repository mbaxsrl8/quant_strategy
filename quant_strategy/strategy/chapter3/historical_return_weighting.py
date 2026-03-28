from atrader import *
from neutralization import standardization
from MAD_factor import extreme_MAD
import statsmodels.api as sm

if __name__ == "__main__":
    factor_names = ["matapi", "tapi", "obv", "amv250", "amv120", "amv60", "amv5"]
    code_list = list(get_code_list("hs300", date="2025-07-01").code)
    data = get_kdata(
        target_list=code_list,
        frequency="month",
        fre_num=1,
        begin_date="2025-02-01",
        end_date="2025-06-30",
        fq=1,
        fill_up=True,
        df=True,
        sort_by_date=False,
    )
    close = data.pivot_table(index="code", columns="time", values="close")
    code = sorted(set(list(data["code"])), key=list(data["code"]).index)
    stock_close = close.loc[code]

    stock_return = stock_close.diff(axis=1).div(stock_close)
    factors_4 = get_factor_by_day(
        factor_list=factor_names, target_list=code_list, date="2025-05-30"
    )
    factors = factors_4.set_index("code").rename(index=str.lower)
    factors_process = standardization(extreme_MAD(factors.fillna(0)))

    factor_return = list()
    for i in range(factors_process.columns.size):
        X = factors_process.iloc[:, i]
        Y = stock_return.iloc[:, -1]
        result = sm.OLS(Y.astype(float), X.astype(float)).fit()
        factor_return.append(result.params.iloc[0])
    print(factor_return)

    weight = [x / sum(map(abs, factor_return)) for x in factor_return]
    for i in range(len(weight)):
        factors_process.iloc[:, i] = factors_process.iloc[:, i].mul(abs(weight[i]))
    composite_factor_return = factors_process.sum(axis=1)
    composite_factor_return = pd.DataFrame(composite_factor_return)
    print(composite_factor_return.head(5))
