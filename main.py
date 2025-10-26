#!/usr/bin/env python3
"""
Парсер реестров СРО ААС (Саморегулируемая организация аудиторов)

Автор: [ada]

Использование:
    Интерактивный режим:
        python main.py

    Режим cron (автоматический):
        python main.py --registry auditors --mode quick
        python main.py --registry organizations --mode full
        python main.py -r certificates -m quick
        python main.py --list  # Показать доступные реестры
"""

import sys
import os
import argparse
from datetime import datetime

from config import REGISTRIES
from parsers.organizations_parser import OrganizationsParser
from parsers.auditors_parser import AuditorsParser
from parsers.generic_parser import GenericRegistryParser
from utils.excel_exporter import ExcelExporter
from utils.logger import setup_logger


def print_banner():
    """Вывод баннера приложения"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║          ПАРСЕР РЕЕСТРОВ СРО ААС                          ║
    ║   Саморегулируемая организация аудиторов                 ║
    ║              Ассоциация «Содружество»                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_registry_map():
    """Получить маппинг реестров"""
    return {
        "1": ("auditors", "Реестр аудиторов и индивидуальных аудиторов"),
        "2": ("organizations", "Реестр аудиторских организаций"),
        "3": ("certificates", "Реестр квалификационных аттестатов"),
        "4": ("individual_auditors", "Перечень индивидуальных аудиторов"),
        "5": ("training_centers", "Реестр учебно-методических центров"),
        "6": ("oppk_confirmation", "Сведения о подтверждении ОППК"),
        "7": ("ozo_training", "Сведения о прохождении ПК руководителем"),
        "8": ("excluded_auditors", "Реестр исключенных аудиторов"),
        "9": ("excluded_organizations", "Реестр исключенных организаций"),
        "10": ("cancelled_certificates", "Реестр аннулированных аттестатов"),
        "11": ("excluded_training_centers", "УМЦ исключенные из реестра"),
        "12": ("disciplinary_auditors", "Дисциплинарные меры к аудиторам"),
        "13": ("disciplinary_organizations", "Дисциплинарные меры к организациям"),
        "14": ("audit_networks", "Перечень сетей аудиторских организаций"),
    }


def list_registries():
    """Вывести список доступных реестров"""
    print("\n" + "=" * 60)
    print("ДОСТУПНЫЕ РЕЕСТРЫ ДЛЯ --registry ПАРАМЕТРА:")
    print("=" * 60)

    registry_map = get_registry_map()

    print("\n📋 ДЕЙСТВИТЕЛЬНЫЕ ЧЛЕНЫ:")
    print("  auditors                  - Реестр аудиторов")
    print("  organizations             - Реестр организаций")
    print("  certificates              - Квалификационные аттестаты")
    print("  individual_auditors       - Индивидуальные аудиторы")
    print("  training_centers          - Учебно-методические центры")
    print("  oppk_confirmation         - Подтверждение ОППК")
    print("  ozo_training              - Прохождение ПК руководителем")

    print("\n❌ ИСКЛЮЧЕННЫЕ ЧЛЕНЫ:")
    print("  excluded_auditors         - Исключенные аудиторы")
    print("  excluded_organizations    - Исключенные организации")
    print("  cancelled_certificates    - Аннулированные аттестаты")
    print("  excluded_training_centers - Исключенные УМЦ")

    print("\n⚠️  ДИСЦИПЛИНАРНЫЕ МЕРЫ:")
    print("  disciplinary_auditors     - Меры к аудиторам")
    print("  disciplinary_organizations - Меры к организациям")

    print("\n🌐 СЕТИ:")
    print("  audit_networks            - Сети организаций")

    print("\n" + "=" * 60)
    print("Режимы (--mode):")
    print("  quick - Быстрый (первая страница)")
    print("  full  - Полный (все страницы)")
    print("=" * 60)
    print("\nПример:")
    print("  python main.py --registry auditors --mode quick")
    print("  python main.py -r organizations -m full\n")


def print_menu():
    """Вывод главного меню"""
    print("\n" + "=" * 60)
    print("ДОСТУПНЫЕ РЕЕСТРЫ:")
    print("=" * 60)

    print("\n📋 ДЕЙСТВИТЕЛЬНЫЕ ЧЛЕНЫ И ВЫДАННЫЕ АТТЕСТАТЫ:")
    print("  1. Реестр членов — аудиторов и индивидуальных аудиторов ⭐")
    print("  2. Реестр членов — аудиторских организаций ⭐")
    print("  3. Реестр выданных СРО ААС квалификационных аттестатов ⭐")
    print("  4. Перечень индивидуальных аудиторов ⭐")
    print("  5. Реестр учебно-методических центров ⭐")
    print("  6. Сведения о подтверждении ОППК аудиторами ⭐")
    print("  7. Сведения о прохождении ПК руководителем аудита ОЗО ФР ⭐")

    print("\n❌ ИСКЛЮЧЕННЫЕ ЧЛЕНЫ И АННУЛИРОВАННЫЕ АТТЕСТАТЫ:")
    print("  8. Реестр аудиторов, прекративших членство в СРО ААС ⭐")
    print("  9. Реестр аудиторских организаций, прекративших членство ⭐")
    print(" 10. Реестр аннулированных квалификационных аттестатов ⭐")
    print(" 11. УМЦ, исключенные из реестра СРО ААС ⭐")

    print("\n⚠️  ДИСЦИПЛИНАРНЫЕ МЕРЫ:")
    print(" 12. Меры дисциплинарного воздействия к аудиторам ⭐")
    print(" 13. Меры дисциплинарного воздействия к организациям ⭐")

    print("\n🌐 СЕТИ АУДИТОРСКИХ ОРГАНИЗАЦИЙ:")
    print(" 14. Перечень российских и международных сетей ⭐")

    print("\n" + "=" * 60)
    print("  0. Выход")
    print("=" * 60)
    print("\n⭐ - Полностью реализованный парсер")


def parse_organizations(detailed=False):
    """
    Парсинг реестра аудиторских организаций

    Args:
        detailed: Парсить ли детальные страницы
    """
    logger = setup_logger("main")

    print("\n" + "=" * 60)
    print("ПАРСИНГ РЕЕСТРА АУДИТОРСКИХ ОРГАНИЗАЦИЙ")
    print("=" * 60)

    # Подтверждение пользователя
    if detailed:
        print("\n⚠️  ВНИМАНИЕ: Детальный парсинг может занять продолжительное время!")
        choice = input("Продолжить? (y/n): ").lower()
        if choice != "y":
            print("Операция отменена.")
            return

    try:
        # Создание парсера
        parser = OrganizationsParser()

        # Парсинг данных
        print("\n🔄 Начало парсинга...")
        organizations = parser.parse_to_objects(detailed=detailed)

        if not organizations:
            print("\n❌ Не удалось получить данные из реестра.")
            return

        print(f"\n✅ Успешно собрано записей: {len(organizations)}")

        # Экспорт в Excel
        print("\n📊 Экспорт данных в Excel...")
        exporter = ExcelExporter()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"organizations_{timestamp}"

        filepath = exporter.export_organizations(organizations, filename=filename)

        if filepath:
            print(f"\n✅ Данные успешно экспортированы!")
            print(f"📁 Файл: {os.path.abspath(filepath)}")
            print(f"📊 Количество записей: {len(organizations)}")
        else:
            print("\n❌ Ошибка при экспорте данных.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Операция прервана пользователем.")
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}")
        print(f"\n❌ Произошла ошибка: {e}")


def parse_generic_registry(registry_key: str, registry_name: str, detailed=False):
    """
    Универсальная функция парсинга любого реестра

    Args:
        registry_key: Ключ реестра из config.REGISTRIES
        registry_name: Название реестра для отображения
        detailed: Парсить ли детальные страницы
    """
    logger = setup_logger("main")

    print("\n" + "=" * 60)
    print(f"ПАРСИНГ: {registry_name.upper()}")
    print("=" * 60)

    # Подтверждение пользователя
    if detailed:
        print("\n⚠️  ВНИМАНИЕ: Детальный парсинг может занять продолжительное время!")
        choice = input("Продолжить? (y/n): ").lower()
        if choice != "y":
            print("Операция отменена.")
            return

    try:
        # Создание парсера
        parser = GenericRegistryParser(registry_key)

        # Парсинг данных
        print("\n🔄 Начало парсинга...")
        data = parser.parse_registry(detailed=detailed)

        if not data:
            print("\n❌ Не удалось получить данные из реестра.")
            return

        print(f"\n✅ Успешно собрано записей: {len(data)}")

        # Экспорт в Excel
        print("\n📊 Экспорт данных в Excel...")
        exporter = ExcelExporter()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{registry_key}_{timestamp}"

        filepath = exporter.export_to_excel(
            data=data,
            filename=filename,
            sheet_name=registry_name[:30],  # Ограничение длины для Excel
        )

        if filepath:
            print(f"\n✅ Данные успешно экспортированы!")
            print(f"📁 Файл: {os.path.abspath(filepath)}")
            print(f"📊 Количество записей: {len(data)}")
        else:
            print("\n❌ Ошибка при экспорте данных.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Операция прервана пользователем.")
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}")
        print(f"\n❌ Произошла ошибка: {e}")


def parse_auditors(detailed=False):
    """Парсинг реестра аудиторов"""
    logger = setup_logger("main")

    print("\n" + "=" * 60)
    print("ПАРСИНГ РЕЕСТРА АУДИТОРОВ")
    print("=" * 60)

    if detailed:
        print("\n⚠️  ВНИМАНИЕ: Детальный парсинг может занять продолжительное время!")
        choice = input("Продолжить? (y/n): ").lower()
        if choice != "y":
            print("Операция отменена.")
            return

    try:
        parser = AuditorsParser()
        print("\n🔄 Начало парсинга...")
        auditors = parser.parse_to_objects(detailed=detailed)

        if not auditors:
            print("\n❌ Не удалось получить данные из реестра.")
            return

        print(f"\n✅ Успешно собрано записей: {len(auditors)}")

        # Экспорт в Excel
        print("\n📊 Экспорт данных в Excel...")
        exporter = ExcelExporter()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"auditors_{timestamp}"

        # Преобразуем в словари
        data = [auditor.to_dict() for auditor in auditors]
        filepath = exporter.export_to_excel(
            data=data, filename=filename, sheet_name="Аудиторы"
        )

        if filepath:
            print(f"\n✅ Данные успешно экспортированы!")
            print(f"📁 Файл: {os.path.abspath(filepath)}")
            print(f"📊 Количество записей: {len(auditors)}")
        else:
            print("\n❌ Ошибка при экспорте данных.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Операция прервана пользователем.")
    except Exception as e:
        logger.error(f"Ошибка при парсинге: {e}")
        print(f"\n❌ Произошла ошибка: {e}")


def not_implemented():
    """Заглушка для нереализованных функций"""
    print("\n⚠️  Данный парсер находится в разработке.")
    print("💡 Вы можете реализовать его по аналогии с OrganizationsParser.")


def main():
    """Главная функция - интерактивный режим"""
    print_banner()

    # Маппинг выбора на реестры
    registry_map = get_registry_map()

    while True:
        print_menu()

        choice = input("\n👉 Выберите реестр (0-14): ").strip()

        if choice == "0":
            print("\n👋 До свидания!")
            sys.exit(0)

        elif choice == "1":
            # Реестр аудиторов - специализированный парсер
            print(f"\n📋 Выбран: {registry_map[choice][1]}")
            detail_choice = input("Парсить детальные страницы? (y/n): ").lower()
            detailed = detail_choice == "y"
            parse_auditors(detailed=detailed)

        elif choice == "2":
            # Реестр аудиторских организаций - специализированный парсер
            print(f"\n📋 Выбран: {registry_map[choice][1]}")
            detail_choice = input("Парсить детальные страницы? (y/n): ").lower()
            detailed = detail_choice == "y"
            parse_organizations(detailed=detailed)

        elif choice in registry_map:
            # Все остальные реестры - универсальный парсер
            registry_key, registry_name = registry_map[choice]
            print(f"\n📋 Выбран: {registry_name}")
            detail_choice = input("Парсить детальные страницы? (y/n): ").lower()
            detailed = detail_choice == "y"
            parse_generic_registry(registry_key, registry_name, detailed=detailed)

        else:
            print("\n❌ Неверный выбор. Попробуйте снова.")

        # Пауза перед возвратом в меню
        input("\n⏸️  Нажмите Enter для возврата в меню...")


def run_cron_mode(registry_key: str, mode: str):
    """
    Запуск в режиме cron (неинтерактивный)

    Args:
        registry_key: Ключ реестра (auditors, organizations, и т.д.)
        mode: Режим парсинга (quick или full)
    """
    logger = setup_logger("cron")

    # Проверка валидности реестра
    if registry_key not in REGISTRIES:
        logger.error(f"Неизвестный реестр: {registry_key}")
        print(f"❌ Ошибка: Реестр '{registry_key}' не найден.")
        print("Используйте --list для просмотра доступных реестров.")
        sys.exit(1)

    # Определение режима детализации
    detailed = mode.lower() == "full"
    mode_str = "полный" if detailed else "быстрый"

    registry_name = REGISTRIES[registry_key]["name"]

    logger.info(f"Запуск в режиме cron: {registry_key} ({mode_str})")
    print(f"\n🤖 РЕЖИМ CRON")
    print("=" * 60)
    print(f"Реестр: {registry_name}")
    print(f"Режим: {mode_str}")
    print(f"Детализация: {'Да' if detailed else 'Нет'}")
    print("=" * 60 + "\n")

    try:
        # Выбор парсера в зависимости от реестра
        if registry_key == "auditors":
            parse_auditors(detailed=detailed)
        elif registry_key == "organizations":
            parse_organizations(detailed=detailed)
        else:
            parse_generic_registry(registry_key, registry_name, detailed=detailed)

        logger.info(f"Парсинг {registry_key} успешно завершен")
        print("\n✅ Парсинг успешно завершен")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Ошибка при парсинге в режиме cron: {e}")
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)


def parse_args():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Парсер реестров СРО ААС",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Интерактивный режим
  python main.py

  # Режим cron - быстрый парсинг аудиторов
  python main.py --registry auditors --mode quick

  # Режим cron - полный парсинг организаций
  python main.py --registry organizations --mode full

  # Список доступных реестров
  python main.py --list
        """,
    )

    parser.add_argument(
        "-r", "--registry", type=str, help="Ключ реестра для парсинга (см. --list)"
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["quick", "full"],
        default="quick",
        help="Режим парсинга: quick (быстрый) или full (полный)",
    )

    parser.add_argument(
        "-l", "--list", action="store_true", help="Показать список доступных реестров"
    )

    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_args()

        # Режим показа списка реестров
        if args.list:
            list_registries()
            sys.exit(0)

        # Режим cron (неинтерактивный)
        if args.registry:
            run_cron_mode(args.registry, args.mode)

        # Интерактивный режим (по умолчанию)
        else:
            main()

    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
