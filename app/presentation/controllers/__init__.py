from .patient_controller import router as patient_router
from .auth_controller import router as auth_router

__all__ = ["patient_router", "auth_router"]
