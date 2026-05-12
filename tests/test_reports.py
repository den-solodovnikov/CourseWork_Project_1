import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    df = pd.DataFrame(columns=['Дата операции', 'Категория'])
    assert spending_by_category(df, 'Перевод').empty
    df = pd.DataFrame(
        {
            'Дата операции': ['08.05.2026', '05.06.2020'],
            'Категория': ['Перевод', 'Супермаркет']
        }
    )
    assert len(spending_by_category(df, 'Супермаркет', '05.06.2020')) == 1
