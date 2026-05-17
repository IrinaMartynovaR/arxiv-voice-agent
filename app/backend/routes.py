import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError

from app.agent.service import AgentService, get_agent_service
from app.asr.base import AsrService
from app.asr.service import get_asr_service
from app.backend.schemas import ChatRequest, ChatResponse, HealthResponse, VoiceResponse
from app.utils.errors import ServiceUnavailableError
from app.utils.files import get_suffix
from app.utils.temp_files import remove_file, write_bytes_to_temp_file

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Возвращает состояние сервиса.

    Returns:
        Статус backend.
    """
    return HealthResponse(status="ok")


@router.post("/api/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    agent: Annotated[AgentService, Depends(get_agent_service)],
) -> ChatResponse:
    """Обрабатывает текстовый вопрос пользователя.

    Args:
        payload: Тело запроса с вопросом.
        agent: Сервис агента.

    Returns:
        Ответ агента и найденные статьи.
    """
    result = await agent.ask(payload.question)
    return ChatResponse(**result.model_dump())


@router.post("/api/voice", response_model=VoiceResponse)
async def voice(
    file: Annotated[UploadFile, File()],
    agent: Annotated[AgentService, Depends(get_agent_service)],
    asr: Annotated[AsrService, Depends(get_asr_service)],
) -> VoiceResponse:
    """Обрабатывает голосовой вопрос пользователя.

    Args:
        file: Аудиофайл с вопросом.
        agent: Сервис агента.
        asr: Сервис распознавания речи.

    Returns:
        Распознанный вопрос, ответ агента и найденные статьи.
    """
    audio_path = write_bytes_to_temp_file(await file.read(), suffix=get_suffix(file.filename))
    try:
        question = await asr.transcribe(str(audio_path))
        question = ChatRequest(question=question).question
    except ServiceUnavailableError as exc:
        logger.exception("ASR service is unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except ValidationError as exc:
        logger.info("ASR returned blank question")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Voice question is empty",
        ) from exc
    finally:
        remove_file(audio_path)

    logger.info("Voice question transcribed", extra={"question_length": len(question)})
    result = await agent.ask(question)
    return VoiceResponse(question=question, **result.model_dump())
