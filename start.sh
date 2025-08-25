#!/bin/bash

echo "🚀 Iniciando Nuvie Backend Challenge..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Copiar arquivo de ambiente se não existir
if [ ! -f .env ]; then
    echo "📋 Copiando arquivo de configuração..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Configure as variáveis conforme necessário."
fi

# Iniciar serviços
echo "🐳 Iniciando containers Docker..."
docker-compose up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços iniciarem..."
sleep 10

# Verificar health check
echo "🔍 Verificando status da aplicação..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Aplicação está rodando!"
    echo ""
    echo "📊 URLs disponíveis:"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo "   Health: http://localhost:8000/health"
    echo ""
    echo "📝 Para ver logs: docker-compose logs -f api"
    echo "🛑 Para parar: docker-compose down"
else
    echo "❌ Falha ao iniciar a aplicação. Verifique os logs:"
    echo "   docker-compose logs api"
fi
