from atrader import *

factor_data_1 = get_factor_by_code(factor_list=['PE', 'PB'], target='SZSE.000001', begin_date='2025-01-01', end_date='2025-06-30')
print(factor_data_1)