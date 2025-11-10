# Диагностика и исправление проблем Jarvis Assistant Bot

**Дата создания:** 2025-11-11
**Статус бота:** 60% функциональности (базовые функции работают)

---

## 🔍 Обнаруженные проблемы

### ❌ Проблема 1: Память разговоров не работает
**Симптомы:**
- Бот не отвечает на вопрос "Как меня зовут?" после представления
- После "Меня зовут [имя]" → "Как меня зовут?" = нет ответа

**Узел в workflow:** `Postgres Chat Memory` (ID: ecd9f47a-8921-4b87-af83-d64baf5c81eb)
**Credential ID:** P8hk2UZbE9YDsHIB

---

### ❌ Проблема 2: Анализ изображений не работает
**Симптомы:**
- При отправке изображения боту → нет ответа
- Работает для текста, но не для фото

**Узлы в workflow:**
- `Photo to text` (для обычных фото) - ID: 2c68527d-1a1e-43c6-96ea-1a138d14e957
- `Photo to text1` (для изображений в документах) - ID: e677276c-5a22-4aad-95fa-ad495620cd95
**Credential ID:** z0vBSqt6SlKhroIR (OpenRouter)
**Модель:** gpt-4o-mini

---

## 🛠️ Решение проблемы 1: PostgreSQL Memory

### Шаг 1: Проверьте credentials PostgreSQL в n8n

1. Откройте n8n: https://n8n.kir-ito.ru/
2. Перейдите в `Settings` → `Credentials`
3. Найдите credential с ID `P8hk2UZbE9YDsHIB` (название: "Postgres account")
4. Нажмите на него для редактирования

**Проверьте следующие параметры:**

| Параметр | Что проверить |
|----------|---------------|
| **Host** | IP адрес или URL базы данных PostgreSQL |
| **Port** | Обычно `5432` для PostgreSQL |
| **Database** | Имя базы данных (например: `jarvis_db`, `n8n`, `postgres`) |
| **User** | Имя пользователя PostgreSQL |
| **Password** | Пароль для подключения |
| **SSL** | Если используется облачная БД (Supabase, AWS), включите SSL |

5. Нажмите кнопку **"Test connection"**
   - ✅ Если тест успешен → переходите к Шагу 2
   - ❌ Если ошибка → исправьте параметры

### Шаг 2: Создайте таблицу для памяти (если её нет)

PostgreSQL Chat Memory node требует специальную таблицу в БД.

**Вариант A: Использовать Supabase PostgreSQL**

Если у вас уже есть Supabase (он используется для векторной базы):

1. Откройте Supabase Dashboard: https://supabase.com/dashboard
2. Выберите ваш проект
3. Перейдите в `SQL Editor`
4. Выполните следующий SQL скрипт:

```sql
-- Создание таблицы для chat memory
CREATE TABLE IF NOT EXISTS n8n_chat_histories (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индекс для быстрого поиска по session_id
CREATE INDEX IF NOT EXISTS idx_session_id ON n8n_chat_histories(session_id);
```

5. После выполнения проверьте в `Table Editor` → должна появиться таблица `n8n_chat_histories`

**Параметры для n8n Postgres credential (Supabase):**
- **Host:** Найдите в Supabase: Settings → Database → Host
- **Port:** `5432`
- **Database:** `postgres`
- **User:** `postgres`
- **Password:** Найдите в Supabase: Settings → Database → Database password
- **SSL:** Включить (Required)

**Вариант B: Использовать бесплатную PostgreSQL базу**

Если нет Supabase PostgreSQL или хотите отдельную базу:

1. Создайте бесплатный аккаунт на: https://neon.tech/ (бесплатно, 0.5GB)
   - Или: https://supabase.com/ (можно использовать тот же аккаунт)
   - Или: https://railway.app/ (бесплатный план)

2. После создания БД получите connection string и создайте таблицу (SQL выше)

### Шаг 3: Обновите credential в n8n

1. В n8n → Settings → Credentials → Postgres account (ID: P8hk2UZbE9YDsHIB)
2. Введите параметры подключения из Шага 2
3. Нажмите **"Test connection"** → должно быть ✅ Success
4. Сохраните

### Шаг 4: Проверьте узел Postgres Chat Memory в workflow

1. Откройте workflow: https://n8n.kir-ito.ru/workflow/Su2pdOFjSWUUdlLI
2. Найдите узел `Postgres Chat Memory`
3. Убедитесь, что выбран правильный credential
4. Проверьте параметры:
   - **Session ID Type:** `Custom Key`
   - **Session Key:** `={{ $('Telegram Trigger').item.json.message.chat.id }}`
   - **Context Window Length:** `3` (можно увеличить до 10 для лучшей памяти)

### Шаг 5: Протестируйте память

1. Отправьте боту: `Меня зовут Тестовый Пользователь`
2. Подождите ответа
3. Отправьте: `Как меня зовут?`
4. Бот должен ответить с упоминанием имени

**Если всё ещё не работает:**

Проверьте логи в n8n:
1. n8n → Executions → найдите последние запуски
2. Откройте execution с вашим вопросом о памяти
3. Проверьте узел `Postgres Chat Memory` на наличие ошибок
4. Если есть ошибка SQL или connection → проверьте credentials ещё раз

### Альтернативное решение: Window Buffer Memory

Если PostgreSQL не работает, можно временно использовать простую память:

1. В workflow найдите узел `Postgres Chat Memory`
2. Удалите связь между `Postgres Chat Memory` → `Knowledge Base AI Agent`
3. Добавьте новый узел: `Window Buffer Memory`
4. Настройте:
   - **Session Key:** `={{ $('Telegram Trigger').item.json.message.chat.id }}`
   - **Context Window Length:** `5`
5. Подключите к `Knowledge Base AI Agent` через `ai_memory` вход

**Недостаток:** Память не сохраняется между перезапусками n8n, только во время сессии.

---

## 🛠️ Решение проблемы 2: OpenRouter Image Analysis

### Шаг 1: Проверьте OpenRouter API credentials

1. Откройте n8n: https://n8n.kir-ito.ru/
2. Перейдите в `Settings` → `Credentials`
3. Найдите credential с ID `z0vBSqt6SlKhroIR` (название: "OpenRouter")
4. Нажмите для редактирования

**Проверьте:**
- ✅ API Key заполнен
- ✅ Нет сообщений об ошибке

### Шаг 2: Проверьте баланс и доступность модели

1. Откройте OpenRouter Dashboard: https://openrouter.ai/
2. Войдите в свой аккаунт
3. Перейдите в `Credits` или `Usage`

**Проверьте:**
- Есть ли доступные кредиты?
- Модель `gpt-4o-mini` доступна в вашем плане?

**Если кредиты закончились:**
1. Пополните баланс: https://openrouter.ai/credits
2. Минимум: $5 (хватит на ~500-1000 запросов с изображениями)

**Если нет OpenRouter аккаунта:**
1. Создайте: https://openrouter.ai/auth/register
2. Добавьте способ оплаты
3. Пополните баланс ($5-$10)
4. Получите API Key: https://openrouter.ai/keys

### Шаг 3: Обновите API Key в n8n

1. Скопируйте новый API Key из OpenRouter
2. В n8n → Settings → Credentials → OpenRouter (ID: z0vBSqt6SlKhroIR)
3. Вставьте API Key
4. Сохраните

### Шаг 4: Проверьте узлы анализа изображений

Откройте workflow и проверьте оба узла:

**Узел 1: `Photo to text`** (для обычных фото)
1. Параметры:
   - **Resource:** `image`
   - **Operation:** `analyze`
   - **Model:** `gpt-4o-mini`
   - **Text:** "Describe the contents of this photo/image"
   - **Credentials:** OpenRouter (z0vBSqt6SlKhroIR)

**Узел 2: `Photo to text1`** (для изображений в документах)
1. Те же параметры

### Шаг 5: Проверьте workflow execution

1. Отправьте изображение боту в Telegram
2. В n8n → Executions → найдите последний запуск
3. Откройте execution
4. Найдите узлы:
   - `Download Photo` или `Download Image`
   - `Fix mimeType` или `Fix mimeType1`
   - `Photo to text` или `Photo to text1`

**Что искать:**
- ❌ Если узел `Download Photo` завершился с ошибкой → проблема с Telegram API
- ❌ Если узел `Photo to text` завершился с ошибкой → смотрите текст ошибки:
  - `401 Unauthorized` → неверный API key
  - `402 Payment Required` → кредиты закончились
  - `429 Too Many Requests` → превышен лимит запросов
  - `Model not found` → модель недоступна

### Шаг 6: Тестирование

1. Отправьте боту простое изображение (например, скриншот или фото)
2. Подождите 10-15 секунд (анализ изображений медленнее текста)
3. Бот должен ответить с описанием изображения

**Если всё ещё не работает:**

Проверьте альтернативные причины:

**A. Проблема с mimeType:**
- Узлы `Fix mimeType` и `Fix mimeType1` исправляют MIME type для изображений
- Если изображение не в формате .jpg, .jpeg, .png, .webp, .gif → может быть ошибка

**B. Проблема с размером изображения:**
- OpenRouter может отклонять очень большие изображения
- Telegram автоматически сжимает, но проверьте размер файла

**C. Workflow не дошёл до узла:**
- Проверьте в Executions, прошёл ли workflow через `Input Message Router` → `Photo` output
- Если нет → проблема в роутинге сообщений

### Альтернативное решение: OpenAI напрямую

Если OpenRouter не работает, можно использовать OpenAI напрямую:

1. Получите OpenAI API Key: https://platform.openai.com/api-keys
2. Создайте новый credential в n8n: `OpenAI account`
3. В узлах `Photo to text` и `Photo to text1` замените credential на OpenAI
4. Модель останется `gpt-4o-mini` (она есть у OpenAI)

**Стоимость OpenAI:**
- gpt-4o-mini: $0.00015 за 1K input tokens (изображение)
- ~$0.01-0.03 за одно изображение

---

## 📊 Диагностическая таблица

| Проблема | Вероятная причина | Решение |
|----------|------------------|---------|
| Память: нет ответа | PostgreSQL credentials невалидны | Шаг 1-3 (PostgreSQL) |
| Память: нет ответа | Таблица не создана | Шаг 2 (SQL скрипт) |
| Память: нет ответа | Workflow ошибка | Проверить Executions логи |
| Изображения: нет ответа | OpenRouter кредиты закончились | Пополнить баланс |
| Изображения: нет ответа | API key невалиден | Обновить credential |
| Изображения: нет ответа | Модель недоступна | Проверить OpenRouter dashboard |
| Изображения: нет ответа | Workflow ошибка | Проверить Executions логи |

---

## 🧪 Чек-лист финальной проверки

### PostgreSQL Memory
- [ ] Credential подключен и тест успешен
- [ ] Таблица `n8n_chat_histories` создана
- [ ] Узел `Postgres Chat Memory` использует правильный credential
- [ ] Тест: "Меня зовут X" → "Как меня зовут?" работает

### OpenRouter Images
- [ ] Credential содержит валидный API key
- [ ] Баланс кредитов > $0
- [ ] Модель `gpt-4o-mini` доступна
- [ ] Узлы `Photo to text` и `Photo to text1` используют правильный credential
- [ ] Тест: отправка изображения → бот описывает содержимое

---

## 📝 Логи и отладка

### Где смотреть логи:

**В n8n:**
1. Executions → выберите последний запуск
2. Каждый узел показывает:
   - ✅ Зелёная галочка = успешно
   - ❌ Красный крестик = ошибка
3. Кликните на узел с ошибкой → посмотрите JSON output и error message

**Telegram Bot:**
- Если бот вообще не отвечает → проверьте webhook: https://api.telegram.org/bot<TOKEN>/getWebhookInfo
- Pending updates должен быть 0

**OpenRouter:**
- Логи запросов: https://openrouter.ai/activity
- Там видно все запросы, ошибки и потраченные кредиты

**PostgreSQL:**
- Если используете Supabase: Table Editor → `n8n_chat_histories` → проверьте записи
- Должны появляться новые строки после каждого сообщения

---

## 🆘 Если ничего не помогло

1. **Проверьте статус сервисов:**
   - n8n: https://n8n.kir-ito.ru/
   - OpenRouter: https://status.openrouter.ai/
   - Supabase: https://status.supabase.com/

2. **Экспортируйте workflow и проверьте JSON:**
   - Workflow → ... → Download
   - Проверьте, что все credentials ID совпадают

3. **Пересоздайте проблемные узлы:**
   - Удалите узел `Postgres Chat Memory`
   - Создайте новый с нуля
   - Подключите заново

4. **Временно используйте альтернативы:**
   - Вместо PostgreSQL → Window Buffer Memory (встроенная)
   - Вместо OpenRouter → OpenAI напрямую

---

**Создано:** 2025-11-11
**Следующее обновление:** После исправления проблем
