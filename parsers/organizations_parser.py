"""
Парсер реестра аудиторских организаций
"""

from typing import List, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

from parsers.base_parser import BaseParser
from models.organization import Organization
from config import BASE_URL


class OrganizationsParser(BaseParser):
    """
    Парсер для реестра аудиторских организаций
    https://sroaas.ru/reestr/organizatsiy/
    """

    def __init__(self):
        from config import REGISTRIES

        registry = REGISTRIES["organizations"]
        super().__init__(registry["url"], registry["name"])

    def parse_list_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Парсинг страницы со списком аудиторских организаций

        Args:
            soup: Parsed HTML страницы

        Returns:
            Список словарей с данными организаций
        """
        organizations = []

        # Поиск таблицы с данными
        table = soup.find("table")
        if not table:
            self.logger.warning("Таблица с данными не найдена на странице")
            return organizations

        # Парсинг строк таблицы
        rows = table.find_all("tr")[1:]  # Пропускаем заголовок

        for row in rows:
            try:
                cols = row.find_all("td")
                if len(cols) < 4:
                    continue

                # Извлечение данных
                name = cols[0].get_text(strip=True)
                ornz = cols[1].get_text(strip=True)
                inn = cols[2].get_text(strip=True)
                region = cols[3].get_text(strip=True)

                # Статус (если есть)
                status = cols[4].get_text(strip=True) if len(cols) > 4 else None

                # URL детальной страницы (если есть ссылка)
                detail_url = None
                link = row.find("a")
                if link:
                    href = link.get("href")
                    # Проверяем, что href - строка, а не список
                    if isinstance(href, list):
                        href = href[0] if href else None
                    if href:
                        detail_url = urljoin(BASE_URL, href)

                org_data = {
                    "name": name,
                    "ornz": ornz,
                    "inn": inn,
                    "region": region,
                    "status": status,
                    "detail_url": detail_url,
                }

                organizations.append(org_data)

            except Exception as e:
                self.logger.error(f"Ошибка при парсинге строки таблицы: {e}")
                continue

        return organizations

    def parse_detail_page(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Парсинг детальной страницы организации

        Args:
            url: URL детальной страницы
            soup: Parsed HTML страницы

        Returns:
            Словарь с детальными данными
        """
        detail_data = {}

        try:
            # Поиск блока с детальной информацией
            info_blocks = soup.find_all("div", class_=["info-block", "detail-info"])

            for block in info_blocks:
                # Извлечение пар ключ-значение
                labels = block.find_all(["dt", "div"], class_=["label", "info-label"])
                values = block.find_all(["dd", "div"], class_=["value", "info-value"])

                for label, value in zip(labels, values):
                    key = label.get_text(strip=True).lower()
                    val = value.get_text(strip=True)

                    # Маппинг полей
                    if "полное наименование" in key or "полное название" in key:
                        detail_data["full_name"] = val
                    elif "огрн" in key:
                        detail_data["ogrn"] = val
                    elif "кпп" in key:
                        detail_data["kpp"] = val
                    elif "адрес" in key:
                        detail_data["address"] = val
                    elif "телефон" in key or "тел" in key:
                        detail_data["phone"] = val
                    elif "email" in key or "e-mail" in key or "почта" in key:
                        detail_data["email"] = val
                    elif "сайт" in key or "веб-сайт" in key:
                        detail_data["website"] = val
                    elif "руководитель" in key or "директор" in key:
                        detail_data["director"] = val
                    elif "дата регистрации" in key:
                        detail_data["registration_date"] = val
                    elif "дата начала членства" in key or "дата вступления" in key:
                        detail_data["membership_start_date"] = val
                    elif "количество аудиторов" in key:
                        # Извлечение числа
                        match = re.search(r"\d+", val)
                        if match:
                            detail_data["auditors_count"] = int(match.group())

            # Поиск информации о сертификатах
            certificates_section = soup.find(
                "div", class_=["certificates", "attestaty"]
            )
            if certificates_section:
                certs = []
                cert_items = certificates_section.find_all(
                    ["li", "div"], class_="certificate-item"
                )
                for cert in cert_items:
                    certs.append(cert.get_text(strip=True))
                if certs:
                    detail_data["certificates"] = certs

            # Поиск информации о сетях
            networks_section = soup.find("div", class_=["networks", "seti"])
            if networks_section:
                nets = []
                net_items = networks_section.find_all(
                    ["li", "div"], class_="network-item"
                )
                for net in net_items:
                    nets.append(net.get_text(strip=True))
                if nets:
                    detail_data["networks"] = nets

            detail_data["source_url"] = url

        except Exception as e:
            self.logger.error(f"Ошибка при парсинге детальной страницы {url}: {e}")

        return detail_data

    def parse_to_objects(self, detailed: bool = False) -> List[Organization]:
        """
        Парсинг реестра с преобразованием в объекты Organization

        Args:
            detailed: Парсить ли детальные страницы

        Returns:
            Список объектов Organization
        """
        data = self.parse_registry(detailed=detailed)
        organizations = []

        for item in data:
            try:
                org = Organization(
                    name=item.get("name", ""),
                    ornz=item.get("ornz", ""),
                    inn=item.get("inn", ""),
                    region=item.get("region", ""),
                    status=item.get("status"),
                    full_name=item.get("full_name"),
                    ogrn=item.get("ogrn"),
                    kpp=item.get("kpp"),
                    address=item.get("address"),
                    phone=item.get("phone"),
                    email=item.get("email"),
                    website=item.get("website"),
                    director=item.get("director"),
                    auditors_count=item.get("auditors_count"),
                    certificates=item.get("certificates", []),
                    networks=item.get("networks", []),
                    source_url=item.get("source_url"),
                )
                organizations.append(org)
            except Exception as e:
                self.logger.error(f"Ошибка при создании объекта Organization: {e}")
                continue

        return organizations
