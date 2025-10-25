"""
Парсер реестра аудиторов и индивидуальных аудиторов
"""

from typing import List, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

from parsers.base_parser import BaseParser
from models.auditor import Auditor
from config import BASE_URL


class AuditorsParser(BaseParser):
    """
    Парсер для реестра аудиторов и индивидуальных аудиторов
    https://sroaas.ru/reestr/auditory/
    """

    def __init__(self):
        from config import REGISTRIES

        registry = REGISTRIES["auditors"]
        super().__init__(registry["url"], registry["name"])

    def parse_list_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Парсинг страницы со списком аудиторов

        Args:
            soup: Parsed HTML страницы

        Returns:
            Список словарей с данными аудиторов
        """
        auditors = []

        # Поиск таблицы с данными
        table = soup.find("table")
        if not table:
            self.logger.warning("Таблица с данными не найдена на странице")
            return auditors

        # Парсинг строк таблицы
        rows = table.find_all("tr")[1:]  # Пропускаем заголовок

        for row in rows:
            try:
                cols = row.find_all("td")
                if len(cols) < 4:
                    continue

                # Извлечение данных
                full_name = cols[0].get_text(strip=True)
                ornz = cols[1].get_text(strip=True)
                certificate_number = cols[2].get_text(strip=True)
                region = cols[3].get_text(strip=True)

                # Статус (если есть)
                status = cols[4].get_text(strip=True) if len(cols) > 4 else None

                # URL детальной страницы
                detail_url = None
                link = row.find("a")
                if link:
                    href = link.get("href")
                    # Проверяем, что href - строка, а не список
                    if isinstance(href, list):
                        href = href[0] if href else None
                    if href:
                        detail_url = urljoin(BASE_URL, href)

                auditor_data = {
                    "full_name": full_name,
                    "ornz": ornz,
                    "certificate_number": certificate_number,
                    "region": region,
                    "status": status,
                    "detail_url": detail_url,
                }

                auditors.append(auditor_data)

            except Exception as e:
                self.logger.error(f"Ошибка при парсинге строки таблицы: {e}")
                continue

        return auditors

    def parse_detail_page(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Парсинг детальной страницы аудитора

        Args:
            url: URL детальной страницы
            soup: Parsed HTML страницы

        Returns:
            Словарь с детальными данными
        """
        detail_data = {}

        try:
            info_blocks = soup.find_all("div", class_=["info-block", "detail-info"])

            for block in info_blocks:
                labels = block.find_all(["dt", "div"], class_=["label", "info-label"])
                values = block.find_all(["dd", "div"], class_=["value", "info-value"])

                for label, value in zip(labels, values):
                    key = label.get_text(strip=True).lower()
                    val = value.get_text(strip=True)

                    if "инн" in key:
                        detail_data["inn"] = val
                    elif "снилс" in key:
                        detail_data["snils"] = val
                    elif "квалификация" in key:
                        detail_data["qualification"] = val
                    elif "организация" in key and "название" in key:
                        detail_data["organization_name"] = val
                    elif "организация" in key and "инн" in key:
                        detail_data["organization_inn"] = val
                    elif "образование" in key:
                        detail_data["education"] = val
                    elif "стаж" in key:
                        match = re.search(r"\d+", val)
                        if match:
                            detail_data["experience_years"] = int(match.group())

            detail_data["source_url"] = url

        except Exception as e:
            self.logger.error(f"Ошибка при парсинге детальной страницы {url}: {e}")

        return detail_data

    def parse_to_objects(self, detailed: bool = False) -> List[Auditor]:
        """
        Парсинг реестра с преобразованием в объекты Auditor

        Args:
            detailed: Парсить ли детальные страницы

        Returns:
            Список объектов Auditor
        """
        data = self.parse_registry(detailed=detailed)
        auditors = []

        for item in data:
            try:
                auditor = Auditor(
                    full_name=item.get("full_name", ""),
                    ornz=item.get("ornz", ""),
                    certificate_number=item.get("certificate_number", ""),
                    region=item.get("region", ""),
                    status=item.get("status"),
                    inn=item.get("inn"),
                    snils=item.get("snils"),
                    qualification=item.get("qualification"),
                    organization_name=item.get("organization_name"),
                    organization_inn=item.get("organization_inn"),
                    education=item.get("education"),
                    experience_years=item.get("experience_years"),
                    source_url=item.get("source_url"),
                )
                auditors.append(auditor)
            except Exception as e:
                self.logger.error(f"Ошибка при создании объекта Auditor: {e}")
                continue

        return auditors
