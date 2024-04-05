from consts import *
from ratios import get_screening_ratios
import pandas as pd
import numpy as np
import os
import warnings
from tqdm import tqdm
from DCF import DCF
warnings.filterwarnings('ignore')
def filter_market_cap(df):
    return df[df[MARKET_CAP].between(FILTER_MARKET_CAP_SIZE[0],FILTER_MARKET_CAP_SIZE[1])]

def filter_sector(df):
    return df[df[SECTOR].isin(FILTER_SECTORS)]

def filter_exchange(df):
    return df[df[EXCHANGE].isin(FILTER_EXCHANGE)]


def screen_criteria(ticker, df_ratios, df_static_ratios):
    cols = ["Ticker"]
    df_ticker = pd.DataFrame(columns=cols)
    revenue_growths = df_ratios[df_ratios["Category"] == 'REVENUE_GROWTH'].iloc[0].values[1:]
    revenue_growths = [val for val in revenue_growths if not pd.isnull(val)]

    results = {"ticker": ticker}
    # TEST 1 - Hard revenue test
    is_all_revenue_growth_larger_than_5 = sum([val>=5 for val in revenue_growths])
    results["is_all_revenue_growth_larger_than_5"] = is_all_revenue_growth_larger_than_5


    # TEST 2 - Easy revenue test
    median_revenue_growth = round(np.median(revenue_growths),2)
    results["median_revenue_growth"] = median_revenue_growth

    # TEST 3 - Hard EPS test
    eps_growths = df_ratios[df_ratios["Category"] == 'EPS_GROWTH'].iloc[0].values[1:]
    eps_growths = [val for val in eps_growths if not pd.isnull(val)]
    is_all_eps_growth_larger_than_10 = sum([val >= 10 for val in eps_growths])
    results["is_all_eps_growth_larger_than_10"] = is_all_eps_growth_larger_than_10

    # TEST 4 - Easy EPS test
    median_eps_growth = round(np.median(eps_growths), 2)
    results["median_eps_growth"] = median_eps_growth

    # TEST 5 - Hard ROIC test
    roic = df_ratios[df_ratios["Category"] == 'ROIC'].iloc[0].values[1:]
    roic = [val for val in roic if not pd.isnull(val)]
    is_roic_larger_than_15 = sum([val >= 15 for val in roic])
    results["is_roic_larger_than_15"] = is_roic_larger_than_15

    # TEST 6 - Easy ROIC test
    median_roic = round(np.median(roic), 2)
    results["median_roic"] = median_roic

    # TEST 7 - Hard ROE test
    roe = df_ratios[df_ratios["Category"] == 'ROE'].iloc[0].values[1:]
    roe = [val for val in roe if not pd.isnull(val)]
    is_roe_larger_than_15 = sum([val >= 15 for val in roe])
    results["is_roe_larger_than_15"] = is_roe_larger_than_15

    # TEST 8 - Easy ROIC test
    median_roe = round(np.median(roe), 2)
    results["median_roe"] = median_roe

    # TEST 9 - Last year ICR test
    icr = df_ratios[df_ratios["Category"] == 'ICR'].iloc[0].values[1]
    results["icr"] = icr

    # TEST 10 - Last year PEG test
    peg = df_static_ratios["PEG"].item()
    results["peg"] = peg
    return results




def screen_warren_criteria(ticker):
    df_ratios, df_static_ratios = get_screening_ratios(ticker)
    return screen_criteria(ticker, df_ratios, df_static_ratios)

def filter_basic(df):
    df = filter_market_cap(df)
    df = filter_sector(df)
    df = filter_exchange(df)
    return df.reset_index(drop=True)


def total_score(row):
  total_score = 0
  for col in row.keys():
    if "score" in col:
      total_score += row[col]
  return total_score

def score_column(col, val):
  if col == 'is_all_revenue_growth_larger_than_5':
    if val == 8:
      return 1
    if val == 9:
      return 2
    if val >= 10:
      return 3
  if col == 'median_revenue_growth':
    if 50 < val <= 72:
      return 1
    if 72 < val <= 128:
      return 2
    if val > 128:
      return 3
  if col == 'is_all_eps_growth_larger_than_10':
    if val == 6:
      return 1
    if val == 7:
      return 2
    if val >= 8:
      return 3
  if col == 'median_eps_growth':
    if 48 < val <= 68:
      return 1
    if 68 < val <= 104:
      return 2
    if val > 104:
      return 3
  if col == 'is_roic_larger_than_15':
    if 4 <= val <= 5:
      return 1
    if 6 <= val <= 7:
      return 2
    if val >= 8:
      return 3
  if col == 'median_roic':
    if 18 < val <= 32:
      return 1
    if 32 < val <= 120:
      return 2
    if val > 120:
      return 3
  if col == 'is_roe_larger_than_15':
    if 6 <= val <= 6:
      return 1
    if 7 <= val <= 8:
      return 2
    if val >= 9:
      return 3
  if col == 'median_roe':
    if 24 < val <= 39:
      return 1
    if 39 < val <= 72:
      return 2
    if val > 72:
      return 3
  if col == 'icr':
    if 10 < val <= 34:
      return 1
    if 34 < val <= 62:
      return 2
    if val > 62:
      return 3
  if col == 'peg':
    if 0.35 < val <= 1:
      return 1
    if 0.2 < val <= 0.35:
      return 2
    if 0 < val <= 0.2:
      return 3
  return 0



def get_warren_screening():
    tickers = sorted(os.listdir('data'))
    file1 = open('skip.txt', 'r')
    skips = [val.replace('\n', '') for val in file1.readlines()]

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
            "peg",
            "WACC",
            "growth",
            "instrict_value_per_share",
            "current_price",
            "margin_of_safety"]

    screening_df = pd.DataFrame(columns=cols)
    for ticker in tqdm(tickers):
        if '.' in ticker or ticker in skips:
            continue
        try:
            results_dict = screen_warren_criteria(ticker)
            DCF_results = DCF(ticker)
            results_dict.update(DCF_results)
            screening_df = pd.concat([screening_df, pd.DataFrame.from_dict([results_dict])], ignore_index=True)
        except:
            continue

    skip_cols = [
            "ticker",
            "WACC",
            "growth",
            "instrict_value_per_share",
            "current_price",
            "margin_of_safety"]
    for col in screening_df.columns:
        if col in skip_cols:
            continue
        screening_df[f"{col}_score"] = screening_df[col].apply(lambda val: score_column(col, val))

    screening_df["total_score"] = screening_df.apply(lambda row: total_score(row), axis=1)



    screening_df.sort_values(by='total_score', ascending=False, inplace=True)
    return screening_df

if __name__ == "__main__":
    df = get_warren_screening()
    print(df)
