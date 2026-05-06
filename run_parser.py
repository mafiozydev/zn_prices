import asyncio
from parser import scrape_ozon

if __name__ == "__main__":
    print("🚀 Запуск парсера Ozon (Soulway)...")
    asyncio.run(scrape_ozon())
    print("✅ Готово! Данные сохранены в prices.db")