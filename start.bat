@echo off
echo Starting Nuvie Backend Challenge...

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Copiar arquivo de ambiente se não existir
if not exist .env (
    echo Copying environment configuration file...
    copy .env.example .env
    echo .env file created. Configure variables as needed.
)

REM Iniciar serviços
echo Starting Docker containers...
docker-compose up -d

REM Aguardar serviços ficarem prontos
echo Waiting for database to initialize...
timeout /t 15 /nobreak >nul

REM Executar migrations
echo Running database migrations...
docker-compose exec -T api alembic upgrade head
if errorlevel 1 (
    echo Warning: Failed to run migrations. Retrying...
    timeout /t 5 /nobreak >nul
    docker-compose exec -T api alembic upgrade head
)

REM Verificar health check
echo Checking application status...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo Failed to start application. Check logs:
    echo    docker-compose logs api
) else (
    echo Application is running!
    echo.
    echo Available URLs:
    echo    API: http://localhost:8000
    echo    Docs: http://localhost:8000/docs
    echo    Health: http://localhost:8000/health
    echo.
    echo To view logs: docker-compose logs -f api
    echo To stop: docker-compose down
)

pause
