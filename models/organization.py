"""
Модель данных для аудиторской организации
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class Organization:
    """Модель аудиторской организации"""

    # Основная информация
    name: str
    ornz: str  # Основной регистрационный номер записи
    inn: str
    region: str
    status: Optional[str] = None

    # Дополнительная информация (заполняется при детальном парсе)
    full_name: Optional[str] = None
    ogrn: Optional[str] = None
    kpp: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    director: Optional[str] = None

    # Даты
    registration_date: Optional[datetime] = None
    membership_start_date: Optional[datetime] = None
    membership_end_date: Optional[datetime] = None

    # Дополнительные данные
    auditors_count: Optional[int] = None
    certificates: List[str] = field(default_factory=list)
    networks: List[str] = field(default_factory=list)

    # Метаинформация
    source_url: Optional[str] = None
    parsed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для экспорта"""
        return {
            "Наименование": self.name,
            "Полное наименование": self.full_name or "",
            "ОРНЗ": self.ornz,
            "ИНН": self.inn,
            "КПП": self.kpp or "",
            "ОГРН": self.ogrn or "",
            "Регион": self.region,
            "Статус": self.status or "",
            "Адрес": self.address or "",
            "Телефон": self.phone or "",
            "Email": self.email or "",
            "Сайт": self.website or "",
            "Руководитель": self.director or "",
            "Дата регистрации": (
                self.registration_date.strftime("%d.%m.%Y")
                if self.registration_date
                else ""
            ),
            "Дата начала членства": (
                self.membership_start_date.strftime("%d.%m.%Y")
                if self.membership_start_date
                else ""
            ),
            "Дата окончания членства": (
                self.membership_end_date.strftime("%d.%m.%Y")
                if self.membership_end_date
                else ""
            ),
            "Количество аудиторов": self.auditors_count or "",
            "Сертификаты": ", ".join(self.certificates),
            "Сети": ", ".join(self.networks),
            "URL источника": self.source_url or "",
            "Дата сбора данных": self.parsed_at.strftime("%d.%m.%Y %H:%M:%S"),
        }
