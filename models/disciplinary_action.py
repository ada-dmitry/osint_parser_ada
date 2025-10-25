"""
Модель данных для дисциплинарной меры
"""

from dataclasses import dataclass, field
from typing import Optional, Dict
from datetime import datetime


@dataclass
class DisciplinaryAction:
    """Модель меры дисциплинарного воздействия"""

    # Основная информация
    subject_name: str  # ФИО аудитора или название организации
    subject_type: str  # "auditor" или "organization"
    ornz: str
    action_type: str  # Тип меры воздействия

    # Детали
    violation_description: str
    decision_date: datetime
    decision_number: Optional[str] = None

    # Дополнительная информация
    inn: Optional[str] = None
    region: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    # Решение
    decision_body: Optional[str] = None
    appeal_status: Optional[str] = None

    # Метаинформация
    source_url: Optional[str] = None
    parsed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Преобразование в словарь для экспорта"""
        return {
            "Субъект": self.subject_name,
            "Тип субъекта": (
                "Аудитор" if self.subject_type == "auditor" else "Организация"
            ),
            "ОРНЗ": self.ornz,
            "Мера воздействия": self.action_type,
            "Описание нарушения": self.violation_description,
            "Дата решения": (
                self.decision_date.strftime("%d.%m.%Y") if self.decision_date else ""
            ),
            "Номер решения": self.decision_number or "",
            "ИНН": self.inn or "",
            "Регион": self.region or "",
            "Дата вступления в силу": (
                self.effective_date.strftime("%d.%m.%Y") if self.effective_date else ""
            ),
            "Дата окончания": (
                self.expiry_date.strftime("%d.%m.%Y") if self.expiry_date else ""
            ),
            "Орган принявший решение": self.decision_body or "",
            "Статус обжалования": self.appeal_status or "",
            "URL источника": self.source_url or "",
            "Дата сбора данных": self.parsed_at.strftime("%d.%m.%Y %H:%M:%S"),
        }
