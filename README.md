# 📋 Парсер реестров СРО ААС

Это Python-приложение для автоматизированного сбора данных из 14 официальных реестров **Саморегулируемой организации аудиторов Ассоциация «Содружество»** (СРО ААС). Проект реализует веб-скрейпинг с поддержкой пагинации, обработкой ошибок и экспортом в Excel.

## 🎯 Основные возможности

- **14 реестров** — полное покрытие всех публичных реестров СРО ААС
- **Два режима парсинга:**
  - 🚀 **Быстрый** (первая страница, ~50 записей, 1-2 сек)
  - 🔍 **Полный** (все страницы с пагинацией, тысячи записей, несколько минут)
- **Экспорт в Excel** — автоматическое форматирование, заголовки, стилизация
- **Логирование** — подробные логи всех операций в `logs/`
- **Обработка ошибок** — повторные попытки (3x) при сбоях сети
- **CLI-интерфейс** — интерактивное меню для выбора реестра
- **Режим Cron** — автоматизация парсинга через аргументы командной строки
- **Неинтерактивный режим** — для запуска по расписанию без пользовательского ввода

## 📊 Поддерживаемые реестры

**Действующие члены (7 реестров):**
1. Реестр аудиторов и индивидуальных аудиторов (14,691+ записей)
2. Реестр аудиторских организаций (256+ записей)
3. Квалификационные аттестаты
4. Индивидуальные аудиторы
5. Учебно-методические центры
6. Подтверждение ОППК
7. Прохождение ПК руководителем аудита ОЗО ФР

**Исключенные члены (4 реестра):**
8. Аудиторы, прекратившие членство
9. Аудиторские организации, прекратившие членство
10. Аннулированные аттестаты
11. Исключенные УМЦ

**Дисциплинарные меры (2 реестра):**
12. Меры воздействия к аудиторам
13. Меры воздействия к организациям

**Сети (1 реестр):**
14. Российские и международные сети аудиторских организаций

## 🚀 Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/ada-dmitry/osint_parser_ada.git
cd osint_parser_ada

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### Запуск

**Интерактивный режим:**
```bash
python main.py
# Выбор реестра из меню → выбор режима (y/n)
```

**Через скрипт (Fish Shell):**
```bash
./run.fish
```

### Режим командной строки (для Cron)

**Просмотр доступных реестров:**
```bash
python main.py --list
```

**Запуск парсинга без интерактивного режима:**
```bash
# Быстрый парсинг аудиторов
python main.py --registry auditors --mode quick

# Полный парсинг организаций
python main.py --registry organizations --mode full

# Сокращенный синтаксис
python main.py -r certificates -m quick
```

**Доступные реестры для --registry:**
- `auditors`, `organizations`, `certificates`
- `individual_auditors`, `training_centers`, `oppk_confirmation`, `ozo_training`
- `excluded_auditors`, `excluded_organizations`, `cancelled_certificates`, `excluded_training_centers`
- `disciplinary_auditors`, `disciplinary_organizations`
- `audit_networks`

**Режимы (--mode):**
- `quick` — быстрый (первая страница, ~50 записей)
- `full` — полный (все страницы)

### Автоматизация с Cron

Примеры cron записей находятся в файле `cron_examples.sh`.

**Настройка автоматического парсинга:**

```bash
# Открыть редактор cron
crontab -e

# Добавить задачу (парсинг аудиторов каждый день в 02:00)
0 2 * * * cd /path/to/osint_parser_ada && venv/bin/python main.py --registry auditors --mode quick >> logs/cron_auditors.log 2>&1

# Полный парсинг организаций каждое воскресенье в 01:00
0 1 * * 0 cd /path/to/osint_parser_ada && venv/bin/python main.py --registry organizations --mode full >> logs/cron_organizations_full.log 2>&1
```

**Просмотр логов:**
```bash
tail -f logs/cron_auditors.log
```

📖 **Подробное руководство:** См. [CRON_GUIDE.md](CRON_GUIDE.md) для детальных инструкций по настройке автоматизации.

### Использование

**Выбор режима парсинга:**
- `n` (No) — быстрое сканирование (только первая страница, ~50 записей, 1-2 сек)
- `y` (Yes) — полное сканирование (все страницы, все записи, несколько минут)

**Программный режим:**

```python
from parsers.auditors_parser import AuditorsParser
from utils.excel_exporter import ExcelExporter

# Быстрое сканирование
parser = AuditorsParser()
data = parser.parse_registry(detailed=False)  # Только первая страница

# Полное сканирование
data = parser.parse_registry(detailed=True)   # Все страницы

# Экспорт в Excel
exporter = ExcelExporter()
exporter.export_to_excel(data, "auditors", "output.xlsx")
```

## 🏗️ Архитектура проекта

```
osint_parser_ada/
├── config.py              # Конфигурация и URL реестров
├── main.py                # CLI-интерфейс с поддержкой Cron
├── run.fish / run.sh      # Скрипты быстрого запуска
├── run_cron.fish          # Скрипт для Cron (Fish Shell)
├── cron_examples.sh       # Примеры Cron записей
├── CRON_GUIDE.md          # Подробное руководство по Cron
├── parsers/               # Парсеры реестров
│   ├── base_parser.py     # Базовый класс с пагинацией
│   ├── auditors_parser.py # Парсер аудиторов
│   ├── organizations_parser.py
│   └── generic_parser.py  # Универсальный парсер
├── models/                # Модели данных
│   ├── organization.py
│   ├── auditor.py
│   └── ...
├── utils/                 # Утилиты
│   ├── logger.py          # Логирование
│   └── excel_exporter.py  # Экспорт в Excel
└── data/exports/          # Экспортированные файлы

```

## Технические характеристики

- **Python:** 3.8+
- **Зависимости:** requests, beautifulsoup4, lxml, pandas, openpyxl
- **Архитектура:** Паттерн Template Method, модульная структура
- **Режимы работы:** Интерактивный CLI и неинтерактивный (Cron)
- **Обработка ошибок:** Повторные попытки (3x), логирование всех операций
- **Производительность:** ~1.5 сек/страница с задержками для защиты от блокировки

## Конфигурация

Основные настройки в `config.py`:

```python
PARSER_CONFIG = {
    "user_agent": "Mozilla/5.0...",
    "timeout": 30,              # Таймаут запроса (сек)
    "delay_between_requests": 1, # Задержка между запросами (сек)
    "max_retries": 3            # Максимум повторных попыток
}
```

## Логирование

Логи сохраняются в `logs/parser_YYYY-MM-DD.log`:
- INFO: Прогресс парсинга, количество найденных записей
- WARNING: Пропущенные страницы, проблемы с данными
- ERROR: Критические ошибки запросов

---

**Источник данных:** [https://sroaas.ru](https://sroaas.ru)
