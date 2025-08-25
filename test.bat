@echo off
echo Running Nuvie Backend Challenge Tests...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if containers are running
echo Checking if application containers are running...
docker-compose ps | findstr "Up" >nul
if errorlevel 1 (
    echo Application containers are not running. Starting them first...
    docker-compose up -d
    echo Waiting for services to be ready...
    timeout /t 15 /nobreak >nul
    
    REM Run migrations
    echo Running database migrations...
    docker-compose exec -T api alembic upgrade head
)

REM Install test dependencies if not already installed
echo Installing test dependencies...
docker-compose exec -T api pip install pytest-cov coverage pytest-html

REM Run tests with coverage
echo.
echo Running unit tests with coverage...
docker-compose exec -T api pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing --html=reports/test_report.html --self-contained-html

REM Check test results
if errorlevel 1 (
    echo.
    echo Tests failed! Check the output above for details.
    echo.
    echo To view detailed test report: docker-compose exec api cat reports/test_report.html
) else (
    echo.
    echo All tests passed successfully!
    echo.
    echo Coverage report generated in htmlcov/ directory
    echo Test report generated as reports/test_report.html
)

REM Copy reports to host
echo.
echo Copying test reports to host...
docker-compose exec -T api mkdir -p /app/reports
docker cp $(docker-compose ps -q api):/app/htmlcov ./test_coverage 2>nul
docker cp $(docker-compose ps -q api):/app/reports ./test_reports 2>nul

echo.
echo Test execution completed.
echo.
echo Available reports:
echo   Coverage Report: test_coverage/index.html
echo   Test Report: test_reports/test_report.html
echo.
echo To run specific tests: docker-compose exec api pytest tests/test_auth.py -v
echo To run tests with specific pattern: docker-compose exec api pytest tests/ -k "test_create" -v

pause
