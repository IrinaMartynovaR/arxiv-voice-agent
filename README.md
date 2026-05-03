# arXiv Voice Agent

Модульный агент на LangGraph для поиска статей на arXiv. Вопрос можно отправить текстом
или голосом через ASR.

## Архитектура

```text
main.py
app/
  backend/      # FastAPI app, routes, schemas
  settings/     # конфигурация и логирование
  utils/        # общие утилиты
  agent/        # фасад агента
  graph/        # LangGraph state, nodes, builder
  tools/        # инструменты агента
  asr/          # интерфейс и реализации ASR
tests/
```

## Запуск

```bash
uv sync
uv run uvicorn main:app --reload
```

С голосовым вводом:

```bash
uv sync --extra asr
uv run uvicorn main:app --reload
```

## API

- `GET /health` — проверка backend.
- `POST /api/chat` — текстовый вопрос.
- `POST /api/voice` — аудиофайл с вопросом.

