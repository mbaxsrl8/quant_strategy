from atrader import *

def init(context: Context):
    set_backtest(initial_cash=100000)
    reg_kdata(frequency='day', fre_num=1)
    
def on_data(context: Context):
    df_day = get_reg_kdata(reg_idx=context.reg_kdata[0], length=2, df=True)
    print(df_day)
    
if __name__ == '__main__':
    run_backtest(strategy_name='atrader-1_freq', file_path='.', target_list=['SSE.600000'], frequency='day', fre_num=1, begin_date='2025-06-01', end_date='2025-10-19')