"""
Модель данных для сети аудиторских организаций
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class AuditNetwork:
    """Модель сети аудиторских организаций"""

    # Основная информация
    name: str
    network_type: str  # "Российская" или "Международная"
    registration_number: Optional[str] = None

    # Участники
    member_organizations: List[str] = field(default_factory=list)
    member_count: Optional[int] = None

    # Дополнительная информация
    country: Optional[str] = None
    headquarters: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None

    # Контакты
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    # Метаинформация
    source_url: Optional[str] = None
    parsed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для экспорта"""
        return {
            "Название сети": self.name,
            "Тип": self.network_type,
            "Регистрационный номер": self.registration_number or "",
            "Количество участников": self.member_count or "",
            "Участники": ", ".join(self.member_organizations[:10]),  # Первые 10
            "Страна": self.country or "",
            "Штаб-квартира": self.headquarters or "",
            "Сайт": self.website or "",
            "Описание": self.description or "",
            "Контактное лицо": self.contact_person or "",
            "Телефон": self.phone or "",
            "Email": self.email or "",
            "URL источника": self.source_url or "",
            "Дата сбора данных": self.parsed_at.strftime("%d.%m.%Y %H:%M:%S"),
        }
