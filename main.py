#!/usr/bin/env python3
"""
Парсер реестров СРО ААС (Саморегулируемая организация аудиторов)

Автор: [ada]
"""

import sys
import os
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
    """Главная функция приложения"""
    print_banner()

    # Маппинг выбора на реестры
    registry_map = {
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
