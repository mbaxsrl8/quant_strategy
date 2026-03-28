from atrader.calcfactor import *
from atrader import *

def init(context: ContextFactor):
    reg_factor(["pb_ratio_ttm"])
    
def calc_factor(context: ContextFactor):
    result = get_reg_factor(context.reg_factor[0], df=True)
    result = result['value'].values
    return result.reshape(-1, 1)

if __name__ == "__main__":
    run_factor(factor_name="pb_ratio_ttm", file_path='.', targets='hs300', begin_date="2025-04-01", end_date="2026-03-01", fq=1)