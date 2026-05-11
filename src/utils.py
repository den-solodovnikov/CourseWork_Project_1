import json
import os
import time
from os.path import abspath
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

from src import app_logger

if __name__ == "__main__":
    module_name = os.path.splitext(os.path.basename(__file__))[0]
else:
    module_name = __name__
logger = app_logger.get_logger(module_name)


PATH_TO_DATA = abspath(Path('../data/operations.xlsx'))


def get_df_from_file(path: str = PATH_TO_DATA) -> pd.DataFrame | None:
    """ Функция считывания данных из EXCEL-файла в формат DataFrame. """

    try:
        logger.info('Запуск функции считывания данных из EXCEL-файла')
        df_data = pd.read_excel(path)
        return df_data
    except Exception as ex:
        print('Ошибка открытия файла. Файл не найден')
        logger.error(f'Произошла ошибка открытия файла: {ex}')



def currency_conversion() -> list:
    """ Функция обращается к внешнему API для получения текущего курса валют
    из данных в "user_settings.json". """
    load_dotenv()
    API_KEY = os.getenv('API_KEY_APILAYER')
    headers = {"apikey": f'{API_KEY}'}
    url = 'https://api.apilayer.com/exchangerates_data/convert'
    logger.info('Запуск функции получения текущего курса валют')
    currency_rates = []
    try:
        logger.info('Открываем файл user_settings.json для получения списка валют')
        with open('../user_settings.json') as json_file:
            settings = json.load(json_file)
            user_currencies = settings['user_currencies']
            for currency in user_currencies:
                params = {
                    "to": "RUB",
                    "from": f'{currency}',
                    "amount": f'{1}'
                }
                logger.info('Получение данных курса валют их внешнего API')
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                if response.status_code == 200:
                    logger.info(f'Получен доступ к внешнему API, код: {response.status_code}')
                    currency_rates.append({'currency': currency, 'rate': data['result']})
                else:
                    logger.error(f'Ошибка доступа к внешнему API, код: {response.status_code}')
                    print('Ошибка доступа к серверу')
    except FileNotFoundError as ex:
        logger.error(f'Ошибка открытия файла user_settings.json: {ex}')
        print('Не найден файл user_settings.json')

    return currency_rates


def stock_prices_api() -> list | None:
    """ Функция получения курса акций, указанных в user_settings.json из внешнего API-источника. """
    load_dotenv()
    API_KEY = os.getenv('API_KEY_ALPHA_VANTAGE')
    headers = {"apikey": f'{API_KEY}'}
    url = 'https://www.alphavantage.co/query'
    logger.info('Запуск функции получения курса акций')
    stock_prices = []
    try:
        logger.info('Открываем файл user_settings.json для получения списка акций')
        with open('../user_settings.json') as json_file:
            settings = json.load(json_file)
            user_stocks = settings['user_stocks']
            for stock in user_stocks:
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": f'{stock}',
                    "apikey": f'{API_KEY}'
                }
                logger.info('Получение данных курса акций их внешнего API')
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                time.sleep(2)

                if response.status_code == 200:
                    logger.info(f'Получен доступ к внешнему API, код: {response.status_code}')
                    stock_prices.append({'stock': stock, 'price': data['Global Quote']['05. price']})
                else:
                    logger.error(f'Ошибка доступа к внешнему API, код: {response.status_code}')
                    print('Ошибка доступа к серверу')
    except FileNotFoundError as ex:
        logger.error(f'Ошибка открытия файла user_settings.json: {ex}')
        print('Не найден файл user_settings.json')
    return stock_prices
