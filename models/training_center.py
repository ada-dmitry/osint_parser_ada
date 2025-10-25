"""
Модель данных для учебно-методического центра
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class TrainingCenter:
    """Модель учебно-методического центра (УМЦ)"""

    # Основная информация
    name: str
    registration_number: str
    inn: str
    region: str
    status: Optional[str] = None

    # Дополнительная информация
    full_name: Optional[str] = None
    ogrn: Optional[str] = None
    kpp: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    director: Optional[str] = None

    # Аккредитация
    accreditation_date: Optional[datetime] = None
    accreditation_number: Optional[str] = None
    programs: List[str] = field(default_factory=list)

    # Даты
    registration_date: Optional[datetime] = None
    exclusion_date: Optional[datetime] = None
    exclusion_reason: Optional[str] = None

    # Метаинформация
    source_url: Optional[str] = None
    parsed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для экспорта"""
        return {
            "Наименование": self.name,
            "Полное наименование": self.full_name or "",
            "Регистрационный номер": self.registration_number,
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
            "Дата аккредитации": (
                self.accreditation_date.strftime("%d.%m.%Y")
                if self.accreditation_date
                else ""
            ),
            "Номер аккредитации": self.accreditation_number or "",
            "Программы": ", ".join(self.programs),
            "Дата регистрации": (
                self.registration_date.strftime("%d.%m.%Y")
                if self.registration_date
                else ""
            ),
            "Дата исключения": (
                self.exclusion_date.strftime("%d.%m.%Y") if self.exclusion_date else ""
            ),
            "Причина исключения": self.exclusion_reason or "",
            "URL источника": self.source_url or "",
            "Дата сбора данных": self.parsed_at.strftime("%d.%m.%Y %H:%M:%S"),
        }
