import os
import re

from src import app_logger

if __name__ == "__main__":
    module_name = os.path.splitext(os.path.basename(__file__))[0]
else:
    module_name = __name__
logger = app_logger.get_logger(module_name)


def search_description(transactions: list[dict], descript_word: str) -> list:
    """ Функция для поиска в списке словарей операций по заданной строке.
    Возвращает JSON с операциями, у которых в поле 'Категория' или 'Описание' есть строка,
    переданная аргументу функции. """
    transactions_result = []
    try:
        logger.info(f'Запуск простого поиска транзакций по строке: {descript_word}')
        pattern = re.compile(descript_word, re.IGNORECASE)
        for transaction in transactions:
            if (pattern.search(str(transaction.get('Категория', '')).lower())
                    or pattern.search(str(transaction.get('Описание', '')).lower())):
                transactions_result.append(transaction)
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print(f'Ошибка {ex}')
    if not transactions_result:
        logger.info('Не найдены транзакции с указанными параметрами.')
    else:
        logger.info('Транзакции найдены')
    return transactions_result


def search_by_individual(transactions: list[dict]) -> list:
    """ Функция для поиска в списке словарей операций которые относятся к переводам физ.лицам.
    Возвращает JSON с операциями, у которых в поле 'Категория' - Переводы,
    а в описании есть имя и первая буква фамилии с точкой. """
    transactions_result = []
    try:
        logger.info('Запуск поиска транзакций по физ.лицам')
        pattern1 = re.compile('Перевод', re.IGNORECASE)
        pattern2 = re.compile(r'[А-Яа-яA-Za-z]+\s[A-ZА-Я]{1}[.]{1}')
        for transaction in transactions:
            if (pattern1.search(str(transaction.get('Категория', '')).lower())
                    and pattern2.search(str(transaction.get('Описание', '')))):
                transactions_result.append(transaction)
    except Exception as ex:
        logger.error(f'Произошла ошибка: {ex}')
        print(f'Ошибка {ex}')
    if not transactions_result:
        logger.info('Не найдены транзакции с указанными параметрами.')
    else:
        logger.info('Транзакции найдены')
    return transactions_result
