"""
Модуль парсеров для различных реестров СРО ААС
"""

from .base_parser import BaseParser
from .organizations_parser import OrganizationsParser
from .auditors_parser import AuditorsParser
from .generic_parser import GenericRegistryParser

__all__ = [
    "BaseParser",
    "OrganizationsParser",
    "AuditorsParser",
    "GenericRegistryParser",
]
