# zn_prices

**Ozon Price Tracker** — парсер цен на бренд Soulway (+ другие запросы).

## Установка

```bash
git clone https://github.com/mafiozydev/zn_prices.git
cd zn_prices
python -m venv venv
venv\Scripts\activate   # для Windows
pip install -r requirements.txt
playwright install chromium
```

## Запуск (GUI — рекомендуется)

```bash
python run_parser.py
```

Откроется красивое окно с кнопкой Запустить, настройкой цены и логами.

### Консольный режим (headful)

```bash
python run_parser.py --console
```

## Настройки

В `config.py`:
- `MAX_PRICE_USD = 50` — максимальная цена в долларах

В GUI можно менять цену прямо в окне.

## База данных

`prices.db` (SQLite) — история цен.