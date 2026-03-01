"""FastAPI REST API."""

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.core.skill_manager import SkillManager, SkillNotFoundError
from src.models.model_manager import ModelManager

app = FastAPI(title="Magic Skills API", version="1.0.0")

# Initialize managers
skill_manager = SkillManager()
skill_manager.load_all_skills()
model_manager = ModelManager()


class ExecuteRequest(BaseModel):
    """Execute skill request."""
    skill_name: str
    params: Dict[str, Any] = {}
    context: Optional[Dict[str, Any]] = None


class ExecuteResponse(BaseModel):
    """Execute skill response."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class SkillInfo(BaseModel):
    """Skill information."""
    name: str
    description: str
    category: str
    version: str


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/skills/list", response_model=List[SkillInfo])
async def list_skills(category: Optional[str] = None):
    """List all available skills."""
    skills = skill_manager.list_skills(category)
    return [SkillInfo(**skill) for skill in skills]


@app.post("/api/skills/execute", response_model=ExecuteResponse)
async def execute_skill(request: ExecuteRequest):
    """Execute a skill."""
    try:
        result = skill_manager.execute_skill(
            request.skill_name,
            request.params,
            request.context
        )
        return ExecuteResponse(
            success=result.success,
            data=result.data,
            error=result.error,
            execution_time_ms=result.execution_time_ms,
        )
    except SkillNotFoundError:
        raise HTTPException(status_code=404, detail=f"Skill not found: {request.skill_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skills/{skill_name}")
async def get_skill_info(skill_name: str):
    """Get skill information."""
    skill = skill_manager.get_skill(skill_name)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")

    return {
        "name": skill.config.name,
        "description": skill.config.description,
        "version": skill.config.version,
        "category": skill.config.category,
        "author": skill.config.author,
        "tags": skill.config.tags,
        "parameters": skill.config.parameters,
    }


@app.get("/api/models/list")
async def list_models():
    """List available LLM models."""
    return {
        "providers": model_manager.list_providers(),
    }


@app.get("/api/models/{provider}/models")
async def list_provider_models(provider: str):
    """List models for a provider."""
    try:
        models = model_manager.list_models(provider)
        return {"provider": provider, "models": models}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
