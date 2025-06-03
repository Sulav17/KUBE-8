from fastapi import FastAPI
from routers import kubernetes_router, openai_router

app = FastAPI(title="Kubernetes GPT Assistant API")

app.include_router(kubernetes_router.router, prefix="/api", tags=["Kubernetes"])
app.include_router(openai_router.router, prefix="/api", tags=["OpenAI"])
