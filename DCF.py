import pandas as pd
from data import read_financials_data
import os
import yfinance as yf
import numpy as np
from consts import *
from ratios import calculate_growth
from numpy import ones,vstack
from numpy.linalg import lstsq
from sklearn.metrics import mean_absolute_error

def from_str_float(val):
    if type(val) == str:
        val = float(val.replace(",","").replace("%", ""))
    else:
        val = float(val)
    return val

def get_FCF(ticker, df_cash):
    FCF = df_cash[df_cash["Category"] == 'Free Cash Flow']["LTM"].item()
    FCF = from_str_float(FCF)
    return FCF

def get_WACC(ticker, df_income, df_balance):

    # Weights
    base_path = '/Users/yardenrotem/PycharmProjects/pythonProject/data'
    files = [f for f in os.listdir(f'{base_path}/{ticker}')]

    # Interest Income
    interest_income = df_income[df_income["Category"] == "Interest Income"].iloc[0].values[1]
    interest_income = from_str_float(interest_income)

    # Interest Expense
    interest_expense = df_income[df_income["Category"] == "Interest Expense"].iloc[0].values[1]
    interest_expense = np.absolute(from_str_float(interest_expense))

    # Market cap
    stock_ticker = yf.Ticker(ticker)
    market_cap = stock_ticker.info["marketCap"] / 1000000

    # Equity
    equity = market_cap + interest_income - interest_expense

    # Short term debt
    short_term_debt = df_balance[df_balance["Category"] == "Notes Payable/Short Term Debt"].iloc[0].values[1]
    short_term_debt = from_str_float(short_term_debt)

    # Long term debt
    long_term_debt = df_balance[df_balance["Category"] == "Total Long Term Debt"].iloc[0].values[1]
    long_term_debt = from_str_float(long_term_debt)

    # Debt
    debt = short_term_debt + long_term_debt

    # Weights
    We = equity / (equity + debt)
    Wd = debt   / (equity + debt)

    # Cost of Equity
    risk_free_rate  = 3
    expected_market = 8
    beta = stock_ticker.info['beta']
    Ce = risk_free_rate + beta * (expected_market - risk_free_rate)

    # Cost of debt
    country = stock_ticker.info.get('country', 'Not available')
    tax_rate = country_to_tax[country]
    ebit = df_income[df_income["Category"] == "Operating Income"].iloc[0].values[1]
    ebit = np.absolute(from_str_float(ebit))
    spread = ebit / interest_expense
    Cd = (risk_free_rate + spread) * (1 - tax_rate)

    # WACC
    WACC = We*Ce + Wd*Cd

    return round(WACC / 100, 2), country

def discount_factor(WACC, n):
    return 1 / (np.power(1+WACC,n))

def estimate_growth(df_cash):
    all_FCF = df_cash[df_cash["Category"] == "Free Cash Flow"].iloc[0].values[1:]
    all_FCF = [from_str_float(val) for val in all_FCF]
    max_len = min(len(all_FCF), 11) - 1
    growths = [calculate_growth(all_FCF[i], all_FCF[i+1]) for i in range(max_len)]
    growths = [min(max(-20, val), 20) for val in growths]
    growth_rate = np.mean(growths) * 0.8
    return growth_rate / 100

def discounted_fcf_calculate(fcf, i, WACC, growth):
    return (fcf * np.power(1+growth,i)) * discount_factor(WACC, i)

def future_fcf_calac(fcf, i, growth):
    return fcf * np.power(1 + growth, i)

def get_dcf_table(FCF, WACC, df_cash):
    growth = estimate_growth(df_cash)
    future_fcf = [future_fcf_calac(FCF, i, growth) for i in range(1,11)]
    discounted_fcf = [discounted_fcf_calculate(FCF, i, WACC, growth) for i in range(1,11)]
    return discounted_fcf, future_fcf, growth

def get_NPV(dcf_table):
    return sum(dcf_table)

def get_terminal_value(dcf_table, country, WACC):
    perpetuity_growth = country_to_GPD[country]
    return (dcf_table[-1] * (1+perpetuity_growth)) / (WACC - perpetuity_growth)

def get_discounted_terminal_value(TV, WACC):
    return TV * discount_factor(WACC, 10)

def get_instrict_value(NPV, DTV):
    return NPV + DTV

def get_instrict_value_per_share(instrict_value, df_balance, df_income):
    cash = df_balance[df_balance["Category"] == "Cash & Equivalents"].iloc[0].values[1]
    cash = np.absolute(from_str_float(cash))
    debt = df_balance[df_balance["Category"] == "Total Liabilities"].iloc[0].values[1]
    debt = np.absolute(from_str_float(debt))
    # Diluted Weighted Average Shares Outstanding
    shares = df_income[df_income["Category"] == "Diluted Weighted Average Shares Outstanding"].iloc[0].values[1]
    shares = np.absolute(from_str_float(shares))

    return round((instrict_value + cash - debt) / (shares),2)


def get_margin_of_safety(ticker, instrict_value_per_share):
    if instrict_value_per_share <= 0:
        return 0
    stock_data = yf.Ticker(ticker)
    current_price = stock_data.history(period='1d')['Close'][0]
    return round(100* (1 - (current_price / instrict_value_per_share)) ,2), current_price

def DCF(ticker):

    results = {}

    df_balance, df_income, df_cash, df_ratios = read_financials_data(ticker)

    # FCF
    FCF = get_FCF(ticker, df_cash)

    # WACC
    WACC, country = get_WACC(ticker, df_income, df_balance)
    results["WACC"] = round(WACC * 100, 2)

    # DCF
    discounted_fcf, future_fcf, growth = get_dcf_table(FCF, WACC, df_cash)
    results["growth"] = round(growth * 100, 2)

    # NPV
    NPV  = get_NPV(discounted_fcf)

    # Terminal Value
    TV = get_terminal_value(future_fcf, country, WACC)

    # Discounted Terminal Value
    DTV = get_discounted_terminal_value(TV, WACC)

    # Instrict Value
    instrict_value = get_instrict_value(NPV, DTV)

    # Instrict Value per share
    instrict_value_per_share = get_instrict_value_per_share(instrict_value, df_balance, df_income)
    results["instrict_value_per_share"] = instrict_value_per_share

    # Margin of safety
    margin_of_safety, current_price = get_margin_of_safety(ticker, instrict_value_per_share)
    results["current_price"] = round(current_price,2)
    results["margin_of_safety"] = margin_of_safety

    return results


if __name__ == "__main__":
    print(DCF('ANET'))