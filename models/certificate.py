"""
Модель данных для квалификационного аттестата
"""

from dataclasses import dataclass, field
from typing import Optional, Dict
from datetime import datetime


@dataclass
class Certificate:
    """Модель квалификационного аттестата аудитора"""

    # Основная информация
    certificate_number: str
    auditor_full_name: str
    issue_date: datetime
    status: str

    # Дополнительная информация
    qualification_type: Optional[str] = None
    issuer: Optional[str] = None
    validity_period: Optional[str] = None

    # Данные аудитора
    auditor_inn: Optional[str] = None
    auditor_snils: Optional[str] = None

    # Причина аннулирования (для аннулированных)
    cancellation_reason: Optional[str] = None
    cancellation_date: Optional[datetime] = None

    # Метаинформация
    source_url: Optional[str] = None
    parsed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для экспорта"""
        return {
            "Номер аттестата": self.certificate_number,
            "ФИО аудитора": self.auditor_full_name,
            "Дата выдачи": (
                self.issue_date.strftime("%d.%m.%Y") if self.issue_date else ""
            ),
            "Статус": self.status,
            "Тип квалификации": self.qualification_type or "",
            "Выдан": self.issuer or "",
            "Срок действия": self.validity_period or "",
            "ИНН аудитора": self.auditor_inn or "",
            "СНИЛС аудитора": self.auditor_snils or "",
            "Причина аннулирования": self.cancellation_reason or "",
            "Дата аннулирования": (
                self.cancellation_date.strftime("%d.%m.%Y")
                if self.cancellation_date
                else ""
            ),
            "URL источника": self.source_url or "",
            "Дата сбора данных": self.parsed_at.strftime("%d.%m.%Y %H:%M:%S"),
        }
