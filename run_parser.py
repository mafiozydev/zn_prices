import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        # Консольный режим
        import asyncio
        from parser import scrape_ozon
        print("🚀 Запуск парсера Ozon (Soulway) в консольном режиме...")
        asyncio.run(scrape_ozon(headless=False))
        print("✅ Готово! Данные сохранены в prices.db")
    else:
        # GUI режим (по умолчанию)
        from gui import OzonParserGUI
        import tkinter as tk
        root = tk.Tk()
        app = OzonParserGUI(root)
        root.mainloop()