from typing import Dict

from fastapi import APIRouter, HTTPException

home_route = APIRouter()


@home_route.get(
    "/health",
    response_model=Dict[str, str],
    summary="Health check endpoint",
    description="Returns service health status"
)
async def health_check() -> Dict[str, str]:
    try:
        # Add actual health checks here
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable"
        )