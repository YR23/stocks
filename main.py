import pandas as pd
from screener import *
from scrap import scrap_ticker
from ratios import get_screening_ratios
import os
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')





tickers = sorted(os.listdir('data'))
file1 = open('skip.txt', 'r')
skips = [val.replace('\n','') for val in file1.readlines()]
cols = ["ticker",
        "is_all_revenue_growth_larger_than_5",
        "median_revenue_growth",
        "is_all_eps_growth_larger_than_10",
        "median_eps_growth",
        "is_roic_larger_than_15",
        "median_roic",
        "is_roe_larger_than_15",
        "median_roe",
        "icr",
        "peg"]



    # print()
    # break
#



