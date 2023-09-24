# Використовуємо базовий образ Python 3.9
FROM python:3.9

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Створюємо та встановлюємо директорію для коду додатку
RUN mkdir /app
WORKDIR /app

# Копіюємо та встановлюємо залежності Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли з поточної директорії (де знаходиться Dockerfile) в контейнер
COPY . /app/
