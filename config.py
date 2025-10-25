"""
Конфигурационный файл парсера СРО ААС
"""

# Базовые настройки
BASE_URL = "https://sroaas.ru"

# URL реестров
REGISTRIES = {
    # Реестры действительных членов и выданных аттестатов
    "auditors": {
        "name": "Реестр членов — аудиторов и индивидуальных аудиторов",
        "url": f"{BASE_URL}/reestr/auditory/",
        "active": True,
    },
    "organizations": {
        "name": "Реестр членов — аудиторских организаций",
        "url": f"{BASE_URL}/reestr/organizatsiy/",
        "active": True,
    },
    "certificates": {
        "name": "Реестр выданных СРО ААС квалификационных аттестатов аудитора",
        "url": f"{BASE_URL}/reestr/reestr-vydannykh-sro-aas-kvalifikatsionnykh-attestatov-auditora/",
        "active": True,
    },
    "individual_auditors": {
        "name": "Перечень индивидуальных аудиторов",
        "url": f"{BASE_URL}/reestr/ia/",
        "active": True,
    },
    "training_centers": {
        "name": "Реестр учебно-методических центров",
        "url": f"{BASE_URL}/reestr/umc/",
        "active": True,
    },
    "oppk_confirmation": {
        "name": "Сведения о подтверждении ОППК аудиторами",
        "url": f"{BASE_URL}/reestr/oppk/",
        "active": True,
    },
    "ozo_training": {
        "name": "Сведения о прохождении ПК руководителем аудита ОЗО ФР",
        "url": f"{BASE_URL}/reestr/pcozo/",
        "active": True,
    },
    # Реестры исключенных членов и аннулированных аттестатов
    "excluded_auditors": {
        "name": "Реестр аудиторов, прекративших членство в СРО ААС",
        "url": f"{BASE_URL}/reestr/reestr-auditorov-prekrativshikh-chlenstvo-v-sro-aas/",
        "active": True,
    },
    "excluded_organizations": {
        "name": "Реестр аудиторских организаций, прекративших членство в СРО ААС",
        "url": f"{BASE_URL}/reestr/reestr-auditorskikh-organizatsiy-prekrativshikh-chlenstvo-v-sro-aas/",
        "active": True,
    },
    "cancelled_certificates": {
        "name": "Реестр аннулированных СРО ААС квалификационных аттестатов аудитора",
        "url": f"{BASE_URL}/reestr/reestr-annulirovannykh-sro-aas-kvalifikatsionnykh-attestatov-auditora/",
        "active": True,
    },
    "excluded_training_centers": {
        "name": "УМЦ, исключенные из реестра СРО ААС",
        "url": f"{BASE_URL}/reestr/umc-prekrativshikh-chlenstvo/",
        "active": True,
    },
    # Реестры дисциплинарных мер
    "disciplinary_auditors": {
        "name": "Меры дисциплинарного воздействия к членам СРО ААС - аудиторам",
        "url": f"{BASE_URL}/reestr/mery-distsiplinarnogo-vozdeystviya-k-chlenam-sro-aas/",
        "active": True,
    },
    "disciplinary_organizations": {
        "name": "Меры дисциплинарного воздействия к членам СРО – аудиторским организациям",
        "url": f"{BASE_URL}/reestr/mery-distsiplinarnogo-vozdeystviya-k-chlenam-sro-aas-organizatsiy/",
        "active": True,
    },
    # Перечень сетей
    "audit_networks": {
        "name": "Перечень российских и международных сетей аудиторских организаций",
        "url": f"{BASE_URL}/reestr/seti-auditorskikh-organizatsiy",
        "active": True,
    },
}

# Настройки парсера
PARSER_CONFIG = {
    "timeout": 30,  # таймаут запроса в секундах
    "delay_between_requests": 1,  # задержка между запросами в секундах
    "max_retries": 3,  # максимальное количество попыток
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Настройки экспорта
EXPORT_CONFIG = {
    "output_dir": "data/exports/",
    "date_format": "%Y-%m-%d_%H-%M-%S",
    "encoding": "utf-8",
}

# Настройки логирования
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_dir": "logs/",
}
