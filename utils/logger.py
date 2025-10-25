"""
Настройка логирования
"""

import logging
import os
from datetime import datetime
from config import LOGGING_CONFIG


def setup_logger(name: str = "sro_parser") -> logging.Logger:
    """
    Настройка логгера для парсера

    Args:
        name: Имя логгера

    Returns:
        Настроенный логгер
    """
    # Создание директории для логов
    log_dir = LOGGING_CONFIG.get("log_dir", "logs/")
    os.makedirs(log_dir, exist_ok=True)

    # Создание логгера
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_CONFIG.get("level", "INFO"))

    # Очистка существующих обработчиков
    if logger.hasHandlers():
        logger.handlers.clear()

    # Формат логов
    formatter = logging.Formatter(LOGGING_CONFIG.get("format"))

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Обработчик для файла
    log_file = os.path.join(
        log_dir, f"parser_{datetime.now().strftime('%Y-%m-%d')}.log"
    )
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
