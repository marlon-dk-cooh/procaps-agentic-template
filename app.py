"""FastAPI wrapper para el demo del agente de plantilla.

Expone el grafo supervisor / subagente DeepAgents como puntos finales HTTP para que pueda
funcionar dentro de un contenedor desplegado a través de Azure Container Apps (ver Pipelines/main.yml).
"""

from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent-template-api")

# ---------------------------------------------------------------------------
# Agent – carga diferida en el arranque para que los errores de importación se manifiesten de inmediato
# ---------------------------------------------------------------------------
_agent: Any = None


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Build the LangGraph agent once on startup."""
    global _agent  # noqa: PLW0603
    logger.info("⏳ Loading agent graph …")

    from agents.demo_agent import agent_template_demo  # heavy import

    _agent = agent_template_demo
    logger.info("✅ Agent graph loaded successfully.")
    yield


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Deep-Agents Procaps Template",
    description=(
        "Supervisor no conversacional / subagente demo "
        "expuesto como una aplicación FastAPI."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Esquemas de respuesta.
# ---------------------------------------------------------------------------
class InvokeRequest(BaseModel):
    """Request body para POST /llamado."""

    message: str = Field(
        ...,
        min_length=1,
        description="La instrucción del usuario a enviar al agente supervisor.",
        json_schema_extra={
            "example": "Por favor procesa mi documento ubicado en /blabla/path/to/my_document.pdf"
        },
    )


class VirtualFile(BaseModel):
    path: str
    data: Any
    mime_type: str | None = None
    modified_at: str | None = None


class InvokeResponse(BaseModel):
    """Respuesta estructurada de una invocación del agente."""

    reply: str = Field(..., description="Respuesta final del agente supervisor.")
    files: list[VirtualFile] = Field(
        default_factory=list,
        description="Archivos virtuales producidos por las herramientas del agente.",
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health", tags=["ops"])
async def health_check():
    """Health check para Azure Container Apps."""
    return {"status": "healthy", "agent_loaded": _agent is not None}


@app.post("/invoke", response_model=InvokeResponse, tags=["agent"])
async def invoke_agent(body: InvokeRequest):
    """Invoca el demo agent con el mensaje proporcionado y devuelve los resultados.

    El agente es no conversacional: recibe una sola instrucción,
    orquesta el flujo supervisor → subagente y devuelve los artefactos virtuales generados
    junto con la respuesta final del LLM.
    """

    if _agent is None:
        raise HTTPException(status_code=503, detail="Agent graph not loaded yet.")

    initial_state = {
        "messages": [HumanMessage(content=body.message)],
    }

    logger.info("🚀 Invoking agent with message: %s", body.message[:120])

    try:
        final_state = _agent.invoke(initial_state)
    except Exception as exc:
        logger.exception("Agent invocation failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    raw_files: dict[str, Any] = final_state.get("files", {})
    virtual_files = [
        VirtualFile(
            path=path,
            data=artifact.get("data"),
            mime_type=artifact.get("mime_type"),
            modified_at=artifact.get("modified_at"),
        )
        for path, artifact in raw_files.items()
    ]

    messages = final_state.get("messages", [])
    reply = messages[-1].content if messages else "No response generated."

    logger.info("✅ Agent finished – %d virtual file(s) produced.", len(virtual_files))

    return InvokeResponse(reply=reply, files=virtual_files)
