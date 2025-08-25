@echo off
echo 🚀 Iniciando Nuvie Backend Challenge...

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está rodando. Por favor, inicie o Docker primeiro.
    pause
    exit /b 1
)

REM Copiar arquivo de ambiente se não existir
if not exist .env (
    echo 📋 Copiando arquivo de configuração...
    copy .env.example .env
    echo ✅ Arquivo .env criado. Configure as variáveis conforme necessário.
)

REM Iniciar serviços
echo 🐳 Iniciando containers Docker...
docker-compose up -d

REM Aguardar serviços ficarem prontos
echo ⏳ Aguardando serviços iniciarem...
timeout /t 10 /nobreak >nul

REM Verificar health check
echo 🔍 Verificando status da aplicação...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Falha ao iniciar a aplicação. Verifique os logs:
    echo    docker-compose logs api
) else (
    echo ✅ Aplicação está rodando!
    echo.
    echo 📊 URLs disponíveis:
    echo    API: http://localhost:8000
    echo    Docs: http://localhost:8000/docs
    echo    Health: http://localhost:8000/health
    echo.
    echo 📝 Para ver logs: docker-compose logs -f api
    echo 🛑 Para parar: docker-compose down
)

pause
