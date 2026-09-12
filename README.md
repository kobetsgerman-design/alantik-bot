# 🤖 Alantik Telegram Bot

Автоматический бот для публикации товаров из Google Sheets в Telegram канал @alantiknw

---

## 📋 Содержимое

- `bot.py` - основной код бота
- `requirements.txt` - зависимости Python
- `.env.example` - пример переменных окружения
- `Procfile` - конфиг для Railway.app

---

## 🚀 Быстрый старт на Railway.app

### Шаг 1: Подготовить данные

✅ **Уже готово! У тебя есть:**
- Telegram токен: `8585986349:AAHz7QkmGEOAviW7M48SVMlnORR4etzGX_c`
- Google Sheets ID: `1DmGoEj4YyB7flwGNSbW7wbhz62F9Pu7ARNkJVQ67LQo`
- Google Cloud credentials (JSON)
- Доступ к каналу @alantiknw

---

### Шаг 2: Загрузить на GitHub

1. Создай новый репозиторий на GitHub (например: `alantik-bot`)
2. Загрузи туда эти файлы:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `.env.example`

**Команды git:**
```bash
git init
git add .
git commit -m "Initial commit: Alantik Telegram Bot"
git branch -M main
git remote add origin https://github.com/ТВОЙ_ЮЗЕР/alantik-bot.git
git push -u origin main
```

---

### Шаг 3: Развернуть на Railway.app

1. Откройи https://railway.app
2. Нажми **"Deploy Now"**
3. Выбери **"GitHub Repo"**
4. Авторизуйся через GitHub
5. Выбери репозиторий `alantik-bot`
6. Нажми **"Deploy"**

---

### Шаг 4: Настроить переменные окружения

⚠️ **ВАЖНО: реальные секреты вводятся ТОЛЬКО здесь, в интерфейсе Railway — никогда не в файлах, которые загружаются на GitHub.**

На Railway.app:

1. Открой свой проект
2. Перейди в **"Variables"**
3. Добавь эти переменные (значения возьми из своих личных заметок — Claude присылал их тебе в чате):

```
TELEGRAM_TOKEN=<токен бота от @BotFather>
CHANNEL_ID=@alantiknw
SHEET_ID=<ID твоей Google таблицы из ссылки>
SHEET_NAME=Таблица1
GCP_CREDENTIALS_JSON=<весь JSON ключ одной строкой>
```

4. Нажми **"Save"**

📌 Файл `.env.example` в репозитории — это ШАБЛОН с пустыми плейсхолдерами. Он специально не содержит реальных данных и безопасен для публичного GitHub.

---

## 🎮 Команды бота

После запуска бот поддерживает эти команды в Telegram:

**`/start`** - проверить что бот работает

**`/post`** - постить все новые товары из Google Sheets в канал @alantiknw

---

## 📝 Как добавлять товары

1. Открой Google Sheets: https://docs.google.com/spreadsheets/d/1DmGoEj4YyB7flwGNSbW7wbhz62F9Pu7ARNkJVQ67LQo/edit

2. Добавь новую строку с данными:
   - **Фото (URL)** - ссылка на фото товара
   - **Название** - название товара
   - **Описание** - описание товара
   - **Цена (RUB)** - цена товара в рублях
   - **Статус** - оставь пусто или напиши "новый"

3. Напиши в Telegram боту `/post`

4. Бот автоматически:
   - ✅ Прочитает новые товары
   - ✅ Постит их в @alantiknw
   - ✅ Обновит статус на "опубликовано"

---

## 🔧 Локальный запуск (для тестирования)

1. Установи Python 3.8+

2. Установи зависимости:
```bash
pip install -r requirements.txt
```

3. Создай `.env` файл из `.env.example`

4. Запусти бота:
```bash
python bot.py
```

---

## 📊 Структура Google Sheets

Твоя таблица должна иметь эти колонки:

| A | B | C | D | E |
|---|---|---|---|---|
| Фото (URL) | Название | Описание | Цена (RUB) | Статус |
| https://... | Стол | Восточный стиль | 45000 | опубликовано |
| https://... | Люстра | Хрусталь | 15000 | новый |

---

## ⚠️ Важно

- **Бот работает 24/7** на Railway.app (бесплатно)
- **Статус автоматически** меняется на "опубликовано" после постинга
- **Не постит товары со статусом "опубликовано"** - они уже были постнуты
- **Логи видны в Railway** → твой проект → "Logs"

---

## 🆘 Помощь

Если что-то не работает:

1. Проверь логи в Railway.app
2. Убедись что все переменные окружения заполнены правильно
3. Проверь что Google Sheets доступна по ссылке
4. Проверь что бот добавлен администратором в @alantiknw

---

**Готово! Бот работает! 🚀**
