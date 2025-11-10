# Jarvis Assistant - Лог Работы

**Дата начала:** 2025-11-10
**Имя бота:** Baga_assistant_bot
**Технологии:** Telegram Bot API, n8n

---

## Выполненные задачи

### 2025-11-10

- [x] Создана локальная папка проекта: `C:\Users\damae\OneDrive\Документы\GitHub\Jarvis-assistant`
- [x] Инициализирован git репозиторий
- [x] Создан файл WORK_LOG.md для отслеживания прогресса
- [x] Создана папка `.credentials` для хранения токенов
- [x] Получен Telegram Bot API Token от пользователя
- [x] Получен GitHub Personal Access Token (срок до 09.12.2025)
- [x] Создан репозиторий на GitHub: https://github.com/damaevbagdat/Jarvis-assistant
- [x] Подключен remote origin к локальному репозиторию
- [x] Создан файл `.gitignore` для защиты секретных данных
- [x] Токены сохранены в `.credentials/TOKENS.md`
- [x] Получен workflow "paraplexity 3.0" из n8n
- [x] Workflow сохранен в `workflows/paraplexity-3.0.json`
- [x] Проанализирована структура workflow и все компоненты
- [x] Создана документация workflow в `workflows/README.md`
- [x] Обновлен файл токенов с найденными API ключами

---

## Текущие задачи

- [ ] Проверить работоспособность всех API ключей в n8n
- [ ] Протестировать workflow в n8n
- [ ] Проверить настройки Supabase и PostgreSQL
- [ ] Убедиться, что Google Drive integration работает
- [ ] Протестировать бота в Telegram
- [ ] Документировать проблемы (если есть)

---

## Необходимые доступы

### Telegram Bot ✅
- **Имя бота:** Baga_assistant_bot
- **Username:** @Baga_assistant_bot
- **Token:** Сохранен в `.credentials/TOKENS.md`
- **Статус:** Получен и сохранен

### GitHub Repository ✅
- **Название:** Jarvis-assistant
- **URL:** https://github.com/damaevbagdat/Jarvis-assistant
- **Описание:** Telegram bot assistant with n8n integration
- **Статус:** Создан и подключен

### n8n ✅
- **Instance URL:** https://n8n.kir-ito.ru/
- **Workflow:** paraplexity 3.0 (экспортирован)
- **Timezone:** Asia/Almaty
- **Статус:** Workflow проанализирован

### API Services (требуют проверки)
- ⚠️ **OpenAI/OpenRouter** - для AI функций
- ⚠️ **Google Gemini** - основная языковая модель
- ⚠️ **Supabase** - векторная база знаний
- ⚠️ **PostgreSQL** - память разговоров
- ⚠️ **Google Drive** - загрузка документов для обучения
- ⚠️ **Cohere** - reranking результатов
- ✅ **ConvertAPI** - конвертация документов (ключ найден)
- ✅ **Google Custom Search** - веб-поиск (ключ найден)

---

## Заметки

### Возможности бота (из анализа workflow):

**Обработка входящих данных:**
- Текстовые сообщения
- Голосовые сообщения (транскрипция через Whisper)
- Изображения (анализ через GPT-4o-mini)
- Документы: PDF, Word, Excel, JSON, XML

**AI функции:**
- RAG (Retrieval-Augmented Generation) через Supabase
- Память разговоров через PostgreSQL
- Веб-поиск через Google Custom Search
- Работа с датой/временем
- Semantic reranking через Cohere

**Личность:** "Джарвис" - высокоинтеллектуальный персональный AI-ассистент

### Что нужно доделать:
1. Проверить все credentials в n8n
2. Убедиться, что база знаний загружена в Supabase
3. Протестировать все функции бота
4. Документировать любые проблемы
5. Возможно, нужно обновить некоторые API ключи
