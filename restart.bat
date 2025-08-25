@echo off
echo Rebuilding application with new dependencies...

echo Stopping and removing containers...
docker-compose down --volumes

echo Cleaning images and cache...
docker system prune -f
docker rmi nuvie-backend-challenge-api 2>nul

echo Rebuilding with --no-cache...
docker-compose build --no-cache

echo Starting containers...
docker-compose up -d

echo Waiting for database to initialize...
timeout /t 15 /nobreak >nul

echo Running database migrations...
docker-compose exec -T api alembic upgrade head
if errorlevel 1 (
    echo Warning: Failed to run migrations. Retrying...
    timeout /t 5 /nobreak >nul
    docker-compose exec -T api alembic upgrade head
)

echo Waiting for application to initialize...
timeout /t 10 /nobreak >nul

echo Checking status...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo Application is not responding yet
    echo Checking logs from the last 30 seconds:
    docker-compose logs --tail=50 api
) else (
    echo Application is working!
    echo.
    echo Available URLs:
    echo    Home: http://localhost:8000
    echo    Docs: http://localhost:8000/docs
    echo    Health: http://localhost:8000/health
    echo    Metrics: http://localhost:8000/metrics
    echo.
    echo To monitor logs: docker-compose logs -f api
)

pause
