from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright
import time

# Создаем экземпляр FastAPI
app = FastAPI()

# Основная функция для автоматизации отправки SMS
def automate_sms_with_interaction(phone_number):
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=False)  # Используем headless режим
        context = browser.new_context()
        page = context.new_page()

        try:
            # Переходим на страницу
            url_form = "https://sravni.id/signin/phone"
            page.goto(url_form)
            page.wait_for_load_state("networkidle")
            print("Конечный URL:", page.url)

            # Извлекаем токен
            csrf_token = page.locator("input[name='__RequestVerificationToken']").get_attribute("value")
            print("Найден токен:", csrf_token)

            # Заполняем номер телефона
            phone_input = page.locator("input#textInput-1")  # Выбираем поле ввода по ID
            phone_input.click()  # Фокусируемся на поле
            phone_input.fill("")  # Очищаем поле
            phone_input.type(phone_number, delay=100)  # Вводим текст с задержкой для эмуляции пользователя

            # Нажимаем кнопку "Войти"
            submit_button = page.locator("button[data-qa='Button'][type='submit']:has-text('Войти')")
            submit_button.hover()  # Перемещение мыши на кнопку (имитация пользователя)
            time.sleep(1)  # Пауза в 1 секунду
            submit_button.click()

            # Ждем загрузки страницы с вводом кода
            page.wait_for_selector("input[name='code']", timeout=10000)  # Ожидаем поле ввода кода
            print("СМС успешно отправлено! Страница с вводом кода загружена.")

        except Exception as e:
            print("Произошла ошибка:", e)
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            browser.close()

# Создаем API-эндпоинт для отправки SMS
@app.post("/send_sms")
def send_sms(phone_number: str):
    """
    Эндпоинт для отправки SMS.
    Принимает номер телефона как параметр.
    """
    try:
        automate_sms_with_interaction(phone_number)
        return {"status": "success", "message": f"СМС успешно отправлено на {phone_number}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
