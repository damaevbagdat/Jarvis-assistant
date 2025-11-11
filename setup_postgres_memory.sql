-- =====================================================
-- Jarvis Assistant - PostgreSQL Chat Memory Setup
-- =====================================================
-- Этот скрипт создает таблицу для хранения памяти разговоров
-- Используется n8n Postgres Chat Memory node
--
-- Как использовать:
-- 1. Откройте Supabase Dashboard → SQL Editor
-- 2. Или подключитесь к вашей PostgreSQL базе
-- 3. Скопируйте и выполните этот скрипт
-- =====================================================

-- Создание таблицы для chat memory
CREATE TABLE IF NOT EXISTS n8n_chat_histories (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индекс для быстрого поиска по session_id
CREATE INDEX IF NOT EXISTS idx_session_id
ON n8n_chat_histories(session_id);

-- Индекс для сортировки по времени
CREATE INDEX IF NOT EXISTS idx_created_at
ON n8n_chat_histories(created_at DESC);

-- Комментарии к таблице и полям
COMMENT ON TABLE n8n_chat_histories IS 'Хранение истории разговоров для Jarvis Assistant Bot';
COMMENT ON COLUMN n8n_chat_histories.id IS 'Уникальный ID записи';
COMMENT ON COLUMN n8n_chat_histories.session_id IS 'ID сессии (chat.id из Telegram)';
COMMENT ON COLUMN n8n_chat_histories.type IS 'Тип сообщения: human или ai';
COMMENT ON COLUMN n8n_chat_histories.content IS 'Содержимое сообщения';
COMMENT ON COLUMN n8n_chat_histories.created_at IS 'Время создания записи';

-- Проверка: показать структуру таблицы
\d n8n_chat_histories

-- Проверка: показать все индексы
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'n8n_chat_histories';

-- Готово!
SELECT 'Таблица n8n_chat_histories успешно создана!' AS status;
