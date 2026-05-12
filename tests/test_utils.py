import json
from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
import pytest

from src.utils import currency_conversion, get_df_from_file, stock_prices_api


@patch("builtins.open", mock_open)
@patch('pandas.read_excel')
def test_get_df_from_file_open(mock_read):
    fake_df = pd.DataFrame(
        {
            'Номер карты': ['*4542', '*4543'],
            'Валюта': ['RUB', 'USD'],
            'Сумма': [100, 150]
        }
    )
    mock_read.return_value = fake_df
    result = get_df_from_file('test.xlsx')
    assert len(result) == 2
    assert result.equals(fake_df)
    mock_read.assert_called_once_with("test.xlsx")


def test_get_df_from_file_not_found(path='nonexistent_file.xlsx'):
    with pytest.raises(Exception):
        result = get_df_from_file(path)
        assert 'Ошибка открытия файла. Файл не найден' in result


@patch('os.getenv')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'user_stocks': ['AAPL', 'MSFT']}))
@patch('requests.get')
def test_stock_prices_api_success(mock_get, mock_open, mock_getenv):
    mock_getenv.return_value = 'test_api_key'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'Global Quote': {'05. price': '150.00'}
    }
    mock_get.return_value = mock_response
    result = stock_prices_api()
    assert len(result) == 2
    assert result[0]['stock'] == 'AAPL'
    assert result[0]['price'] == '150.00'


@patch('os.getenv')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'user_stocks': ['AAPL']}))
@patch('requests.get')
def test_stock_prices_api_error_status(mock_get, mock_open, mock_getenv):
    mock_getenv.return_value = 'test_api_key'
    mock_response = MagicMock()
    mock_response.status_code = 404  # Ошибка доступа
    mock_get.return_value = mock_response
    result = stock_prices_api()
    assert result == []  # Ожидается пустой список при ошибке


@patch('os.getenv')
@patch('builtins.open', side_effect=FileNotFoundError)
def test_stock_prices_api_file_not_found(mock_open, mock_getenv):
    mock_getenv.return_value = 'test_api_key'
    with pytest.raises(FileNotFoundError):
        stock_prices_api()


@patch('os.getenv')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'user_currencies': ['USD', 'EUR']}))
@patch('requests.get')
def test_currency_conversion_success(mock_get, mock_open, mock_getenv):
    mock_getenv.return_value = 'test_api_key'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'result': '73.21'}
    mock_get.return_value = mock_response
    result = currency_conversion()
    assert len(result) == 2
    assert result[0]['currency'] == 'USD'
    assert result[0]['rate'] == '73.21'


@patch('os.getenv')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'user_currencies': ['USD', 'EUR']}))
@patch('requests.get')
def test_currency_conversion_error_status(mock_get, mock_open, mock_getenv):
    mock_getenv.return_value = 'test_api_key'
    mock_response = MagicMock()
    mock_response.status_code = 404  # Ошибка доступа
    mock_get.return_value = mock_response
    result = currency_conversion()
    assert result == []  # Ожидается пустой список при ошибке


@patch('os.getenv')
@patch('builtins.open', side_effect=FileNotFoundError)
def test_currency_conversion_file_not_found(mock_open, mock_getenv):
    mock_getenv.return_value = 'test_api_key'
    with pytest.raises(FileNotFoundError):
        currency_conversion()
