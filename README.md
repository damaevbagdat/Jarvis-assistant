# Jarvis Assistant Bot

Продвинутый AI-ассистент в Telegram с мультимодальными возможностями и RAG (Retrieval-Augmented Generation).

## Описание

**Джарвис** (@Baga_assistant_bot) - высокоинтеллектуальный персональный AI-ассистент, способный обрабатывать текст, голос, изображения и документы. Использует n8n для оркестрации и векторную базу знаний для точных ответов.

## ✨ Возможности

### 📥 Обработка входящих данных
- 💬 **Текстовые сообщения** - естественное общение
- 🎤 **Голосовые сообщения** - распознавание через Whisper API
- 🖼️ **Изображения** - анализ через GPT-4o-mini
- 📄 **Документы** - PDF, Word, Excel, JSON, XML

### 🧠 AI возможности
- **RAG** - векторная база знаний через Supabase
- **Память разговоров** - контекст через PostgreSQL
- **Веб-поиск** - актуальная информация через Google
- **Semantic Search** - улучшенная релевантность с Cohere

## 🚀 Быстрый старт

**Минимальная настройка (~10 минут):**

Следуйте инструкциям в [QUICK_START.md](QUICK_START.md)

**Полная настройка (~30 минут):**

Подробный чек-лист в [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)

## 📚 Документация

- **[QUICK_START.md](QUICK_START.md)** - Быстрый запуск за 10 минут
- **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Полный чек-лист настройки
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Диагностика и исправление проблем
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - Результаты тестирования
- **[workflows/README.md](workflows/README.md)** - Документация n8n workflow
- **[WORK_LOG.md](WORK_LOG.md)** - История разработки
- **[.credentials/TOKENS.md](.credentials/TOKENS.md)** - API ключи (не в git)

## 🏗️ Технологии

- **Telegram Bot API** - основа бота
- **n8n** - оркестрация workflow
- **Google Gemini** - основная языковая модель
- **OpenAI/OpenRouter** - Whisper, GPT-4o-mini, embeddings
- **Supabase** - векторная база знаний
- **PostgreSQL** - память разговоров
- **Cohere** - reranking результатов
- **Google Custom Search** - веб-поиск
- **ConvertAPI** - конвертация документов

## 📁 Структура проекта

```
Jarvis-assistant/
├── .credentials/              # Токены и API ключи (не в git)
│   └── TOKENS.md             # Все credentials проекта
├── workflows/                 # n8n workflows
│   ├── paraplexity-3.0.json  # Основной workflow
│   └── README.md             # Документация workflow
├── .gitignore                # Исключения git
├── README.md                 # Этот файл
├── QUICK_START.md            # Быстрый старт
├── SETUP_CHECKLIST.md        # Полный чек-лист
└── WORK_LOG.md               # История разработки
```

## 🎯 Архитектура

```
Пользователь (Telegram)
    ↓
Telegram Bot API
    ↓
n8n Workflow
    ├─→ Обработка текста → AI Agent
    ├─→ Whisper API → Транскрипция → AI Agent
    ├─→ GPT-4o-mini → Анализ изображения → AI Agent
    └─→ Extract & Parse → Документы → AI Agent
         ↓
    AI Agent (Google Gemini)
         ├─→ Supabase Vector Store (RAG)
         ├─→ Google Custom Search (Веб)
         ├─→ PostgreSQL (Память)
         └─→ Cohere (Reranking)
         ↓
    Ответ пользователю
```

## 🔧 Требования

### Обязательные (для базовой работы):
- n8n instance (https://n8n.kir-ito.ru/)
- Telegram Bot Token ✅
- Google Gemini API ⚠️
- Supabase account ⚠️

### Опциональные (для полной функциональности):
- OpenAI/OpenRouter API (голос, изображения)
- PostgreSQL (память разговоров)
- Google Drive API (загрузка базы знаний)
- Cohere API (улучшение поиска)

## 🔐 Безопасность

⚠️ **ВАЖНО:**
- Никогда не коммитьте файлы из `.credentials/` в git
- Не публикуйте API ключи
- Регулярно ротируйте токены
- GitHub PAT истекает 09.12.2025 - обновите заранее

## 📊 Статус проекта

**Текущая готовность:** 60% ✅

### ✅ Что работает:
- Базовая текстовая коммуникация
- Идентичность бота как "Джарвис"
- Google Gemini API (основная LLM)
- Supabase векторная база знаний (RAG)
- Веб-поиск через Google Custom Search
- n8n Workflow активен и стабилен

### ❌ Известные проблемы:
- **Память разговоров** - не работает (PostgreSQL credentials)
- **Анализ изображений** - не работает (OpenRouter API)
- **ConvertAPI** - невалидный ключ для Word документов

### 🔧 Исправление проблем:

**⚡ САМОЕ БЫСТРОЕ (5 минут, готовые параметры):** [FINAL_FIX.md](FINAL_FIX.md)
**🚀 Подробная инструкция (25 минут):** [FIX_STEP_BY_STEP.md](FIX_STEP_BY_STEP.md)
**💨 Экспресс-вариант (2 минуты):** [QUICK_FIX.md](QUICK_FIX.md)

📖 Подробное руководство: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
📊 Результаты тестирования: [TEST_RESULTS.md](TEST_RESULTS.md)
📝 История разработки: [WORK_LOG.md](WORK_LOG.md)

## Автор

**damaevbagdat** - [GitHub](https://github.com/damaevbagdat)

## Лицензия

> Будет добавлено позже

---

**Создано:** 2025-11-10
**Обновлено:** 2025-11-12
