from src.utils import currency_conversion, stock_prices_api
from src.views import (get_top_transactions, get_transactions_total_spent,
                       greetings)

if __name__ == '__main__':
    date_user = input('Введите дату и время в формате YYYY-MM-DD HH:MM:SS\n')
    data = {
        'greeting': greetings(),
        'cards': get_transactions_total_spent(),
        'top_transactions': get_top_transactions(),
        'currency_conversion': currency_conversion(),
        'currency_rates': stock_prices_api()
    }
    print(data)
