"""
Модель данных для аудитора
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class Auditor:
    """Модель аудитора или индивидуального аудитора"""

    # Основная информация
    full_name: str
    ornz: str  # Основной регистрационный номер записи
    certificate_number: str
    region: str
    status: Optional[str] = None

    # Дополнительная информация
    inn: Optional[str] = None
    snils: Optional[str] = None
    qualification: Optional[str] = None

    # Организация (для аудиторов)
    organization_name: Optional[str] = None
    organization_inn: Optional[str] = None

    # Даты
    certificate_issue_date: Optional[datetime] = None
    membership_start_date: Optional[datetime] = None
    membership_end_date: Optional[datetime] = None

    # Дополнительные данные
    education: Optional[str] = None
    experience_years: Optional[int] = None
    specializations: List[str] = field(default_factory=list)

    # Метаинформация
    source_url: Optional[str] = None
    parsed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для экспорта"""
        return {
            "ФИО": self.full_name,
            "ОРНЗ": self.ornz,
            "Номер аттестата": self.certificate_number,
            "Регион": self.region,
            "Статус": self.status or "",
            "ИНН": self.inn or "",
            "СНИЛС": self.snils or "",
            "Квалификация": self.qualification or "",
            "Организация": self.organization_name or "",
            "ИНН организации": self.organization_inn or "",
            "Дата выдачи аттестата": (
                self.certificate_issue_date.strftime("%d.%m.%Y")
                if self.certificate_issue_date
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
            "Образование": self.education or "",
            "Стаж (лет)": self.experience_years or "",
            "Специализации": ", ".join(self.specializations),
            "URL источника": self.source_url or "",
            "Дата сбора данных": self.parsed_at.strftime("%d.%m.%Y %H:%M:%S"),
        }
