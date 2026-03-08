from atrader import *

def init(context: Context):
    set_backtest(initial_cash=1000000)
    
def on_data(context: Context):
    order_volume(account_idx=0, target_idx=0, volume=1, side=1, position_effect=1, order_type=2)
    
if __name__ == '__main__':
    run_backtest(strategy_name='example_test', file_path='.', target_list=['SHFE.RB0000'], frequency='min', fre_num=15, begin_date='2025-01-01', end_date='2025-06-30')