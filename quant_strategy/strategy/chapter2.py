from atrader import *

def init(context: Context):
    reg_kdata(frequency='minute', fre_num=5)
    reg_kdata(frequency='minute', fre_num=15)
    reg_factor(factor_list=['PE'])
    context.pyfh = get_kdata(code='SHSE.600000', frequency='minute', fre_num=5, begin_date='2025-03-01', end_date='2025-04-30')
    context.m = 10
    context.n = 20
    
def on_data(context: Context):
    data0 = get_reg_kdata(reg_idx=context.reg_kdata[0])
    print(data0)
    cash = context.account(account_idx=0).cash
    print('cash =', cash)
    order_volume(account_idx=0, target_idx=0, volume=1, side=1, position_effect=1, order_type=2)
    
if __name__ == '__main__':
    run_backtest(strategy_name='chapter2', file_path='.', target_list=['SSE_600000'], frequency='min', fre_num=15, begin_date='2025-06-01', end_date='2025-10-19')