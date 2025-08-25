# 🏥 Nuvie Backend Challenge - Sistema de Gerenciamento de Pacientes

[![FastAPI](https://img.shields.io/badge/FastAPI-009639?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FCA121?style=for-the-badge&logo=SQLAlchemy&logoColor=white)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)](https://jwt.io)

---

## 📋 SOBRE O PROJETO

### 🎯 Descrição do Sistema
Sistema backend moderno e escalável para **gerenciamento completo de dados de pacientes** desenvolvido com FastAPI. Implementa Clean Architecture para garantir maintibilidade, escalabilidade e testabilidade. O sistema permite CRUD completo de pacientes, autenticação JWT, integração com APIs externas para importação de dados e documentação automática via Swagger.

### 🛠️ Stack Tecnológica

#### **🚀 Framework e Linguagem**
- **FastAPI 0.104.1** - Framework web assíncrono de alta performance
- **Python 3.11+** - Linguagem principal com type hints completos
- **Uvicorn** - Servidor ASGI de produção

#### **🗄️ Banco de Dados e ORM**
- **PostgreSQL 15** - Banco de dados relacional principal
- **SQLAlchemy 2.0 Async** - ORM moderno com suporte assíncrono
- **Alembic** - Sistema de migrations automáticas
- **asyncpg** - Driver PostgreSQL assíncrono

#### **🔐 Autenticação e Segurança**
- **JWT (JSON Web Tokens)** - Autenticação stateless
- **bcrypt** - Hash seguro de senhas
- **passlib** - Biblioteca de criptografia
- **python-jose** - Manipulação de tokens JWT

#### **📊 Validação e Serialização**
- **Pydantic V2** - Validação de dados com ConfigDict
- **EmailValidator** - Validação específica de emails
- **Regex Validators** - Validações customizadas

#### **🌐 Integrações Externas**
- **httpx** - Cliente HTTP assíncrono moderno
- **JSONPlaceholder API** - Fonte de dados externos simulados

#### **🧪 Testes e Qualidade**
- **pytest** - Framework de testes robusto
- **pytest-asyncio** - Suporte para testes assíncronos
- **pytest-cov** - Relatórios de cobertura de código
- **TestClient** - Cliente de testes FastAPI

#### **🐳 Infraestrutura e Deploy**
- **Docker & Docker Compose** - Containerização completa
- **Nginx** - Proxy reverso para produção
- **Scripts .bat/.sh** - Automação de deployment

### 🏗️ Arquitetura Implementada

**Clean Architecture** com separação clara de responsabilidades:

```
📁 app/
├── 🎯 domain/              # Regras de Negócio
│   ├── entities/           # Entidades principais (Patient, User)
│   └── interfaces.py       # Contratos e abstrações
├── 🔄 application/         # Casos de Uso
│   └── use_cases/          # Lógica de aplicação
├── 🔧 infrastructure/      # Detalhes Técnicos
│   ├── repositories/       # Acesso a dados
│   └── external/           # APIs externas
├── 🌐 presentation/        # Interface Web
│   └── controllers/        # Endpoints REST
├── 📄 schemas/             # DTOs Pydantic
└── 🗄️ models/              # Models SQLAlchemy
```

### ⚡ Funcionalidades Principais

#### **👥 Gestão de Pacientes**
- ✅ **CRUD Completo** - Criar, ler, atualizar e deletar pacientes
- ✅ **Busca Avançada** - Filtros por nome com paginação
- ✅ **Validação Rigorosa** - Email único, telefone e nome
- ✅ **Modelo Simplificado** - name, email, phone (essencial)

#### **🔐 Sistema de Autenticação**
- ✅ **Registro de Usuários** - Criação de contas seguras
- ✅ **Login JWT** - Autenticação stateless moderna
- ✅ **Proteção de Rotas** - Middleware de autenticação
- ✅ **Validação de Tokens** - Verificação automática

#### **🔗 Integração Externa**
- ✅ **Import de Dados** - Consumo da API JSONPlaceholder
- ✅ **Transformação de Dados** - Limpeza e normalização
- ✅ **Controle de Duplicatas** - Validação por email único
- ✅ **Tratamento de Erros** - Handling robusto

#### **📊 Monitoramento e Saúde**
- ✅ **Health Check** - Verificação de status da aplicação
- ✅ **Documentação Automática** - Swagger UI integrado
- ✅ **Logs Estruturados** - Rastreamento de operações
- ✅ **Métricas de Sistema** - Informações de performance

---

## 🚀 COMO INICIAR O PROJETO

### 🎯 Scripts .BAT (Prioridade 1 - Recomendado)

#### **Inicialização Rápida**
```batch
# Primeira execução - Setup completo
start.bat

# Reinicialização com rebuild
restart.bat

# Execução de testes
test.bat
```

#### **Funcionalidades dos Scripts**
- **`start.bat`**: Verifica Docker, copia .env, inicia serviços, aguarda inicialização, testa health check
- **`restart.bat`**: Para containers, remove volumes, reconstrói imagens, reinicia com configurações atualizadas
- **`test.bat`**: Executa suite completa de testes com relatórios de cobertura

### 🐳 Docker Compose (Prioridade 2)

#### **Comandos Manuais**
```bash
# 1. Preparação do ambiente
cp .env.example .env

# 2. Inicialização completa
docker-compose up --build -d

# 3. Executar migrations
docker-compose exec api alembic upgrade head

# 4. Verificar status
docker-compose ps
docker-compose logs api

# 5. Parar aplicação
docker-compose down
```

#### **Comandos de Desenvolvimento**
```bash
# Rebuild completo (após mudanças)
docker-compose down --volumes
docker-compose build --no-cache
docker-compose up -d

# Logs em tempo real
docker-compose logs -f api

# Acesso ao container
docker-compose exec api bash
```

### 🐍 Python Direto (Prioridade 3)

#### **Setup do Ambiente**
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt
```

#### **Configuração Local**
```bash
# 4. Configurar PostgreSQL local
createdb nuvie_db

# 5. Configurar variáveis de ambiente
# Editar .env com configurações locais
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/nuvie_db
SECRET_KEY=your-local-secret-key

# 6. Executar migrations
alembic upgrade head

# 7. Iniciar aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🧪 Comandos de Teste e Diagnóstico

#### **Execução de Testes**
```bash
# Todos os testes com Docker
docker-compose exec api pytest

# Testes com cobertura
docker-compose exec api pytest --cov=app --cov-report=html

# Testes específicos
docker-compose exec api pytest tests/test_patients.py -v
docker-compose exec api pytest tests/test_auth.py -v
```

#### **Diagnóstico Completo (Comando Específico)**
```bash
# Script de diagnóstico detalhado
docker-compose exec api bash diagnose_tests.sh
```

**O script `diagnose_tests.sh` executa:**
- ✅ Teste de autenticação específico
- ✅ Teste de paciente específico  
- ✅ Teste de endpoint completo
- ✅ Resumo de todos os testes (34 testes)
- ✅ Relatório detalhado de falhas
- ✅ Análise de warnings e logs

#### **Outros Comandos Úteis**
```bash
# Verificar saúde da aplicação
curl http://localhost:8000/health

# Documentação Swagger
# Abrir: http://localhost:8000/docs

# Logs específicos
docker-compose logs api | grep ERROR
docker-compose logs db --tail=50

# Status dos containers
docker-compose ps
docker stats
```

### 🌐 URLs de Acesso

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **API Principal** | http://localhost:8000 | Endpoint base da API |
| **Swagger UI** | http://localhost:8000/docs | Documentação interativa |
| **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |
| **Health Check** | http://localhost:8000/health | Status da aplicação |
| **PostgreSQL** | localhost:5432 | Banco de dados |

---

## 📚 ENDPOINTS E DOCUMENTAÇÃO

### 🔐 Autenticação

#### `POST /auth/register` - Registrar Novo Usuário

**Descrição:** Cria uma nova conta de usuário no sistema com validações completas

**Autenticação:** ❌ Não necessária

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Body | username | string | ✅ | Nome de usuário único (3-50 chars) |
| Body | email | string | ✅ | Email válido e único |
| Body | password | string | ✅ | Senha segura (min 8 chars) |
| Body | full_name | string | ❌ | Nome completo (max 200 chars) |

**Validações:**
- username: Apenas letras, números e underscore
- email: Formato válido de email (@domain.com)
- password: Mínimo 8 caracteres com letras e números
- full_name: Somente letras, espaços e acentos

**Exemplo Request:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao123",
    "email": "joao@example.com",
    "password": "MinhaSenh@123",
    "full_name": "João Silva"
  }'
```

**Exemplo Response (201):**
```json
{
  "id": 1,
  "username": "joao123",
  "email": "joao@example.com",
  "full_name": "João Silva",
  "is_active": true,
  "created_at": "2025-08-25T10:00:00Z"
}
```

**Possíveis Erros:**
- 400: Bad Request - Email já cadastrado
- 422: Validation Error - Dados inválidos

#### `POST /auth/token` - Login e Obtenção de JWT

**Descrição:** Autentica usuário e retorna token JWT para acesso às rotas protegidas

**Autenticação:** ❌ Não necessária

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Form | username | string | ✅ | Nome de usuário ou email |
| Form | password | string | ✅ | Senha do usuário |

**Validações:**
- username: Deve existir no sistema
- password: Deve corresponder ao hash armazenado

**Exemplo Request:**
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao123&password=MinhaSenh@123"
```

**Exemplo Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2FvMTIzIiwiZXhwIjoxNjM5NTU2NDAwfQ.signature",
  "token_type": "bearer"
}
```

**Possíveis Erros:**
- 400: Bad Request - Credenciais inválidas

#### `GET /auth/me` - Dados do Usuário Autenticado

**Descrição:** Retorna informações do usuário logado baseado no token JWT

**Autenticação:** ✅ Obrigatória

**Parâmetros:** Nenhum

**Validações:**
- Token JWT válido no header Authorization
- Usuário deve existir e estar ativo

**Exemplo Request:**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Exemplo Response (200):**
```json
{
  "id": 1,
  "username": "joao123", 
  "email": "joao@example.com",
  "full_name": "João Silva",
  "is_active": true
}
```

**Possíveis Erros:**
- 403: Forbidden - Token ausente
- 401: Unauthorized - Token inválido/expirado

### 👥 Gestão de Pacientes

#### `GET /patients/` - Listar Pacientes com Filtros

**Descrição:** Lista pacientes com paginação e busca por nome

**Autenticação:** ✅ Obrigatória

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Query | skip | int | ❌ | Registros para pular (padrão: 0) |
| Query | limit | int | ❌ | Máximo de registros (padrão: 100, máx: 1000) |
| Query | search | string | ❌ | Busca no nome do paciente (mín: 2 chars) |

**Validações:**
- skip: Deve ser >= 0
- limit: Entre 1 e 1000
- search: Mínimo 2 caracteres se informado

**Exemplo Request:**
```bash
curl -X GET "http://localhost:8000/patients/?skip=0&limit=10&search=Silva" \
  -H "Authorization: Bearer TOKEN_JWT"
```

**Exemplo Response (200):**
```json
[
  {
    "id": 1,
    "name": "João Silva",
    "email": "joao.silva@email.com", 
    "phone": "+5511999999999",
    "created_at": "2025-08-25T10:00:00Z",
    "updated_at": "2025-08-25T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Maria Silva Santos",
    "email": "maria.santos@email.com",
    "phone": "+5511888888888", 
    "created_at": "2025-08-25T11:00:00Z",
    "updated_at": "2025-08-25T11:00:00Z"
  }
]
```

**Possíveis Erros:**
- 403: Forbidden - Sem autenticação
- 400: Bad Request - Parâmetros inválidos

#### `POST /patients/` - Criar Novo Paciente

**Descrição:** Cria um novo paciente no sistema com dados obrigatórios

**Autenticação:** ✅ Obrigatória

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Body | name | string | ✅ | Nome completo (2-100 chars) |
| Body | email | string | ✅ | Email único e válido |
| Body | phone | string | ✅ | Telefone (10-20 chars) |

**Validações:**
- name: Apenas letras, espaços, hífens e apostrofes
- email: Formato válido e único no sistema
- phone: Entre 10-15 dígitos (aceita formatação)

**Exemplo Request:**
```bash
curl -X POST "http://localhost:8000/patients/" \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana Costa",
    "email": "ana.costa@email.com",
    "phone": "+5511777777777"
  }'
```

**Exemplo Response (201):**
```json
{
  "id": 3,
  "name": "Ana Costa",
  "email": "ana.costa@email.com",
  "phone": "+5511777777777",
  "created_at": "2025-08-25T12:00:00Z",
  "updated_at": "2025-08-25T12:00:00Z"
}
```

**Possíveis Erros:**
- 400: Bad Request - Email já existe
- 422: Validation Error - Dados inválidos

#### `GET /patients/{id}` - Buscar Paciente por ID

**Descrição:** Retorna dados completos de um paciente específico

**Autenticação:** ✅ Obrigatória

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Path | id | int | ✅ | ID único do paciente |

**Validações:**
- id: Deve ser inteiro positivo e existir no sistema

**Exemplo Request:**
```bash
curl -X GET "http://localhost:8000/patients/1" \
  -H "Authorization: Bearer TOKEN_JWT"
```

**Exemplo Response (200):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao.silva@email.com",
  "phone": "+5511999999999",
  "created_at": "2025-08-25T10:00:00Z", 
  "updated_at": "2025-08-25T10:00:00Z"
}
```

**Possíveis Erros:**
- 404: Not Found - Paciente não encontrado
- 403: Forbidden - Sem autenticação

#### `PUT /patients/{id}` - Atualizar Paciente

**Descrição:** Atualiza dados de um paciente existente (campos opcionais)

**Autenticação:** ✅ Obrigatória

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Path | id | int | ✅ | ID único do paciente |
| Body | name | string | ❌ | Novo nome (2-100 chars) |
| Body | email | string | ❌ | Novo email (deve ser único) |
| Body | phone | string | ❌ | Novo telefone (10-20 chars) |

**Validações:**
- Mesmas validações do POST para campos informados
- Email deve ser único (exceto se for o mesmo atual)

**Exemplo Request:**
```bash
curl -X PUT "http://localhost:8000/patients/1" \
  -H "Authorization: Bearer TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva Santos",
    "phone": "+5511666666666"
  }'
```

**Exemplo Response (200):**
```json
{
  "id": 1,
  "name": "João Silva Santos",
  "email": "joao.silva@email.com",
  "phone": "+5511666666666",
  "created_at": "2025-08-25T10:00:00Z",
  "updated_at": "2025-08-25T13:00:00Z"
}
```

**Possíveis Erros:**
- 404: Not Found - Paciente não encontrado
- 400: Bad Request - Email já existe

#### `DELETE /patients/{id}` - Deletar Paciente

**Descrição:** Remove permanentemente um paciente do sistema

**Autenticação:** ✅ Obrigatória

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Path | id | int | ✅ | ID único do paciente |

**Validações:**
- id: Deve ser inteiro positivo e existir no sistema

**Exemplo Request:**
```bash
curl -X DELETE "http://localhost:8000/patients/1" \
  -H "Authorization: Bearer TOKEN_JWT"
```

**Exemplo Response (200):**
```json
{
  "message": "Patient deleted successfully"
}
```

**Possíveis Erros:**
- 404: Not Found - Paciente não encontrado
- 403: Forbidden - Sem autenticação

#### `POST /patients/import-data` - Importar Dados Externos

**Descrição:** Importa pacientes da API JSONPlaceholder com transformação automática

**Autenticação:** ✅ Obrigatória

**Parâmetros:**
| Tipo | Nome | Tipo | Obrigatório | Descrição |
|------|------|------|-------------|-----------|
| Query | count | int | ❌ | Quantidade para importar (padrão: 10, máx: 100) |

**Validações:**
- count: Entre 1 e 100
- Dados são automaticamente limpos e validados
- Emails duplicados são ignorados

**Exemplo Request:**
```bash
curl -X POST "http://localhost:8000/patients/import-data?count=5" \
  -H "Authorization: Bearer TOKEN_JWT"
```

**Exemplo Response (200):**
```json
{
  "message": "Successfully imported 3 patients from external API"
}
```

**Possíveis Erros:**
- 500: Internal Server Error - Erro na API externa
- 403: Forbidden - Sem autenticação

### 📊 Sistema e Monitoramento

#### `GET /health` - Health Check da Aplicação

**Descrição:** Verifica o status geral da aplicação e dependências

**Autenticação:** ❌ Não necessária

**Parâmetros:** Nenhum

**Validações:** Nenhuma

**Exemplo Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Exemplo Response (200):**
```json
{
  "status": "healthy",
  "service": "nuvie-backend",
  "version": "2.0.0",
  "timestamp": "2025-08-25T14:00:00Z"
}
```

**Possíveis Erros:**
- 500: Internal Server Error - Serviço indisponível

#### `GET /` - Informações da API

**Descrição:** Retorna informações básicas sobre a API

**Autenticação:** ❌ Não necessária

**Parâmetros:** Nenhum

**Validações:** Nenhuma

**Exemplo Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Exemplo Response (200):**
```json
{
  "message": "Nuvie Backend Challenge API",
  "version": "2.0.0",
  "status": "active",
  "docs": "/docs"
}
```

### 🔍 Códigos de Status HTTP

| Código | Nome | Descrição | Quando Ocorre |
|--------|------|-----------|---------------|
| **200** | OK | Sucesso | Operação realizada com êxito |
| **201** | Created | Criado | Recurso criado com sucesso |
| **400** | Bad Request | Solicitação Inválida | Dados inválidos ou regra de negócio violada |
| **401** | Unauthorized | Não Autorizado | Token JWT inválido ou expirado |
| **403** | Forbidden | Proibido | Token JWT ausente |
| **404** | Not Found | Não Encontrado | Recurso solicitado não existe |
| **422** | Unprocessable Entity | Entidade Não Processável | Erro de validação Pydantic |
| **500** | Internal Server Error | Erro Interno | Erro não tratado no servidor |

### 📋 Estrutura de Resposta de Erro

**Exemplo de Erro de Validação (422):**
```json
{
  "details": [
    {
      "type": "string_too_short",
      "loc": ["body", "name"],
      "msg": "String should have at least 2 characters",
      "input": "A"
    }
  ],
  "error": "Validation failed",
  "message": "The request contains invalid data"
}
```

**Exemplo de Erro de Negócio (400):**
```json
{
  "detail": "Patient with this email already exists"
}
```