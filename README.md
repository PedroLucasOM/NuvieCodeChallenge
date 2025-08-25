# 🏥 Nuvie Backend Challenge - Sistema de Gerenciamento de Pacientes

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

---

## 🎯 ETAPA 1: OVERVIEW DA APLICAÇÃO

### 📋 Propósito da Aplicação
Sistema backend robusto e escalável para **gerenciamento completo de dados de pacientes** com integração à API Synthea para geração de dados sintéticos em formato FHIR. Desenvolvido seguindo as melhores práticas de arquitetura de software para ambientes hospitalares e de saúde.

### 🛠️ Stack Tecnológico

#### **Core Framework**
- **FastAPI 0.104.1** - Framework web moderno e de alta performance
- **Python 3.11** - Linguagem principal com type hints
- **Pydantic V2** - Validação de dados e serialização

#### **Banco de Dados & Cache**
- **PostgreSQL 15** - Banco de dados principal
- **SQLAlchemy 2.0 Async** - ORM assíncrono moderno
- **Redis 7** - Cache e gerenciamento de sessões
- **Alembic** - Migrations automáticas

#### **Segurança & Autenticação**
- **JWT (JSON Web Tokens)** - Autenticação stateless
- **bcrypt** - Hash seguro de senhas
- **CORS** - Configuração para APIs cross-origin

#### **Infraestrutura & Deploy**
- **Docker & Docker Compose** - Containerização completa
- **Nginx** - Reverse proxy para produção
- **Uvicorn** - Servidor ASGI de alta performance

#### **Testes & Qualidade**
- **pytest + pytest-asyncio** - Testes automatizados
- **Coverage** - Relatórios de cobertura
- **Type hints** - Tipagem estática completa

### 🏗️ Arquitetura Clean Architecture

```
📁 app/
├── 🏛️ domain/              # Camada de Domínio
│   ├── entities/           # Entidades de negócio (Patient, User)
│   └── interfaces.py       # Contratos e abstrações
├── 📊 application/         # Camada de Aplicação  
│   └── use_cases/          # Casos de uso e regras de negócio
├── 🔧 infrastructure/      # Camada de Infraestrutura
│   ├── repositories/       # Implementação de repositórios
│   └── external/           # Serviços externos (Synthea)
├── 🌐 presentation/        # Camada de Apresentação
│   ├── controllers/        # Controllers REST
│   └── dependencies.py     # Injeção de dependências
├── 📄 schemas/             # Schemas Pydantic (DTOs)
└── 🗄️ models/              # Models SQLAlchemy
```

### ⚡ Princípios SOLID Implementados

- **🔹 SRP** - Cada classe possui uma única responsabilidade
- **🔹 OCP** - Código aberto para extensão, fechado para modificação  
- **🔹 LSP** - Interfaces respeitam contratos de substituição
- **🔹 ISP** - Interfaces segregadas por responsabilidade
- **🔹 DIP** - Dependência de abstrações, não implementações

### 🚀 Funcionalidades Principais

#### **Gerenciamento de Pacientes**
- ✅ CRUD completo com validações robustas
- ✅ Busca avançada com múltiplos filtros
- ✅ Paginação otimizada para grandes volumes
- ✅ Validação de dados pessoais e médicos

#### **Sistema de Autenticação**
- ✅ Registro e login de usuários
- ✅ Autenticação JWT stateless
- ✅ Controle de acesso baseado em roles
- ✅ Sessões seguras com refresh tokens

#### **Integração Synthea FHIR**
- ✅ Consumo de dados sintéticos da API Synthea
- ✅ Transformação automática FHIR R4 → Modelo interno
- ✅ Importação batch com controle de duplicatas
- ✅ Mapeamento completo de recursos FHIR

### 🔐 Características de Segurança

- **🛡️ Autenticação JWT** com algoritmo HS256
- **🔒 Hash bcrypt** para senhas com salt
- **🌐 CORS** configurado para ambientes específicos
- **📝 Logs estruturados** para auditoria
- **🔍 Validação rigorosa** de todos os inputs
- **⚡ Rate limiting** por usuário

### ⚡ Performance & Escalabilidade

- **🚀 Operações assíncronas** com SQLAlchemy 2.0
- **💾 Cache Redis** para consultas frequentes  
- **📊 Connection pooling** otimizado
- **🔄 Paginação eficiente** para grandes datasets
- **📈 Métricas Prometheus** para monitoramento

---

## 🔗 ETAPA 2: ENDPOINTS E UTILIZAÇÃO

### 🔐 Autenticação e Autorização

#### **POST** `/auth/register` - Registrar novo usuário
```json
{
  "username": "usuario_exemplo",
  "email": "usuario@exemplo.com", 
  "password": "senha_segura_123",
  "full_name": "Nome Completo"
}
```
**Validações:**
- `username`: string, 3-50 caracteres, únicos
- `email`: formato de email válido, único
- `password`: mínimo 8 caracteres, alfanumérico
- `full_name`: opcional, máximo 200 caracteres

**Response 201:**
```json
{
  "id": 1,
  "username": "usuario_exemplo",
  "email": "usuario@exemplo.com",
  "full_name": "Nome Completo", 
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-08-25T10:00:00Z"
}
```

#### **POST** `/auth/token` - Login e obtenção de JWT
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario_exemplo&password=senha_segura_123"
```
**Validações:**
- `username`: obrigatório, deve existir no sistema
- `password`: obrigatório, deve corresponder ao hash

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### **GET** `/auth/me` - Dados do usuário logado
**Headers:** `Authorization: Bearer {token}`

**Response 200:**
```json
{
  "id": 1,
  "username": "usuario_exemplo",
  "email": "usuario@exemplo.com",
  "full_name": "Nome Completo",
  "is_active": true,
  "is_superuser": false
}
```

### 👥 Gerenciamento de Pacientes

#### **POST** `/patients/` - Criar novo paciente
**Headers:** `Authorization: Bearer {token}`
```json
{
  "first_name": "João",
  "last_name": "Silva", 
  "date_of_birth": "1990-01-15",
  "gender": "male",
  "ssn": "123-45-6789",
  "address": "Rua das Flores, 123",
  "city": "São Paulo",
  "state": "SP", 
  "zip_code": "01234-567",
  "phone": "+5511999999999",
  "email": "joao.silva@email.com",
  "race": "white",
  "ethnicity": "non-hispanic"
}
```
**Validações:**
- `first_name`: obrigatório, 1-100 caracteres
- `last_name`: obrigatório, 1-100 caracteres  
- `date_of_birth`: obrigatório, formato YYYY-MM-DD, não futuro
- `gender`: obrigatório, valores: male/female/other
- `ssn`: opcional, formato XXX-XX-XXXX, único
- `email`: opcional, formato válido de email
- `phone`: opcional, formato internacional

**Response 201:** Dados do paciente criado com ID

#### **GET** `/patients/` - Listar pacientes com filtros
**Headers:** `Authorization: Bearer {token}`

**Query Parameters:**
```bash
GET /patients/?search=joão&gender=male&city=são paulo&age_min=18&age_max=65&limit=10&offset=0
```

| Parâmetro | Tipo | Validação | Descrição |
|-----------|------|-----------|-----------|
| `search` | string | - | Busca em nome, email, SSN |
| `gender` | string | male/female/other | Filtro por gênero |
| `city` | string | - | Filtro por cidade (parcial) |
| `state` | string | - | Filtro por estado |
| `age_min` | int | 0-150 | Idade mínima |
| `age_max` | int | 0-150 | Idade máxima |
| `limit` | int | 1-1000 | Registros por página |
| `offset` | int | ≥0 | Registros para pular |

**Response 200:**
```json
[
  {
    "id": 1,
    "first_name": "João",
    "last_name": "Silva",
    "date_of_birth": "1990-01-15",
    "gender": "male",
    "age": 35,
    "email": "joao.silva@email.com",
    "created_at": "2025-08-25T10:00:00Z"
  }
]
```

#### **GET** `/patients/{id}` - Obter paciente específico
**Headers:** `Authorization: Bearer {token}`
**Validações:** `id` deve ser inteiro positivo existente

**Response 200:** Dados completos do paciente
**Response 404:** `{"detail": "Paciente não encontrado"}`

#### **PUT** `/patients/{id}` - Atualizar paciente
**Headers:** `Authorization: Bearer {token}`
**Body:** Mesmas validações do POST, todos os campos opcionais

**Response 200:** Dados atualizados do paciente
**Response 404:** Paciente não encontrado

#### **DELETE** `/patients/{id}` - Remover paciente  
**Headers:** `Authorization: Bearer {token}`

**Response 200:**
```json
{"message": "Paciente deletado com sucesso"}
```

### 🔄 Integração Synthea

#### **POST** `/patients/import-synthea` - Importar dados Synthea
**Headers:** `Authorization: Bearer {token}`

**Query Parameters:**
```bash
POST /patients/import-synthea?count=10
```
- `count`: int, 1-100, número de pacientes para importar

**Response 200:**
```json
{
  "message": "Importados 8 pacientes do Synthea com sucesso",
  "imported_count": 8,
  "total_processed": 10,
  "duplicates_skipped": 2
}
```

**Códigos de Erro:**
- **500:** Erro na API Synthea ou transformação FHIR

### 📊 Sistema e Monitoramento

#### **GET** `/health` - Health check da aplicação
**Response 200:**
```json
{
  "status": "healthy",
  "service": "nuvie-backend", 
  "version": "2.0.0",
  "database": "connected",
  "cache": "connected"
}
```

#### **GET** `/metrics` - Métricas para Prometheus
**Response 200:**
```json
{
  "service": "nuvie-backend",
  "uptime": "healthy",
  "database": "connected", 
  "memory_usage": "optimal",
  "active_users": 45,
  "total_patients": 1234
}
```

#### **GET** `/` - Informações da API
**Response 200:**
```json
{
  "message": "Nuvie Backend Challenge API",
  "version": "2.0.0", 
  "status": "active",
  "architecture": "Clean Architecture"
}
```

### 🔍 Códigos de Status HTTP

| Código | Significado | Quando Ocorre |
|--------|-------------|---------------|
| 200 | Success | Operação bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Dados inválidos ou validação falhou |
| 401 | Unauthorized | Token ausente ou inválido |
| 404 | Not Found | Recurso não encontrado |
| 422 | Validation Error | Erro de validação Pydantic |
| 500 | Internal Error | Erro interno do servidor |

---

## 🚀 ETAPA 3: EXECUÇÃO E SCRIPTS

### 📋 Pré-requisitos

#### **Ambiente Dockerizado (Recomendado)**
- 🐳 **Docker Desktop** 20.10+
- 🔧 **Docker Compose** 2.0+
- 💾 **4GB RAM** disponível
- 💿 **2GB espaço** em disco

#### **Desenvolvimento Local**
- 🐍 **Python 3.11+**
- 🐘 **PostgreSQL 15+**  
- 🔴 **Redis 7+**
- 📦 **pip** ou **poetry**

### 📜 Scripts Disponíveis

#### **🚀 start.bat / start.sh** - Inicialização completa
```bash
# Verifica Docker
# Copia .env.example → .env (se necessário)
# Inicia todos os serviços
# Aguarda inicialização (10s)
# Testa health check
# Exibe URLs de acesso
```

#### **🔄 restart.bat** - Reinicialização com rebuild
```bash  
# Para containers existentes
# Remove volumes e imagens antigas
# Reconstrói com --no-cache
# Inicia serviços atualizados
# Aguarda e testa (20s)
# Exibe logs em caso de erro
```

### 🐳 Execução via Docker (Recomendado)

#### **Início Rápido**
```bash
# Windows
start.bat

# Linux/Mac  
chmod +x start.sh
./start.sh
```

#### **Comandos Manuais**
```bash
# 1. Copiar configurações
cp .env.example .env

# 2. Editar variáveis (opcional)
# Abrir .env e ajustar configurações

# 3. Iniciar todos os serviços
docker-compose up -d

# 4. Verificar logs
docker-compose logs -f api

# 5. Parar aplicação
docker-compose down
```

#### **Rebuild Completo**
```bash
# Para desenvolvimento com mudanças
docker-compose down --volumes
docker-compose build --no-cache
docker-compose up -d
```

### 💻 Execução Local (Desenvolvimento)

#### **1. Configuração do Ambiente**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

#### **2. Configurar Banco de Dados**
```bash
# PostgreSQL local
createdb nuvie_db

# Configurar .env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/nuvie_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-development-secret-key
```

#### **3. Executar Migrations**
```bash
# Criar migration inicial
alembic upgrade head

# Verificar status
alembic current
```

#### **4. Iniciar Aplicação**
```bash
# Modo desenvolvimento (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### ⚙️ Configuração de Ambiente

#### **Arquivo .env Principal**
```env
# Banco de dados
DATABASE_URL=postgresql+asyncpg://nuvie_user:nuvie_password@localhost:5432/nuvie_db

# Cache Redis  
REDIS_URL=redis://localhost:6379

# Autenticação
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# APIs Externas
SYNTHEA_BASE_URL=https://synthea.mitre.org/

# Aplicação
DEBUG=true
ENVIRONMENT=development
```

#### **Variáveis para Produção**
```env
# Docker Compose Production
POSTGRES_USER=nuvie_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=nuvie_db
SECRET_KEY=your-production-secret-key-256-bits
DEBUG=false
ENVIRONMENT=production
```

### 🔧 Troubleshooting

#### **🐳 Problemas Docker**

**Erro: "Cannot connect to Docker daemon"**
```bash
# Verificar se Docker está rodando
docker info

# Reiniciar Docker Desktop
# Windows: Reiniciar aplicação
# Linux: sudo systemctl restart docker
```

**Erro: "Port 8000 already in use"**
```bash
# Encontrar processo usando porta
netstat -ano | findstr :8000  # Windows
lsof -i :8000                # Linux/Mac

# Parar aplicação anterior
docker-compose down
```

**Erro: "No space left on device"**
```bash
# Limpar volumes não utilizados
docker system prune -a --volumes

# Verificar espaço
docker system df
```

#### **🗄️ Problemas de Banco**

**Erro: "Connection refused"**
```bash
# Verificar se PostgreSQL está rodando
docker-compose logs db

# Verificar conexão
docker-compose exec db psql -U nuvie_user -d nuvie_db
```

**Erro: "Relation does not exist"**
```bash
# Executar migrations
docker-compose exec api alembic upgrade head

# Verificar tabelas
docker-compose exec db psql -U nuvie_user -d nuvie_db -c "\dt"
```

#### **🔐 Problemas de Autenticação**

**Erro: "Invalid token"**
- Verificar se token não expirou (30 min default)
- Confirmar formato: `Authorization: Bearer {token}`
- Verificar SECRET_KEY consistente

### 🌐 URLs de Acesso

#### **Desenvolvimento Local**
- 🏠 **API Principal**: http://localhost:8000
- 📖 **Documentação Swagger**: http://localhost:8000/docs  
- 📚 **Documentação ReDoc**: http://localhost:8000/redoc
- ❤️ **Health Check**: http://localhost:8000/health
- 📊 **Métricas**: http://localhost:8000/metrics
- 🗄️ **PostgreSQL**: localhost:5432
- 🔴 **Redis**: localhost:6379

#### **Docker Services**
```bash
# Verificar status de todos os containers
docker-compose ps

# Logs específicos por serviço
docker-compose logs api      # FastAPI application
docker-compose logs db       # PostgreSQL database  
docker-compose logs redis    # Redis cache

# Acesso direto aos containers
docker-compose exec api bash      # Terminal API
docker-compose exec db psql -U nuvie_user -d nuvie_db  # PostgreSQL CLI
docker-compose exec redis redis-cli  # Redis CLI
```

#### **Comandos de Monitoramento**
```bash
# Performance em tempo real
docker stats

# Verificar health checks
docker-compose ps
curl http://localhost:8000/health

# Logs estruturados
docker-compose logs api | grep ERROR
docker-compose logs api --tail=100 --follow
```