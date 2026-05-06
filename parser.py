import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup
import re
from config import MAX_PRICE_RUB, BRAND_URLS
from database import save_product, init_db

async def scrape_ozon():
    init_db()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        await stealth_async(context)
        page = await context.new_page()

        for url in BRAND_URLS:
            print(f"🔍 Парсим: {url}")
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(4000)

            content = await page.content()
            soup = BeautifulSoup(content, "lxml")

            products = soup.select('div[data-widget="searchResultsV2"] a[href*="/product/"]')
            if not products:
                products = soup.select('a[href*="/product/"]')

            count = 0
            for link in products[:60]:
                href = link.get("href", "")
                if not href.startswith("http"):
                    href = "https://www.ozon.ru" + href

                title_tag = link.select_one('span, div')
                title = title_tag.get_text(strip=True) if title_tag else "Без названия"

                parent = link.parent
                price_text = ""
                if parent:
                    price_span = parent.select_one('span')
                    if price_span:
                        price_text = price_span.get_text()

                price_match = re.search(r'([\d\s]+)', price_text.replace("₽", ""))
                if price_match:
                    try:
                        price_rub = float(price_match.group(1).replace(" ", ""))
                        if price_rub < MAX_PRICE_RUB:
                            print(f"✅ {title[:55]}... — {price_rub} ₽")
                            save_product(href, title, price_rub)
                            count += 1
                    except:
                        pass

            print(f"📦 Сохранено товаров дешевле {MAX_PRICE_RUB} ₽: {count}")

        await browser.close()