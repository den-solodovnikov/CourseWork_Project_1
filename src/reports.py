import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src import app_logger

if __name__ == "__main__":
    module_name = os.path.splitext(os.path.basename(__file__))[0]
else:
    module_name = __name__
logger = app_logger.get_logger(module_name)


def report_to_file(file_name=None):
    """ Декоратор, записывающий в JSON-файл результат-отчет функции.
     Декоратор без параметра — записывает данные отчета в файл 'func_name_report.json'.
     Декоратор с параметром — принимает имя файла в качестве параметра. """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f'Запускаем выполнение декорируемой функции: {func.__name__}')
            result_df = func(*args, **kwargs)
            logger.info('Преобразование полученного результата DataFrame в словарь')
            result_dict = result_df.to_dict(orient='records')
            logger.info('Проверка передачи параметра "file_name"')
            if file_name:
                logger.info(f'Указан файл для записи: {file_name}')
                filename_ = f'../data/{file_name}'
            else:
                filename_ = f'../data/{func.__name__}_report.json'
                logger.info('Файл не указан, запись по умолчанию.')
            try:
                logger.info(f'Выполнение записи в файл: {filename_}.')
                with open(filename_, 'w', encoding='utf-8') as f:
                    json.dump(result_dict, f, ensure_ascii=False, indent=4)
            except Exception as ex:
                logger.error(f'Произошла ошибка: {ex}')
                print(f'Ошибка записи в файл: {filename_}.\n{ex}')
            return result_df
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Функция принимает на вход: DataFrame с транзакциями, название категории,
    опциональную дату в формате 'dd.mm.YYYY' Если дата не передана, то берется текущая дата.
    Возвращает траты по заданной категории за последние три месяца (от переданной даты). """
    if date is None:
        date_end = datetime.today()
        logger.info(f'Дата не указана, устанавливаем текущую: {date_end}')
    else:
        date_end = datetime.strptime(date, '%d.%m.%Y')
        logger.info(f'Указана дата: {date_end}')
    date_start = date_end - relativedelta(months=3)
    logger.info(f'Установка начала периода: {date_start}')
    df_date = transactions
    df_date['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)
    logger.info(f'Фильтруем по временному периоду и категории: {category}')
    filtered_transactions = df_date[(df_date['Дата операции'].between(date_start, date_end))
                                    & (df_date['Категория'].str.contains(category.lower(), case=False, na=False))]
    filtered_transactions['Дата операции'] = filtered_transactions['Дата операции'].dt.strftime('%d.%m.%Y %H:%M:%S')
    if filtered_transactions.empty:
        logger.info('Не найдены транзакции с указанными параметрами.')
    else:
        logger.info('Найдены транзакции. Передаются для записи в файл.')
    return filtered_transactions
