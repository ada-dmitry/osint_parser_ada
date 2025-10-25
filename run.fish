#!/usr/bin/env fish

# Скрипт быстрого запуска для Fish Shell
# Использование: ./run.fish

echo "=============================================="
echo "   ПАРСЕР РЕЕСТРОВ СРО ААС"
echo "=============================================="
echo ""

# Проверка наличия Python
if not command -v python3 &> /dev/null
    echo "❌ Python 3 не найден. Установите Python 3.8 или выше."
    exit 1
end

echo "✅ Python найден: "(python3 --version)
echo ""

# Проверка виртуального окружения
if not test -d venv
    echo "📦 Виртуальное окружение не найдено. Создание..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано."
    echo ""
end

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate.fish

# Проверка зависимостей
if not python -c "import requests" 2>/dev/null
    echo "📥 Установка зависимостей..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo "✅ Зависимости установлены."
    echo ""
end

# Создание необходимых директорий
mkdir -p data/exports
mkdir -p logs

# Запуск парсера
echo "🚀 Запуск парсера..."
echo ""
python main.py

# Деактивация виртуального окружения
deactivate
