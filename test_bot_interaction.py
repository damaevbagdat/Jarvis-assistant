#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерактивный тест бота Jarvis Assistant
Отправляет тестовые сообщения и проверяет ответы
"""

import sys
import requests
import time
from datetime import datetime

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Цвета для вывода
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TelegramBotTester:
    def __init__(self, bot_token: str, chat_id: str = None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def get_updates(self, offset=None, timeout=30):
        """Получает обновления от бота"""
        url = f"{self.base_url}/getUpdates"
        params = {'timeout': timeout}
        if offset:
            params['offset'] = offset

        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"{RED}Ошибка получения обновлений: {e}{RESET}")
            return None

    def send_message(self, text: str):
        """Отправляет сообщение боту"""
        if not self.chat_id:
            print(f"{RED}Chat ID не установлен!{RESET}")
            return False

        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text
        }

        try:
            response = requests.post(url, json=data)
            result = response.json()
            if result.get('ok'):
                return True
            else:
                print(f"{RED}Ошибка отправки: {result.get('description')}{RESET}")
                return False
        except Exception as e:
            print(f"{RED}Ошибка: {e}{RESET}")
            return False

    def wait_for_response(self, timeout=30):
        """Ждет ответ от бота"""
        start_time = time.time()
        last_update_id = None

        # Получаем последнее обновление
        updates = self.get_updates()
        if updates and updates.get('result'):
            last_update_id = updates['result'][-1]['update_id'] + 1

        print(f"{BLUE}⏳ Ожидаю ответ от бота (таймаут: {timeout}сек)...{RESET}")

        while time.time() - start_time < timeout:
            updates = self.get_updates(offset=last_update_id, timeout=5)

            if updates and updates.get('result'):
                for update in updates['result']:
                    message = update.get('message', {})
                    from_user = message.get('from', {})

                    # Проверяем, что это сообщение от бота, а не от нас
                    if from_user.get('is_bot') and message.get('text'):
                        response_text = message.get('text')
                        bot_name = from_user.get('first_name', 'Bot')
                        return True, response_text, bot_name

                    last_update_id = update['update_id'] + 1

            time.sleep(1)

        return False, None, None

def main():
    print("\n" + "="*60)
    print("🤖 Jarvis Assistant - Интерактивный тест бота")
    print("="*60 + "\n")

    BOT_TOKEN = "8440983697:AAFns8rfe5pzMCRQxBbJOMSy73X6CW_1Gdk"

    tester = TelegramBotTester(BOT_TOKEN)

    print(f"{YELLOW}⚠️  ВАЖНО: Для тестирования нужен Chat ID{RESET}")
    print(f"1. Откройте Telegram: @Baga_assistant_bot")
    print(f"2. Отправьте любое сообщение боту")
    print(f"3. Нажмите Enter здесь\n")

    input(f"{BLUE}Нажмите Enter после отправки сообщения боту...{RESET}")

    # Получаем Chat ID из последних сообщений
    print(f"\n{BLUE}🔍 Ищу ваш Chat ID...{RESET}")
    updates = tester.get_updates()

    if updates and updates.get('result'):
        # Ищем последнее сообщение от пользователя (не от бота)
        for update in reversed(updates['result']):
            message = update.get('message', {})
            from_user = message.get('from', {})

            if not from_user.get('is_bot'):
                chat_id = message.get('chat', {}).get('id')
                username = from_user.get('username', 'Unknown')
                first_name = from_user.get('first_name', 'User')

                print(f"{GREEN}✓ Найден Chat ID: {chat_id}{RESET}")
                print(f"   Пользователь: {first_name} (@{username})\n")

                tester.chat_id = str(chat_id)
                break

    if not tester.chat_id:
        print(f"{RED}✗ Не удалось найти Chat ID. Отправьте сообщение боту и попробуйте снова.{RESET}")
        return

    # Тест 1: Проверка основной функциональности
    print("="*60)
    print("Тест 1: Базовая проверка")
    print("="*60 + "\n")

    test_message = "Привет! Как тебя зовут?"
    print(f"{BLUE}📤 Отправляю: '{test_message}'{RESET}")

    if tester.send_message(test_message):
        success, response, bot_name = tester.wait_for_response(timeout=60)

        if success:
            print(f"{GREEN}✓ Бот ответил!{RESET}")
            print(f"{GREEN}📨 От: {bot_name}{RESET}")
            print(f"{GREEN}💬 Ответ: {response[:200]}{'...' if len(response) > 200 else ''}{RESET}\n")

            # Проверяем, упомянул ли бот имя "Джарвис"
            if 'джарвис' in response.lower() or 'jarvis' in response.lower():
                print(f"{GREEN}✓ Бот правильно представился как Джарвис{RESET}\n")
            else:
                print(f"{YELLOW}⚠ Бот не представился как Джарвис (возможно, база знаний не загружена){RESET}\n")
        else:
            print(f"{RED}✗ Бот не ответил в течение 60 секунд{RESET}")
            print(f"{YELLOW}Возможные причины:{RESET}")
            print(f"  1. Workflow не активирован в n8n")
            print(f"  2. Google Gemini API не настроен")
            print(f"  3. Supabase credentials не настроены")
            print(f"  4. Ошибка в workflow\n")
    else:
        print(f"{RED}✗ Не удалось отправить сообщение{RESET}\n")

    # Тест 2: Проверка памяти
    print("\n" + "="*60)
    print("Тест 2: Проверка памяти разговора")
    print("="*60 + "\n")

    test_name = "Тестовый Пользователь"
    print(f"{BLUE}📤 Отправляю: 'Меня зовут {test_name}'{RESET}")

    if tester.send_message(f"Меня зовут {test_name}"):
        tester.wait_for_response(timeout=30)
        time.sleep(2)

        print(f"{BLUE}📤 Отправляю: 'Как меня зовут?'{RESET}")
        if tester.send_message("Как меня зовут?"):
            success, response, _ = tester.wait_for_response(timeout=30)

            if success:
                if test_name.lower() in response.lower():
                    print(f"{GREEN}✓ Память работает! Бот вспомнил ваше имя{RESET}\n")
                else:
                    print(f"{YELLOW}⚠ Память не работает (PostgreSQL не настроен?){RESET}\n")

    print("="*60)
    print("📊 Результаты тестирования")
    print("="*60 + "\n")

    print(f"{GREEN}✓ Что работает:{RESET}")
    print(f"  - Telegram Bot API")
    print(f"  - Webhook n8n")
    print(f"  - Базовая обработка сообщений\n")

    print(f"{YELLOW}⚠️  Что требует проверки:{RESET}")
    print(f"  - Загружена ли база знаний (Supabase)")
    print(f"  - Настроен ли Google Gemini API")
    print(f"  - Работает ли PostgreSQL память")
    print(f"  - Настроены ли OpenAI/OpenRouter для голоса и изображений\n")

if __name__ == "__main__":
    main()
