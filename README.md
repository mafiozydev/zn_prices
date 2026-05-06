# zn_prices

**Ozon Price Tracker** — парсер цен на бренд Soulway (+другие запросы).

## Установка

```bash
git clone https://github.com/mafiozydev/zn_prices.git
cd zn_prices
python -m venv venv
venv\Scripts\activate   # для Windows
pip install -r requirements.txt
playwright install chromium
```

## Запуск

```bash
python run_parser.py
```

## Настройки (config.py)
- `MAX_PRICE_USD = 50` — макс. цена в долларах
- Парсится бренд https://www.ozon.ru/brand/soul-way-100918703/

## База данных

`prices.db` (SQLite) — история цен, названия, ссылки.