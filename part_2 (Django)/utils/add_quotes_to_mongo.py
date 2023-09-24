import json
import os
from pymongo import MongoClient

# Отримати шлях до поточної директорії скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

client = MongoClient("mongodb://localhost")
db = client.hw

# Шлях до файлу з інформацією про авторів
authors_file_path = os.path.join(script_dir, 'authors.json')

# Завантаження даних про авторів
with open(authors_file_path, 'r', encoding='utf-8') as authors_fd:
    authors_data = json.load(authors_fd)

# Вставка даних про авторів в базу даних
for author in authors_data:
    db.authors.insert_one(author)

# Шлях до файлу з цитатами
quotes_file_path = os.path.join(script_dir, 'quotes.json')

# Завантаження даних про цитати
with open(quotes_file_path, 'r', encoding='utf-8') as quotes_fd:
    quotes_data = json.load(quotes_fd)

# Вставка даних про цитати в базу даних
for quote in quotes_data:
    author = db.authors.find_one({'fullname': quote['author']})
    if author:
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tags': quote['tags'],
            # Використовуйте _id автора з колекції authors
            'author_id': author['_id']
        })
    else:
        print("Author not found for:", quote['author'])

client.close()
