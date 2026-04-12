import scipy.optimize as opt
import atrader as at
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 菲林格尔、飞沃科技、天普股份
    poforlio = ["sse.603226", "szse.301232", "sse.605255"]
    close_data = at.get_kdata(
        poforlio,
        "month",
        fre_num=1,
        begin_date="2025-01-01",
        end_date="2026-03-31",
        fill_up=True,
        df=True,
    )["close"]
    close_data = pd.DataFrame(np.array(close_data).reshape(3, -1)).T
    returns = close_data.iloc[1:, :] / close_data.shift(1).iloc[1:, :] - 1
    print("5 head of returns:\n", returns.head())

    means = returns.mean()
    print("mean returns:\n", means)
    cov = returns.cov()
    print("covariance matrix:\n", cov)

    def poforlioVar(w):
        return np.dot(w.T, np.dot(cov, w))

    # define expected return constraint
    mean = np.arange(min(means), max(means), 0.001, dtype=float)
    std = []
    # set the initial guess for weights
    w = [1 / len(means)] * len(means)
    bounds = [(0, None)] * len(means)

    for target in mean:
        constrain = (
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},
            {"type": "eq", "fun": lambda w, t=target: np.dot(w.T, means) - t},
        )
        result = opt.minimize(poforlioVar, w, constraints=constrain, bounds=bounds)
        std.append(np.sqrt(result.fun))

    plt.figure(figsize=(16, 9))
    plt.plot(std, mean, color="blue")
    plt.xlabel("σ", loc="right")
    plt.ylabel("E(R)", loc="top", rotation=0)
    plt.grid()
    
    constrain = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    result = opt.minimize(poforlioVar, w, constraints=constrain, bounds=bounds)
    std_min = np.sqrt(result.fun)
    mean_min = np.dot(result.x.T, means)
    print('Min risk portfolio:\n', result.x)
    print('Min risk portfolio standard deviation:', std_min)
    print('Min risk portfolio mean return:', mean_min)
    
    plt.scatter(std_min, mean_min, color='purple', marker='*', s=50)
    plt.plot(pd.Series(std)[mean>=mean_min], pd.Series(mean)[mean>=mean_min], color='red', label='Efficient Frontier')
    
    # set risk-free rate of interest
    rf = 0.005
    w = [1/len(means)] * len(means)
    constrain = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    def min_sharpe(w):
        return -(np.dot(w.T, means) - rf) / np.sqrt(np.dot(w.T, np.dot(cov, w)))
    result = opt.minimize(min_sharpe, w, constraints=constrain, bounds=bounds)
    sharpe = -result.fun
    weights = result.x
    std_market = np.sqrt(np.dot(weights.T, np.dot(cov, weights)))
    mean_market = np.dot(weights.T, means)
    print('Market portfolio:\n', weights)
    print('Market portfolio standard deviation:', round(std_market, 3))
    print('Market portfolio mean return:', round(mean_market, 3))
    
    plt.scatter(std_market, mean_market, color='green', marker='*', s=50, label='Market Portfolio')
    
    # draw capital market line
    axes = plt.gca()
    # get the x and y limits of the current plot
    x_vals = np.array(axes.get_xlim())
    y_vals = rf + sharpe * x_vals
    plt.plot(x_vals, y_vals, color='orange', label='Capital Market Line')
    
    plt.show()
