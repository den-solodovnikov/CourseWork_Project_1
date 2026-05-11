from datetime import datetime, time

from src.utils import get_df_from_file


def greetings() -> str:
    """ Функция приветствия. В зависимости от текущего времени выбирает тип приветствия. """
    date_now = datetime.now().time()
    if time(6, 0, 0) <= date_now <= time(11, 59, 59):
        greeting = 'Доброе утро'
    elif time(12, 0, 0) <= date_now <= time(17, 59, 59):
        greeting = 'Добрый день'
    elif time(18, 0, 0) <= date_now <= time(22, 59, 59):
        greeting = 'Добрый вечер'
    else:
        greeting = 'Доброй ночи'
    return greeting


def get_transactions_total_spent() -> list:
    """ Функция выводит суммарную информацию по картам: последние 4 цифры карты;
    общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей). Данные поступают из внешнего файла. """
    df_transactions = get_df_from_file()
    df_transactions = df_transactions.dropna(subset="Номер карты")
    df_grouped = (df_transactions[df_transactions['Сумма платежа'] < 0].groupby('Номер карты')['Сумма платежа'].
                  sum().apply(lambda x: round(abs(x), 2)))
    data_spent = df_grouped.to_dict()
    cards = []
    for item, value in data_spent.items():
        item = str(item)[1:]
        cards.append({'last_digits': item, "total_spent": value, "cashback": round((value / 100), 2)})
    return cards


def get_top_transactions() -> list[dict]:
    """ Функция выводит топ 5 транзакций по сумме платежа. """
    df_transactions = get_df_from_file()
    df_transactions = df_transactions.dropna(subset="Номер карты")
    df_sorted = (df_transactions[['Дата платежа', 'Сумма платежа', "Категория", "Описание"]].
                 sort_values(by='Сумма платежа', key=abs, ascending=False).head(5))
    df_top = df_sorted.rename(columns={
        'Дата платежа': 'date',
        'Сумма платежа': 'amount',
        'Категория': 'category',
        'Описание': 'description'
    })
    data_top = df_top.to_dict(orient='records')

    return data_top
