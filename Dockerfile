# Используем Playwright 1.49.1 с Ubuntu Jammy
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Playwright-браузеры
RUN playwright install

# Указываем команду для запуска приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
