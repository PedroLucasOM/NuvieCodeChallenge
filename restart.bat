@echo off
echo 🔄 Reconstruindo aplicação com novas dependências...

echo 📦 Parando e removendo containers...
docker-compose down --volumes

echo 🧹 Limpando imagens e cache...
docker system prune -f
docker rmi nuvie-backend-challenge-api 2>nul

echo 🔨 Reconstruindo com --no-cache...
docker-compose build --no-cache

echo 🚀 Iniciando containers...
docker-compose up -d

echo ⏳ Aguardando aplicação inicializar...
timeout /t 20 /nobreak >nul

echo 🔍 Verificando status...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Aplicação ainda não está respondendo
    echo 📋 Verificando logs dos últimos 30 segundos:
    docker-compose logs --tail=50 api
) else (
    echo ✅ Aplicação funcionando!
    echo.
    echo 📊 URLs disponíveis:
    echo    🏠 Home: http://localhost:8000
    echo    📖 Docs: http://localhost:8000/docs
    echo    ❤️  Health: http://localhost:8000/health
    echo    📊 Metrics: http://localhost:8000/metrics
    echo.
    echo 📝 Para monitorar logs: docker-compose logs -f api
)

pause
