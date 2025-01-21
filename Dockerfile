# Используем текущий образ
FROM mcr.microsoft.com/playwright/python:v1.37.0

# Устанавливаем Xvfb для виртуальной графической среды
RUN apt-get update && apt-get install -y xvfb

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем системные зависимости для Playwright
RUN playwright install-deps

# Устанавливаем Playwright-браузеры
RUN playwright install

# Указываем команду для запуска приложения
CMD ["sh", "-c", "xvfb-run -a uvicorn app:app --host 0.0.0.0 --port $PORT"]
