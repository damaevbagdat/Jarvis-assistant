# ⚡ Быстрое исправление (2 минуты)

## 🔴 Память разговоров (1 минута)

### 1. Supabase - создать таблицу

**Открой:** https://supabase.com/dashboard → твой проект → SQL Editor → New query

**Скопируй и вставь (Ctrl+V):**
```sql
CREATE TABLE IF NOT EXISTS n8n_chat_histories (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_session_id ON n8n_chat_histories(session_id);
```

**Нажми:** RUN

---

### 2. Supabase - скопировать параметры

**Открой:** Settings → Database

**Скопируй эти значения** (понадобятся в следующем шаге):
```
Host: [скопируй db.xxxxxxxxxxxx.supabase.co]
Password: [скопируй пароль который задавал при создании проекта]
```

---

### 3. n8n - настроить credential

**Открой:** https://n8n.kir-ito.ru/ → Settings → Credentials

**Найди:** "Postgres account" (или поиск по ID: `P8hk2UZbE9YDsHIB`)

**Вставь параметры из Supabase:**
```
Host: [вставь из шага 2]
Database: postgres
User: postgres
Password: [вставь из шага 2]
Port: 5432
SSL: require  ← ВАЖНО! Выбери "require"
```

**Нажми:** Test connection → Save

✅ **Память готова!**

---

## 🔴 Анализ изображений (1 минута)

### 1. OpenRouter - получить API key

**Если НЕТ аккаунта:**
- Открой: https://openrouter.ai/auth/register
- Зарегистрируйся
- Add credits: минимум $5

**Если ЕСТЬ аккаунт:**
- Открой: https://openrouter.ai/keys
- Создай новый ключ или скопируй существующий

**Скопируй ключ:** `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx`

---

### 2. n8n - обновить credential

**Открой:** https://n8n.kir-ito.ru/ → Settings → Credentials

**Найди:** "OpenRouter" (или поиск по ID: `z0vBSqt6SlKhroIR`)

**Вставь API Key:**
```
[вставь ключ из шага 1]
```

**Нажми:** Save

✅ **Изображения готовы!**

---

## 🧪 Тест (30 секунд)

**Открой Telegram:** @Baga_assistant_bot

**Тест памяти:**
```
Меня зовут Багдат
```
Подожди ответ, потом:
```
Как меня зовут?
```
✅ Должен ответить с твоим именем

**Тест изображений:**
Отправь любое фото

✅ Должен описать содержимое

---

## 🆘 Если не работает

**Память:**
- n8n → Executions → последний запуск → проверь узел "Postgres Chat Memory"
- Supabase → Table Editor → должна быть таблица `n8n_chat_histories`

**Изображения:**
- n8n → Executions → последний запуск → проверь узел "Photo to text"
- OpenRouter → https://openrouter.ai/activity → проверь логи

---

**Готово!** Бот теперь работает на 100% 🎉
