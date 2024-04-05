import os
import pandas as pd




def read_ratios(ticker, base_path, files):
    income_statement_file = [f for f in files if 'Financial Ratios' in f][0]
    df = pd.read_excel(f"{base_path}/{ticker}/{income_statement_file}")
    cols = {col: col.split("\n")[0].strip() for col in df.columns}
    cols['Period Ending:'] = 'Category'
    df.rename(columns=cols, inplace=True)
    df_ratios = df.iloc[1:]
    df_ratios["Category"] = [val.strip() for val in df_ratios["Category"]]
    return df_ratios

def read_balance_sheet(ticker, base_path, files):
    balance_sheet_file = [f for f in files if 'Balance Sheet' in f][0]
    df = pd.read_excel(f"{base_path}/{ticker}/{balance_sheet_file}")
    cols = {col: col.split("\n")[0].strip() for col in df.columns}
    cols['Period Ending:'] = 'Category'
    df.rename(columns=cols, inplace=True)
    df_balance = df.iloc[1:]
    return df_balance

## -- Income Statement -- ##
def read_income_statement(ticker, base_path, files):
    income_statement_file = [f for f in files if 'Income Statement' in f][0]
    df = pd.read_excel(f"{base_path}/{ticker}/{income_statement_file}")
    cols = {col: col.split("\n")[0].strip() for col in df.columns}
    cols['Period Ending:'] = 'Category'
    df.rename(columns=cols, inplace=True)
    df_income = df.iloc[1:]
    return df_income

## -- Cash Flow -- ##
def read_cash_flow(ticker, base_path, files):
    cash_flow_file = [f for f in files if 'Cash Flow Statement' in f][0]
    df = pd.read_excel(f"{base_path}/{ticker}/{cash_flow_file}")
    cols = {col: col.split("\n")[0].strip() for col in df.columns}
    cols['Period Ending:'] = 'Category'
    df.rename(columns=cols, inplace=True)
    df_cash = df.iloc[1:]
    return df_cash


def read_financials_data(ticker):
    base_path = 'data'
    files = os.listdir(f'{base_path}/{ticker}')
    df_balance = read_balance_sheet(ticker, base_path, files)
    df_income  = read_income_statement(ticker, base_path, files)
    df_cash    = read_cash_flow(ticker, base_path, files)
    df_ratios  = read_ratios(ticker, base_path, files)
    return df_balance, df_income, df_cash, df_ratios

