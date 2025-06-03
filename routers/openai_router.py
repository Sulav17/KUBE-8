# openai_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.openai_handler import get_kubectl_command
from utils.kube_executor import execute_kubectl_command

router = APIRouter()

class TranslateRequest(BaseModel):
    context: str
    prompt: str

class ExecuteRequest(BaseModel):
    context: str
    command: str

@router.post("/translate")
async def translate(req: TranslateRequest):
    try:
        command = get_kubectl_command(req.prompt, req.context)
        # Do NOT execute yet. Return the command to the frontend/client.
        return {"translated_command": f"{command}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute(req: ExecuteRequest):
    try:
        output = execute_kubectl_command(req.command)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
