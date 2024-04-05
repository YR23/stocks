from data import read_financials_data
import pandas as pd
import numpy as np

def get_relevant_years(df):
    years_columns = sorted([year for year in df.columns if year.strip().isnumeric()], reverse=True)[:11]
    return years_columns


def get_current_and_last_value(category, df_balance, df_income, df_cash, df_financial_ratios, year, last_year):
    this_year_value, last_year_value = 0,0

    if category == 'Revenue':
        try:
            rev = df_income[df_income["Category"] == category]
            this_year_value = float(rev[year].item().replace(',', ''))
            last_year_value = float(rev[last_year].item().replace(',', ''))
        except:
            this_year_value, last_year_value = 0, 0

    if category == 'EPS':
        net_income = df_income[df_income["Category"] == 'Net Income']
        dividend_paid = df_cash[df_cash["Category"] == 'Dividends Paid']
        shares_outstanding = df_income[df_income["Category"] == 'Diluted Weighted Average Shares Outstanding']

        current_net_income = float(net_income[year].item().replace(',',''))
        current_dividend_paid = float(dividend_paid[year].item().replace(',',''))
        current_shares_outstanding = float(shares_outstanding[year].item().replace(',',''))
        if current_shares_outstanding == 0:
            this_year_value = 0
        else:
            this_year_value = round((current_net_income + current_dividend_paid) / current_shares_outstanding, 2)

        last_year_net_income = float(net_income[last_year].item().replace(',',''))
        last_year_dividend_paid = float(dividend_paid[last_year].item().replace(',',''))
        last_year_shares_outstanding = float(shares_outstanding[last_year].item().replace(',',''))
        if last_year_shares_outstanding == 0:
            last_year_value = 0
        else:
            last_year_value = round((last_year_net_income + last_year_dividend_paid) / last_year_shares_outstanding, 2)

    if category == "PEG":
        try:
            peg = df_financial_ratios[df_financial_ratios["Category"] == 'Price Earnings to Growth Ratio']
            this_year_value = float(peg[year].item().replace('%', '').replace(',',''))
            last_year_value = float(peg[last_year].item().replace('%', '').replace(',',''))
        except:
            this_year_value, last_year_value = 0, 0

    if category == 'ICR':
        try:
            icr = df_financial_ratios[df_financial_ratios["Category"] == 'Interest Coverage Ratio']
            this_year_value = float(icr[year].item().replace('%', '').replace(',',''))
            last_year_value = float(icr[last_year].item().replace('%', '').replace(',',''))
        except:
            this_year_value, last_year_value = 0, 0

    if category == 'ROIC':
        try:
            roic = df_financial_ratios[df_financial_ratios["Category"] == 'Return on Invested Capital']
            this_year_value = float(roic[year].item().replace('%', '').replace(',',''))
            last_year_value = float(roic[last_year].item().replace('%', '').replace(',',''))
        except:
            this_year_value, last_year_value = 0, 0

    if category == 'ROE':
        try:
            roe = df_financial_ratios[df_financial_ratios["Category"] == 'Return on Equity']
            this_year_value = float(roe[year].item().replace('%', '').replace(',',''))
            last_year_value = float(roe[last_year].item().replace('%', '').replace(',',''))
        except:
            this_year_value, last_year_value = 0, 0

    return this_year_value, last_year_value


def calculate_growth(final_value, original_value):
    growth = 0
    if final_value > 0 and original_value> 0:
        growth = round(((final_value / original_value) - 1) * 100, 2)
    if final_value > 0 and original_value < 0:
        growth = round((100 * (final_value - original_value)/ np.absolute(original_value)),2)
    if final_value < 0 and original_value > 0:
        growth = round((100 * (final_value - original_value)/ original_value),2)
    if final_value < 0 and original_value < 0:
        growth = round((100 * (final_value - original_value) / np.absolute(original_value)), 2)
    return growth

def calculate_current_ratio(category, df_balance, df_income, df_cash, df_financial_ratios, years_columns, idx):
    year = years_columns[idx]
    last_year = years_columns[idx+1]
    data_dict = {}
    this_year_value, last_year_value = get_current_and_last_value(category, df_balance, df_income, df_cash, df_financial_ratios, year, last_year)

    if last_year_value == 0:
        growth = 0
    else:
        growth = calculate_growth(this_year_value, last_year_value)
        # growth = round((this_year_value / last_year_value - 1) * 100, 2)
    data_dict.update({year: [this_year_value, growth]})
    return data_dict


def get_value_and_growth(category, df_balance, df_income, df_cash, df_financial_ratios, years_columns):
    data_dict = {'Category': [category, f"{category.upper()}_GROWTH"]}
    for idx in range(len(years_columns) - 1):
        curr_dict = calculate_current_ratio(category, df_balance, df_income, df_cash, df_financial_ratios, years_columns, idx)
        data_dict.update(curr_dict)
    return data_dict

def calcluate_static_ratio(ratio, df_ratios, df_balance, df_income, df_cash, df_financial_ratios):
    if ratio == 'PEG':
        pe  = df_financial_ratios[df_financial_ratios["Category"] == 'Price to Earnings Ratio']
        pe = float(pe.iloc[0]["LTM"].replace('%', '').replace(',',''))
        eps_growth = df_ratios[df_ratios["Category"] == 'EPS_GROWTH'].iloc[0].values[1:]
        eps_growth = np.nanmedian(eps_growth)
        if pe <= 0 or eps_growth <= 0:
            peg = -1
        else:
            peg = round(pe / eps_growth,2)
    return [peg]

def get_screening_ratios(ticker):
    df_balance, df_income, df_cash, df_financial_ratios = read_financials_data(ticker)
    income_years_columns = get_relevant_years(df_income)
    balance_years_columns = get_relevant_years(df_balance)
    cash_years_columns    = get_relevant_years(df_cash)
    ratios_years_columns  = get_relevant_years(df_financial_ratios)
    income_balance = list(set(income_years_columns) & set(balance_years_columns))
    cash_ratios    = list(set(cash_years_columns) & set(ratios_years_columns))
    years_columns  = sorted(list(set(income_balance) & set(cash_ratios)), reverse=True)
    columns = ['Category'] + years_columns
    df_ratios = pd.DataFrame(columns=columns)

    ratios = ["Revenue", "EPS", "ROIC", "ROE", "ICR"]
    for ratio in ratios:
        data_dict = get_value_and_growth(ratio, df_balance, df_income, df_cash, df_financial_ratios, years_columns)
        df_ratios = pd.concat([df_ratios, pd.DataFrame(data_dict)], ignore_index=True)

    df_static_ratios = pd.DataFrame(columns=["PEG"])
    for ratio in df_static_ratios.columns:
        df_static_ratios[ratio] = calcluate_static_ratio(ratio, df_ratios, df_balance, df_income, df_cash, df_financial_ratios)
    return df_ratios, df_static_ratios

if __name__ == "__main__":
    import warnings
    from tqdm import tqdm
    warnings.filterwarnings('ignore')
    import os
    for ticker in tqdm(os.listdir('data')[:1000]):
        try:
            get_screening_ratios(ticker)
        except:
            continue

