# Nutrition Tracker

Клиент-серверное приложение для мониторинга и анализа
энергетической ценности рациона питания.

## Стек
- Сервер: Python, FastAPI, SQLAlchemy, SQLite
- Клиент: Python, PyQt6
- Тестирование: pytest

## Установка
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m server.seed_data
