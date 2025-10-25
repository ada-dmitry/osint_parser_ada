"""
Базовый парсер для реестров СРО ААС
"""

import requests
import time
import re
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import PARSER_CONFIG, BASE_URL
from utils.logger import setup_logger


class BaseParser(ABC):
    """
    Базовый класс для парсеров реестров СРО ААС
    """

    def __init__(self, registry_url: str, registry_name: str):
        """
        Инициализация парсера

        Args:
            registry_url: URL реестра
            registry_name: Название реестра
        """
        self.registry_url = registry_url
        self.registry_name = registry_name
        self.logger = setup_logger(f"{self.__class__.__name__}")

        # Настройки сессии
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": PARSER_CONFIG["user_agent"]})

        self.timeout = PARSER_CONFIG["timeout"]
        self.delay = PARSER_CONFIG["delay_between_requests"]
        self.max_retries = PARSER_CONFIG["max_retries"]

    def _make_request(
        self, url: str, params: Optional[Dict] = None
    ) -> Optional[requests.Response]:
        """
        Выполнение HTTP-запроса с повторными попытками

        Args:
            url: URL для запроса
            params: Параметры запроса

        Returns:
            Response объект или None в случае ошибки
        """
        for attempt in range(self.max_retries):
            try:
                self.logger.debug(
                    f"Запрос к {url} (попытка {attempt + 1}/{self.max_retries})"
                )
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()

                # Задержка между запросами
                time.sleep(self.delay)

                return response

            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Ошибка при запросе {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))
                else:
                    self.logger.error(
                        f"Не удалось выполнить запрос к {url} после {self.max_retries} попыток"
                    )

        return None

    def _parse_html(self, html: str) -> BeautifulSoup:
        """
        Парсинг HTML

        Args:
            html: HTML-контент

        Returns:
            BeautifulSoup объект
        """
        return BeautifulSoup(html, "lxml")

    def _get_pagination_urls(self, base_url: str, soup: BeautifulSoup) -> List[str]:
        """
        Получение списка URL всех страниц с пагинацией

        Args:
            base_url: Базовый URL реестра
            soup: Parsed HTML основной страницы

        Returns:
            Список URL всех страниц
        """
        urls = [base_url]

        # Поиск пагинации (разные варианты классов)
        pagination = (
            soup.find("div", class_="b-pagination-block")
            or soup.find("div", class_="pagination")
            or soup.find("ul", class_="pagination")
        )

        if pagination:
            # Находим максимальный номер страницы
            max_page = 1
            links = pagination.find_all("a")

            for link in links:
                href = link.get("href")
                if href and href not in ["#", ""]:
                    # Проверяем, что href - строка, а не список
                    if isinstance(href, list):
                        href = href[0] if href else None
                    if href:
                        # Извлекаем номер страницы из URL
                        # Формат: ?PAGEN_1=page-N
                        match = re.search(r"page-(\d+)", str(href))
                        if match:
                            page_num = int(match.group(1))
                            max_page = max(max_page, page_num)
                        else:
                            # Добавляем URL как есть (для других форматов пагинации)
                            page_url = urljoin(BASE_URL, href)
                            if page_url not in urls:
                                urls.append(page_url)

            # Генерируем URL-ы для всех страниц
            if max_page > 1:
                self.logger.info(f"Обнаружено страниц: {max_page}")
                urls = [base_url]  # Очищаем и добавляем первую
                for page_num in range(2, max_page + 1):
                    # Формируем URL для каждой страницы
                    page_url = f"{base_url}?PAGEN_1=page-{page_num}"
                    urls.append(page_url)

        self.logger.info(f"Найдено страниц с пагинацией: {len(urls)}")
        return urls

    @abstractmethod
    def parse_list_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Парсинг страницы со списком записей реестра

        Args:
            soup: Parsed HTML страницы

        Returns:
            Список словарей с данными
        """
        pass

    @abstractmethod
    def parse_detail_page(self, url: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Парсинг детальной страницы записи

        Args:
            url: URL детальной страницы
            soup: Parsed HTML страницы

        Returns:
            Словарь с детальными данными
        """
        pass

    def parse_registry(self, detailed: bool = False) -> List[Dict[str, Any]]:
        """
        Парсинг всего реестра

        Args:
            detailed: Парсить ли детальные страницы
                      True - парсить все страницы с детальной информацией
                      False - парсить только первую страницу без деталей

        Returns:
            Список собранных данных
        """
        self.logger.info(f"Начало парсинга реестра: {self.registry_name}")
        all_data = []

        # Получение первой страницы
        response = self._make_request(self.registry_url)
        if not response:
            self.logger.error("Не удалось получить первую страницу реестра")
            return all_data

        soup = self._parse_html(response.text)

        # В режиме detailed=True парсим все страницы, иначе только первую
        if detailed:
            pagination_urls = self._get_pagination_urls(self.registry_url, soup)
        else:
            pagination_urls = [self.registry_url]
            self.logger.info("Режим быстрого сканирования: только первая страница")

        # Парсинг каждой страницы
        for page_num, page_url in enumerate(pagination_urls, 1):
            self.logger.info(
                f"Парсинг страницы {page_num}/{len(pagination_urls)}: {page_url}"
            )

            if page_num > 1:  # Первую страницу уже получили
                response = self._make_request(page_url)
                if not response:
                    continue
                soup = self._parse_html(response.text)

            # Парсинг списка на странице
            page_data = self.parse_list_page(soup)
            self.logger.info(f"Найдено записей на странице: {len(page_data)}")

            # Детальный парсинг, если требуется
            if detailed:
                for item in page_data:
                    if "detail_url" in item and item["detail_url"] is not None:
                        detail_response = self._make_request(item["detail_url"])
                        if detail_response:
                            detail_soup = self._parse_html(detail_response.text)
                            detail_data = self.parse_detail_page(
                                item["detail_url"], detail_soup
                            )
                            item.update(detail_data)

            all_data.extend(page_data)

        self.logger.info(f"Парсинг завершен. Всего записей: {len(all_data)}")
        return all_data
