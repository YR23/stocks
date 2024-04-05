import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from screener import *
from tqdm import tqdm


def scrap_all_stocks():
    df = pd.read_csv('stocks.csv')
    df = filter_basic(df)
    tickers = df[TICKER].values
    dones = os.listdir('/Users/yardenrotem/PycharmProjects/pythonProject/data')
    for tick in tqdm(tickers):
        # if tick in dones:
        #     continue
        files_done = os.listdir(f'/Users/yardenrotem/PycharmProjects/pythonProject/data/{tick}')
        ratios = [f for f in files_done if 'Income Statement' in f]
        if len(ratios) == 0:
            scrap_ticker(tick)

def scrap_ticker(ticker):
    try:
        scrap_ticker_income(ticker)
        scrap_ticker_balance(ticker)
        scrap_ticker_cash(ticker)
        scrap_ticker_ratios(ticker)
    except:
        file1 = open("/Users/yardenrotem/PycharmProjects/pythonProject/failed.txt", "a")  # append mode
        file1.write(f"{ticker} \n")
        file1.close()

def scrap_ticker_income(ticker):
    print(f"Scraping income ticker: {ticker}")
    # Set the path to the ChromeDriver
    chrome_driver_path = '/Users/yardenrotem/PycharmProjects/pythonProject/chrome/chromedriver'  # Replace with the actual path
    download_path      = f'/Users/yardenrotem/PycharmProjects/pythonProject/data/{ticker}'
    os.makedirs(download_path, exist_ok=True)

    # Create a ChromeOptions object and set the executable path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={chrome_driver_path}")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # To disable the download prompt
        "profile.default_content_setting_values.automatic_downloads": 1
    })

    # Create a new instance of the Chrome driver with the ChromeOptions object
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    ## -- Income Statment -- ##
    url = f'https://discountingcashflows.com/company/{ticker}/income-statement/'  # Replace with the URL of the website you want to visit
    # url = 'driver.get("chrome://settings/?search=Downloads")'
    driver.get(url)
    time.sleep(5)

    button_id = "/html/body/div[1]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[4]/button"  # Replace with the actual ID of your button
    button = driver.find_element(By.XPATH, button_id)
    # Click the button
    driver.execute_script("arguments[0].click();", button)
    time.sleep(5)
    driver.quit()

def scrap_ticker_balance(ticker):
    print(f"Scraping balance ticker: {ticker}")
    # Set the path to the ChromeDriver
    chrome_driver_path = '/Users/yardenrotem/PycharmProjects/pythonProject/chrome/chromedriver'  # Replace with the actual path
    download_path      = f'/Users/yardenrotem/PycharmProjects/pythonProject/data/{ticker}'
    os.makedirs(download_path, exist_ok=True)

    # Create a ChromeOptions object and set the executable path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={chrome_driver_path}")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # To disable the download prompt
        "profile.default_content_setting_values.automatic_downloads": 1
    })

    # Create a new instance of the Chrome driver with the ChromeOptions object
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    url = f'https://discountingcashflows.com/company/{ticker}/balance-sheet-statement/'  # Replace with the URL of the website you want to visit
    # url = 'driver.get("chrome://settings/?search=Downloads")'
    driver.get(url)
    time.sleep(5)

    button_id = "/html/body/div[1]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[4]/button"  # Replace with the actual ID of your button
    button = driver.find_element(By.XPATH, button_id)
    # Click the button
    driver.execute_script("arguments[0].click();", button)
    time.sleep(5)
    driver.quit()


def scrap_ticker_cash(ticker):
    print(f"Scraping cash ticker: {ticker}")
    # Set the path to the ChromeDriver
    chrome_driver_path = '/Users/yardenrotem/PycharmProjects/pythonProject/chrome/chromedriver'  # Replace with the actual path
    download_path      = f'/Users/yardenrotem/PycharmProjects/pythonProject/data/{ticker}'
    os.makedirs(download_path, exist_ok=True)

    # Create a ChromeOptions object and set the executable path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={chrome_driver_path}")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # To disable the download prompt
        "profile.default_content_setting_values.automatic_downloads": 1
    })

    # Create a new instance of the Chrome driver with the ChromeOptions object
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    url = f'https://discountingcashflows.com/company/{ticker}/cash-flow-statement/'  # Replace with the URL of the website you want to visit
    # url = 'driver.get("chrome://settings/?search=Downloads")'
    driver.get(url)
    time.sleep(5)

    button_id = "/html/body/div[1]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[4]/button"  # Replace with the actual ID of your button
    button = driver.find_element(By.XPATH, button_id)
    # Click the button
    driver.execute_script("arguments[0].click();", button)
    time.sleep(5)
    driver.quit()


def scrap_ticker_ratios(ticker):
    print(f"Scraping ratios ticker: {ticker}")
    # Set the path to the ChromeDriver
    chrome_driver_path = '/Users/yardenrotem/PycharmProjects/pythonProject/chrome/chromedriver'  # Replace with the actual path
    download_path      = f'/Users/yardenrotem/PycharmProjects/pythonProject/data/{ticker}'
    os.makedirs(download_path, exist_ok=True)

    # Create a ChromeOptions object and set the executable path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={chrome_driver_path}")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # To disable the download prompt
        "profile.default_content_setting_values.automatic_downloads": 1
    })

    # Create a new instance of the Chrome driver with the ChromeOptions object
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the website
    url = f'https://discountingcashflows.com/company/{ticker}/ratios/'  # Replace with the URL of the website you want to visit
    # url = 'driver.get("chrome://settings/?search=Downloads")'
    driver.get(url)
    time.sleep(5)

    button_id = "/html/body/div[1]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[3]/button"
    button = driver.find_element(By.XPATH, button_id)
    # Click the button
    driver.execute_script("arguments[0].click();", button)
    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    scrap_all_stocks()

