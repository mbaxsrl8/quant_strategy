from atrader import *


def init(context: Context):
    set_backtest(initial_cash=100000)
    print('account_list =', context.account_list)
    print('target_list =', context.target_list)


def on_data(context: Context):
    pass
