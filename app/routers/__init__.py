from .auth import router as auth_router
from .patients import router as patients_router

__all__ = ["auth_router", "patients_router"]
