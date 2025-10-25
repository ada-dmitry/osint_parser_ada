#!/bin/bash

# Скрипт быстрого запуска парсера СРО ААС
# Использование: ./run.sh

echo "=============================================="
echo "   ПАРСЕР РЕЕСТРОВ СРО ААС"
echo "=============================================="
echo ""

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.8 или выше."
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Виртуальное окружение не найдено. Создание..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано."
    echo ""
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверка зависимостей
if ! python -c "import requests" 2>/dev/null; then
    echo "📥 Установка зависимостей..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo "✅ Зависимости установлены."
    echo ""
fi

# Создание необходимых директорий
mkdir -p data/exports
mkdir -p logs

# Запуск парсера
echo "🚀 Запуск парсера..."
echo ""
python main.py

# Деактивация виртуального окружения
deactivate
