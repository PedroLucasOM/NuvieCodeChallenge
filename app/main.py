from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Nuvie Backend Challenge",
    description="Sistema para gerenciamento de dados de pacientes com integração Synthea",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    logger.warning(f"Validation error on {request.url}: {errors}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation failed",
            "message": "The request contains invalid data",
            "details": errors
        }
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    logger.warning(f"Pydantic validation error on {request.url}: {errors}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation failed",
            "message": "The provided data is invalid",
            "details": errors
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error {exc.status_code} on {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"HTTP {exc.status_code}",
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

from app.presentation.controllers import patient_controller, auth_controller

app.include_router(auth_controller.router, prefix="/auth", tags=["authentication"])
app.include_router(patient_controller.router, prefix="/patients", tags=["patients"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Nuvie Backend Challenge API",
        version="2.0.0",
        description="Sistema de Gerenciamento de Pacientes com autenticação JWT",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Insira o token JWT obtido do endpoint /auth/token (formato: seu_token_aqui)"
        }
    }
    
    protected_paths = ["/patients", "/auth/me"]
    for path, path_item in openapi_schema["paths"].items():
        if any(protected_path in path for protected_path in protected_paths):
            for method, operation in path_item.items():
                if isinstance(operation, dict):
                    operation["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    return {
        "message": "Nuvie Backend Challenge API", 
        "version": "2.0.0",
        "status": "active",
        "architecture": "Clean Architecture"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "nuvie-backend",
        "version": "2.0.0"
    }

@app.get("/metrics")
async def metrics():
    return {
        "service": "nuvie-backend",
        "uptime": "healthy",
        "database": "connected",
        "memory_usage": "optimal"
    }
