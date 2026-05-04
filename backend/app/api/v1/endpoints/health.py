from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
async def healthcheck(request: Request) -> dict[str, str]:
    db_ready = bool(getattr(request.app.state, "db_ready", False))
    return {
        "status": "ok" if db_ready else "degraded",
        "database": "connected" if db_ready else "unavailable",
    }
