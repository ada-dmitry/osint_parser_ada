# Архитектура проекта

Ниже — схема на уровне компонентов в формате, аналогичном примеру.

```
                 [CLI (main.py / run.fish / run.sh / run_cron.fish)]
                                   |
                                   v
               Fetcher — загрузка HTML и проверка кода ответа
                     [Fetcher: HTTP GET (requests.Session)]
                             (timeout / retries / delay)
                                   |
                                   v
    • Parser      — извлечение таблиц/списков и распознавание колонок (BS4+lxml)
    • Normalizer  — очистка значений, trim, удаление префиксов, приведение типов/дат
    • Model       — маппинг в dataclasses (Auditor, Organization, …)
    • Exporter    — выгрузка pandas.DataFrame в Excel через openpyxl
                                   |
                                   v
[Pipeline]
[Parser (BeautifulSoup + эвристики)] --> [Normalizer] --> [Model] --> [DataFrame] --> [Exporter (XLSX)]
```

## Соответствие компонент файлам

- CLI / запуск:
  - `main.py` — CLI-меню, режим неинтерактивного запуска через аргументы (`--registry`, `--mode`, `--list`).
  - `run.fish`, `run.sh` — быстрый старт; `run_cron.fish` — обёртка для cron (Fish).

- Fetcher:
  - `parsers/base_parser.py` → `BaseParser._make_request()` (requests.Session, заголовок User-Agent, таймаут, задержка, повторные попытки).
  - Пагинация: `BaseParser._get_pagination_urls()`.

- Parser:
  - Специализированные: `parsers/auditors_parser.py`, `parsers/organizations_parser.py`.
  - Универсальный: `parsers/generic_parser.py` (табличные реестры, автоматическое определение заголовков).
  - Общая точка входа: `BaseParser.parse_registry(detailed=...)`.

- Normalizer:
  - Локальные шаги очистки/приведения: обрезка пробелов, извлечение чисел/дат, нормализация полей (внутри парсеров).
  - Приведение к словарям/рубрикам, единообразные ключи для экспорта.

- Model:
  - `models/auditor.py`, `models/organization.py`, и др. — dataclasses, метод `to_dict()` для экспорта.

- DataFrame + Exporter:
  - Формирование `pandas.DataFrame` и экспорт: `utils/excel_exporter.py` → `ExcelExporter.export_to_excel()`.
  - Форматирование XLSX (ширина колонок, шапка, стили): `ExcelExporter._format_excel()`.

- Конфигурация и логирование:
  - `config.py` — URL реестров (`REGISTRIES`), сетевые и экспортные настройки (`PARSER_CONFIG`, `EXPORT_CONFIG`, `LOGGING_CONFIG`).
  - `utils/logger.py` — консольный и файловый логгеры (`logs/parser_YYYY-MM-DD.log`).

## Потоки выполнения

- Режим запуска:
  - Интерактивный CLI: выбор реестра и детализации из меню (`main.py`).
  - Неинтерактивный (для cron): `python main.py --registry <key> --mode <quick|full>`.

- Детализация:
  - `mode=quick` — первая страница (без обхода пагинации и детальных карточек).
  - `mode=full` — все страницы (пагинация) и, при поддержке, парсинг детальных карточек записей.

- Надёжность:
  - Повторные попытки при ошибках сети, управляемая задержка между запросами.
  - Логи INFO/DEBUG в консоль и файл.

- Выходные данные:
  - Сырые записи → нормализованные словари → модели (dataclasses) → `pandas.DataFrame` → XLSX в `data/exports/`.
