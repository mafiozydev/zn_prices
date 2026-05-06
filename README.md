# Ozon Price Tracker (zn_prices)

Парсер цен на БАДы, спортпит и продукцию **Soulway** с Ozon.ru.

### Основные возможности
- Парсинг цен на продукцию Soulway и другие БАДы/спортпит
- Хранение истории цен в SQLite
- Фильтр по максимальной цене (по умолчанию ≤ 50 USD)
- Запуск 2 раза в день

## Установка

1. `git clone https://github.com/mafiozydev/zn_prices.git`
2. `cd zn_prices`
3. `pip install -r requirements.txt`
4. Скопировать `.env.example` → `.env`
5. `python run_parser.py`

## Настройка
Отредактируй `config.py`:
- Список брендов/поисковых запросов
- `MAX_PRICE_USD = 50`

**Внимание**: Парсинг нарушает ToS Ozon. Используй только для личных целей.