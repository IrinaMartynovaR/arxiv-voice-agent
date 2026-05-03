import logging
from tempfile import NamedTemporaryFile
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.agent.service import AgentService, get_agent_service
from app.asr.base import AsrService
from app.asr.service import get_asr_service
from app.backend.schemas import ChatRequest, ChatResponse, HealthResponse, VoiceResponse
from app.utils.errors import ServiceUnavailableError
from app.utils.files import get_suffix

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
    try:
        with NamedTemporaryFile(delete=True, suffix=get_suffix(file.filename)) as audio_file:
            audio_file.write(await file.read())
            audio_file.flush()
            question = await asr.transcribe(audio_file.name)
    except ServiceUnavailableError as exc:
        logger.exception("ASR service is unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    logger.info("Voice question transcribed", extra={"question_length": len(question)})
    result = await agent.ask(question)
    return VoiceResponse(question=question, **result.model_dump())
