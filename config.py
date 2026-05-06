import os
from dotenv import load_dotenv

load_dotenv()

MAX_PRICE_USD = float(os.getenv("MAX_PRICE_USD", 50))
MAX_PRICE_RUB = MAX_PRICE_USD * 80  # примерный курс

BRAND_URLS = [
    "https://www.ozon.ru/brand/soul-way-100918703/",
]

SEARCH_QUERIES = [
    "soulway",
    "soulway протеин",
    "soulway bcaa",
]