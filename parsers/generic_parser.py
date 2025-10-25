"""
Универсальный парсер для реестров с табличной структурой
"""

from typing import List, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parsers.base_parser import BaseParser
from config import BASE_URL


class GenericRegistryParser(BaseParser):
    """
    Универсальный парсер для реестров с простой табличной структурой
    Может использоваться для реестров, где не требуется специальная обработка
    """

    def __init__(self, registry_key: str):
        """
        Args:
            registry_key: Ключ реестра из config.REGISTRIES
        """
        from config import REGISTRIES

        registry = REGISTRIES[registry_key]
        super().__init__(registry["url"], registry["name"])
        self.registry_key = registry_key

    def parse_list_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Универсальный парсинг таблицы
        """
        items = []

        table = soup.find("table")
        if not table:
            self.logger.warning("Таблица с данными не найдена")
            return items

        # Получаем заголовки
        headers = []
        header_row = table.find("tr")
        if header_row:
            headers = [
                th.get_text(strip=True) for th in header_row.find_all(["th", "td"])
            ]

        # Парсим строки
        rows = table.find_all("tr")[1:]

        for row in rows:
            try:
                cols = row.find_all("td")
                if not cols:
                    continue

                item_data = {}

                # Сопоставляем колонки с заголовками
                for i, col in enumerate(cols):
                    header_name = headers[i] if i < len(headers) else f"col_{i}"
                    item_data[header_name] = col.get_text(strip=True)

                # Ищем ссылку на детальную страницу
                link = row.find("a")
                if link:
                    href = link.get("href")
                    # Проверяем, что href - строка, а не список
                    if isinstance(href, list):
                        href = href[0] if href else None
                    if href and isinstance(href, str):
                        item_data["detail_url"] = urljoin(BASE_URL, href)

                items.append(item_data)

            except Exception as e:
                self.logger.error(f"Ошибка при парсинге строки: {e}")
                continue

        return items

    def parse_detail_page(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Универсальный парсинг детальной страницы
        """
        detail_data = {}

        try:
            # Ищем все блоки с информацией
            info_blocks = soup.find_all(
                ["div", "table"], class_=["info-block", "detail-info", "info"]
            )

            for block in info_blocks:
                # Пробуем различные варианты структуры

                # Вариант 1: dt/dd
                labels = block.find_all("dt")
                values = block.find_all("dd")

                if labels and values:
                    for label, value in zip(labels, values):
                        key = label.get_text(strip=True)
                        val = value.get_text(strip=True)
                        detail_data[key] = val

                # Вариант 2: div с классами
                label_divs = block.find_all("div", class_=["label", "info-label"])
                value_divs = block.find_all("div", class_=["value", "info-value"])

                if label_divs and value_divs:
                    for label, value in zip(label_divs, value_divs):
                        key = label.get_text(strip=True)
                        val = value.get_text(strip=True)
                        detail_data[key] = val

            detail_data["source_url"] = url

        except Exception as e:
            self.logger.error(f"Ошибка при парсинге детальной страницы: {e}")

        return detail_data
