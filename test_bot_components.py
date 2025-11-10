#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматический тест компонентов Jarvis Assistant Bot
Проверяет доступность всех сервисов и API ключей
"""

import sys
import json
import requests
from typing import Dict, Tuple

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Цвета для вывода
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(service: str, status: str, message: str):
    """Выводит статус проверки сервиса"""
    if status == "OK":
        print(f"{GREEN}✓{RESET} {service}: {message}")
    elif status == "ERROR":
        print(f"{RED}✗{RESET} {service}: {message}")
    elif status == "WARNING":
        print(f"{YELLOW}⚠{RESET} {service}: {message}")

def test_telegram_bot(token: str) -> Tuple[bool, str]:
    """Проверяет Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('ok'):
            bot_info = data.get('result', {})
            username = bot_info.get('username', 'Unknown')
            first_name = bot_info.get('first_name', 'Unknown')
            return True, f"Бот активен: @{username} ({first_name})"
        else:
            return False, f"Ошибка API: {data.get('description', 'Unknown error')}"
    except Exception as e:
        return False, f"Ошибка подключения: {str(e)}"

def test_telegram_webhook(token: str) -> Tuple[bool, str]:
    """Проверяет установку webhook"""
    try:
        url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('ok'):
            webhook_info = data.get('result', {})
            webhook_url = webhook_info.get('url', '')

            if webhook_url:
                pending = webhook_info.get('pending_update_count', 0)
                return True, f"Webhook установлен: {webhook_url} (ожидает: {pending})"
            else:
                return False, "Webhook не установлен! Нужно активировать workflow в n8n"
        else:
            return False, f"Ошибка: {data.get('description')}"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"

def test_google_custom_search(api_key: str, cx: str) -> Tuple[bool, str]:
    """Проверяет Google Custom Search API"""
    try:
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q=test"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            total_results = data.get('searchInformation', {}).get('totalResults', '0')
            return True, f"API работает (найдено результатов: {total_results})"
        elif response.status_code == 429:
            return False, "Превышен лимит запросов (100/день для бесплатной версии)"
        else:
            data = response.json()
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            return False, f"Ошибка API: {error_msg}"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"

def test_convertapi(api_secret: str) -> Tuple[bool, str]:
    """Проверяет ConvertAPI"""
    try:
        url = f"https://v2.convertapi.com/user?Secret={api_secret}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            seconds_left = data.get('SecondsLeft', 0)
            return True, f"API работает (осталось секунд: {seconds_left})"
        else:
            return False, f"Ошибка API: статус {response.status_code}"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"

def test_n8n_availability(url: str) -> Tuple[bool, str]:
    """Проверяет доступность n8n"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, "n8n instance доступен"
        else:
            return False, f"Статус: {response.status_code}"
    except Exception as e:
        return False, f"Недоступен: {str(e)}"

def main():
    """Основная функция тестирования"""
    print("\n" + "="*60)
    print("🤖 Jarvis Assistant - Проверка компонентов системы")
    print("="*60 + "\n")

    # Загружаем credentials (если есть)
    TELEGRAM_TOKEN = "8440983697:AAFns8rfe5pzMCRQxBbJOMSy73X6CW_1Gdk"
    GOOGLE_API_KEY = "AIzaSyDhV99XrRlFjLW1PufniRv57nPdQe9aBtc"
    GOOGLE_CX = "d0fe2c20be7944723"
    CONVERTAPI_SECRET = "ztPOkh7Tu0d89y7E5e1QgCw3US20rNUD"
    N8N_URL = "https://n8n.kir-ito.ru/"

    print("📡 Проверка базовых сервисов:\n")

    # Тест n8n
    success, message = test_n8n_availability(N8N_URL)
    print_status("n8n Instance", "OK" if success else "ERROR", message)

    # Тест Telegram Bot
    success, message = test_telegram_bot(TELEGRAM_TOKEN)
    print_status("Telegram Bot API", "OK" if success else "ERROR", message)

    # Тест Telegram Webhook
    success, message = test_telegram_webhook(TELEGRAM_TOKEN)
    print_status("Telegram Webhook", "OK" if success else "WARNING", message)

    # Тест Google Custom Search
    success, message = test_google_custom_search(GOOGLE_API_KEY, GOOGLE_CX)
    print_status("Google Custom Search", "OK" if success else "ERROR", message)

    # Тест ConvertAPI
    success, message = test_convertapi(CONVERTAPI_SECRET)
    print_status("ConvertAPI", "OK" if success else "ERROR", message)

    print("\n" + "="*60)
    print("⚠️  Credentials требующие ручной проверки в n8n:")
    print("="*60 + "\n")

    credentials_to_check = [
        ("OpenAI/OpenRouter", "z0vBSqt6SlKhroIR", "Для Whisper, GPT-4o-mini, embeddings"),
        ("Google Gemini", "qEF2TfQl9STbXGRw", "Основная языковая модель"),
        ("Supabase", "Kpj9ArW3swQdueue", "Векторная база знаний"),
        ("PostgreSQL", "P8hk2UZbE9YDsHIB", "Память разговоров"),
        ("Google Drive", "MjNkJQC04HTyzo2W", "Загрузка базы знаний"),
        ("Cohere", "fCIyqRXZvjN2BZcA", "Reranking результатов"),
    ]

    for name, cred_id, purpose in credentials_to_check:
        print(f"{YELLOW}⚠{RESET} {name}")
        print(f"   Credential ID: {cred_id}")
        print(f"   Назначение: {purpose}")
        print(f"   Проверить в: n8n → Settings → Credentials\n")

    print("="*60)
    print("\n✅ Следующие шаги:")
    print("1. Открыть n8n: https://n8n.kir-ito.ru/")
    print("2. Активировать workflow 'paraplexity 3.0' (если неактивен)")
    print("3. Проверить каждый credential в списке выше")
    print("4. Запустить узел 'When clicking Execute workflow' для загрузки базы знаний")
    print("5. Протестировать бота: @Baga_assistant_bot\n")

if __name__ == "__main__":
    main()
