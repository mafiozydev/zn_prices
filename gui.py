import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import asyncio
from parser import scrape_ozon
from config import MAX_PRICE_USD

class OzonParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ozon Soulway Parser • by Grok")
        self.root.geometry("720x520")
        self.root.resizable(False, False)

        # Верхняя панель настроек
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="Max price (USD):").pack(side="left")
        self.price_var = tk.StringVar(value=str(MAX_PRICE_USD))
        ttk.Entry(top_frame, textvariable=self.price_var, width=8).pack(side="left", padx=5)

        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(top_frame, text="Headless (без окна браузера)", variable=self.headless_var).pack(side="left", padx=15)

        # Кнопка запуска
        self.run_btn = ttk.Button(top_frame, text="▶ Запустить парсер", command=self.start_parsing)
        self.run_btn.pack(side="right")

        # Логи
        log_frame = ttk.LabelFrame(root, text="Логи", padding=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=18, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True)

        # Нижняя панель
        bottom_frame = ttk.Frame(root, padding=10)
        bottom_frame.pack(fill="x")

        self.status_label = ttk.Label(bottom_frame, text="Готов к работе")
        self.status_label.pack(side="left")

        ttk.Button(bottom_frame, text="Открыть prices.db", command=self.open_db).pack(side="right")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_parsing(self):
        self.run_btn.config(state="disabled")
        self.log_text.delete("1.0", tk.END)
        self.status_label.config(text="Работает...")

        def run_async():
            try:
                # Обновляем MAX_PRICE_USD из поля
                import config
                config.MAX_PRICE_RUB = float(self.price_var.get()) * 80

                headless = self.headless_var.get()
                self.log("🚀 Запуск парсера...")

                # Запускаем асинхронный парсер
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                count = loop.run_until_complete(
                    scrape_ozon(headless=headless, progress_callback=self.log)
                )
                loop.close()

                self.log(f"\n✅ Готово! Сохранено товаров: {count}")
                self.status_label.config(text=f"Готово — {count} товаров")
            except Exception as e:
                self.log(f"❌ Ошибка: {str(e)}")
            finally:
                self.run_btn.config(state="normal")

        threading.Thread(target=run_async, daemon=True).start()

    def open_db(self):
        import os
        import subprocess
        db_path = os.path.abspath("prices.db")
        if os.path.exists(db_path):
            subprocess.Popen(["explorer", db_path])
        else:
            self.log("❌ prices.db ещё не создан")

if __name__ == "__main__":
    root = tk.Tk()
    app = OzonParserGUI(root)
    root.mainloop()