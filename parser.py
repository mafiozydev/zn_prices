import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup
import re
from config import MAX_PRICE_RUB
from database import save_product, init_db

async def scrape_ozon(headless: bool = False, progress_callback=None):
    init_db()
    saved_count = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        await stealth_async(context)
        page = await context.new_page()

        # Идём на ozon.com и ищем "soulway"
        msg = "🌍 Идём на ozon.com и ищем Soulway..."
        print(msg)
        if progress_callback: progress_callback(msg)

        await page.goto("https://www.ozon.com/", wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2500)

        # Поиск на английской версии ozon.com
        search_input = page.locator('input[placeholder*="Search"], input[placeholder*="What are you looking"]').first
        await search_input.click()
        await search_input.fill("soulway")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(6000)

        # Прокручиваем результаты
        for _ in range(5):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2800)

        content = await page.content()
        soup = BeautifulSoup(content, "lxml")

        # Селекторы для ozon.com
        products = soup.select('div[data-widget="searchResultsV2"] a[href*="/product/"]')
        if not products:
            products = soup.select('a[href*="/product/"][class*="tile"]')
        if not products:
            products = soup.select('article a[href*="/product/"]')

        for link in products[:150]:
            href = link.get("href", "")
            if not href.startswith("http"):
                href = "https://www.ozon.com" + href

            title = ""
            title_tag = link.select_one('span, div, h3, h4')
            if title_tag:
                title = title_tag.get_text(strip=True)

            price = None
            parent = link.find_parent()
            if parent:
                price_text = parent.get_text()
                # Ищем цену в USD или другой валюте
                price_match = re.search(r'([\d\s]{2,})\s*[$₽€]', price_text)
                if price_match:
                    try:
                        price = float(price_match.group(1).replace(" ", ""))
                    except:
                        pass

            if price and price < MAX_PRICE_RUB and len(title) > 8:
                msg = f"✅ {title[:55]}... — {price} ₽/USD"
                print(msg)
                if progress_callback: progress_callback(msg)
                save_product(href, title, price)
                saved_count += 1

        msg = f"📦 Сохранено товаров дешевле {MAX_PRICE_RUB} ₽: {saved_count}"
        print(msg)
        if progress_callback: progress_callback(msg)

        await browser.close()
    return saved_count