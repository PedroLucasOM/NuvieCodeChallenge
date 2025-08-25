from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Nuvie Backend Challenge",
    description="Sistema para gerenciamento de dados de pacientes com integração Synthea",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    from app.presentation.controllers import patient_controller, auth_controller
    app.include_router(auth_controller.router, prefix="/auth", tags=["authentication"])
    app.include_router(patient_controller.router, prefix="/patients", tags=["patients"])

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
