# GarimpoAuto (cars-project)

[![CI/CD Pipeline](https://github.com/iuri-medina/cars-project/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/iuri-medina/cars-project/actions/workflows/ci-cd.yml)

Sistema de gerenciamento de anúncios de veículos desenvolvido com Django, PostgreSQL, Nginx e Docker, com deploy automatizado no Google Cloud Platform via GitHub Actions.

## Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Stack Tecnológica](#stack-tecnológica)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Desenvolvimento Local](#desenvolvimento-local)
  - [Com Docker (Recomendado)](#com-docker-recomendado)
  - [Sem Docker](#sem-docker)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deploy no Google Cloud](#deploy-no-google-cloud)
  - [Configuração Inicial do GCP](#configuração-inicial-do-gcp)
  - [Configuração da Instância VM](#configuração-da-instância-vm)
  - [Secrets do GitHub](#secrets-do-github)
- [Operações](#operações)
- [Nginx e Arquivos Estáticos](#nginx-e-arquivos-estáticos)
- [Observabilidade](#observabilidade)
- [Segurança](#segurança)

---

## Visão Geral

O **GarimpoAuto** é uma plataforma para gerenciamento de anúncios de veículos, permitindo cadastro, edição, busca e visualização de carros feita para fins de estudos. O sistema utiliza arquitetura moderna com containers Docker, deploy automatizado e infraestrutura escalável na nuvem.

<img width="1439" height="772" alt="tela1" src="https://github.com/user-attachments/assets/c068b9e2-8795-4f5e-b2d8-29d72a1ab9b0" />

<img width="1440" height="777" alt="Captura de Tela 2025-10-17 às 23 05 02" src="https://github.com/user-attachments/assets/8a0e937e-8494-41e1-a1af-f356178fba31" />

<img width="1440" height="777" alt="Captura de Tela 2025-10-17 às 23 05 24" src="https://github.com/user-attachments/assets/7c720c21-5c32-4759-afdf-ba2c0f7c2b25" />

<img width="1440" height="778" alt="Captura de Tela 2025-10-17 às 23 05 45" src="https://github.com/user-attachments/assets/ce8ca60e-344a-4fa5-b25e-4cbfd2995751" />

<img width="1440" height="777" alt="Captura de Tela 2025-10-17 às 23 06 38" src="https://github.com/user-attachments/assets/3c987fa4-a5bd-4889-9f89-9590853e5dc4" />

<img width="1440" height="779" alt="Captura de Tela 2025-10-17 às 23 06 48" src="https://github.com/user-attachments/assets/76df6ce6-8115-4280-a2e4-623ba8fe779d" />


**Características principais:**

- Totalmente containerizado com Docker Compose v2
- CI/CD automatizado com GitHub Actions
- Deploy automático no Google Cloud Compute Engine
- Autenticação de usuários e controle de acesso
- Artifact Registry para gerenciamento de imagens Docker
- Nginx como proxy reverso e servidor de arquivos estáticos
- PostgreSQL como banco de dados
- Testes automatizados no pipeline

---

## Arquitetura

```
┌─────────┐
│  User   │
└────┬────┘
     │
     ▼
┌─────────────────┐
│  Nginx :80      │ ◄── Proxy reverso + arquivos estáticos/media
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Gunicorn/Django │ ◄── Aplicação Python
│    app:8000     │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│  PostgreSQL     │ ◄── Banco de dados
│    db:5432      │
└─────────────────┘

Volumes Docker:
├── static_volume  → /app/staticfiles (CSS, JS, assets)
├── media_volume   → /app/media (uploads de usuários)
└── postgres_data  → /var/lib/postgresql/data (dados do banco)
```

---

## Stack Tecnológica

| Componente          | Tecnologia                 | Versão            |
| ------------------- | -------------------------- | ----------------- |
| **Backend**         | Python/Django              | 5.2+              |
| **Banco de Dados**  | PostgreSQL                 | 17                |
| **Servidor App**    | Gunicorn                   | Latest            |
| **Proxy Reverso**   | Nginx                      | Latest            |
| **Containerização** | Docker + Docker Compose v2 | Latest            |
| **CI/CD**           | GitHub Actions             | -                 |
| **Cloud**           | Google Cloud Platform      | -                 |
| **Registry**        | Artifact Registry          | us-docker.pkg.dev |

---

## Estrutura do Projeto

```
cars-project/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline de CI/CD
├── app/                        # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                   # App de autenticação
├── cars/                       # App principal (anúncios)
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── fixtures/              # Dados iniciais (states, brands)
│   └── templates/
├── static/                     # Arquivos estáticos fonte (CSS, JS)
│   ├── css/
│   └── js/
├── media/                      # Uploads de usuários
├── nginx/
│   └── nginx.conf             # Configuração do Nginx
├── docker-compose.yml         # Orquestração de containers
├── Dockerfile                 # Imagem da aplicação
├── entrypoint.sh              # Script de inicialização (migrations + collectstatic)
├── requirements.txt           # Dependências Python
├── manage.py
└── README.md
```

---

## Pré-requisitos

### Para Desenvolvimento Local

- **Docker Desktop** ou **Docker Engine** + **Docker Compose v2**
- **Git**
- (Opcional) **Python 3.11+** se rodar sem Docker

### Para Deploy no GCP

- **Google Cloud SDK (gcloud CLI)**
- **Conta GCP** com projeto ativo
- **Instância Compute Engine** configurada

---

## Desenvolvimento Local

### Com Docker (Recomendado)

#### 1. Clone o repositório

```bash
git clone https://github.com/iuri-medina/cars-project.git
cd cars-project
```

#### 2. Crie o arquivo `.env`

```bash
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=dev-only-not-secret-change-in-production
ALLOWED_HOSTS=*
POSTGRES_DB=carros
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
EOF
```

#### 3. Inicie os serviços

```bash
docker compose up --build -d
```

O `entrypoint.sh` automaticamente:

- Aguarda o PostgreSQL ficar pronto
- Executa `makemigrations` e `migrate`
- Carrega fixtures (estados e marcas)
- Executa `collectstatic`
- Inicia o Gunicorn

#### 4. Crie um superusuário

```bash
docker compose exec app python manage.py createsuperuser
```

#### 5. Acesse a aplicação

- **Frontend**: http://localhost/cars
- **Admin**: http://localhost/admin

#### 6. Visualize os logs

```bash
# Logs da aplicação
docker compose logs -f app

# Logs do Nginx
docker compose logs -f nginx

# Logs do banco de dados
docker compose logs -f db
```

---

### Sem Docker

#### 1. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

#### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 3. Configure PostgreSQL localmente

Instale e configure o PostgreSQL, depois crie o banco:

```bash
createdb carros
```

#### 4. Configure variáveis de ambiente

Crie um arquivo `.env` conforme o exemplo acima, ajustando `POSTGRES_HOST=localhost`.

#### 5. Execute as migrações

```bash
python manage.py migrate
python manage.py loaddata cars/fixtures/states.json cars/fixtures/brands.json
```

#### 6. Colete arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

#### 7. Inicie o servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

---

## Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configuração. Crie um arquivo `.env` na raiz do projeto:

### Exemplo `.env` (Desenvolvimento)

```bash
DEBUG=True
SECRET_KEY=dev-only-not-secret-change-in-production
ALLOWED_HOSTS=*
POSTGRES_DB=carros
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Exemplo `.env` (Produção)

```bash
DEBUG=False
SECRET_KEY=<gere-uma-chave-secreta-forte-aqui>
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,35.123.45.67
POSTGRES_DB=carros
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<senha-forte-e-segura>
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Descrição das Variáveis

| Variável            | Descrição                                | Padrão Dev | Produção           |
| ------------------- | ---------------------------------------- | ---------- | ------------------ |
| `DEBUG`             | Ativa modo debug do Django               | `True`     | `False`            |
| `SECRET_KEY`        | Chave secreta do Django                  | (insegura) | **Obrigatório**    |
| `ALLOWED_HOSTS`     | Hosts permitidos (separados por vírgula) | `*`        | Domínios/IPs reais |
| `POSTGRES_DB`       | Nome do banco de dados                   | `carros`   | `carros`           |
| `POSTGRES_USER`     | Usuário do PostgreSQL                    | `postgres` | `postgres`         |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL                      | `postgres` | **Senha forte**    |
| `POSTGRES_HOST`     | Host do banco                            | `db`       | `db`               |
| `POSTGRES_PORT`     | Porta do banco                           | `5432`     | `5432`             |

### Gerar SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## CI/CD Pipeline

O projeto utiliza GitHub Actions para CI/CD automatizado. O workflow está em `.github/workflows/ci-cd.yml`.

### Fluxo do Pipeline

#### **Job 1: Build & Test** (executa em todo push/PR para main/development)

1. ✅ Checkout do código
2. ✅ Criação de `.env` temporário para testes
3. ✅ Build das imagens: `docker compose build`
4. ✅ Inicialização dos serviços: `docker compose up -d`
5. ✅ Aguarda 30s para `entrypoint.sh` completar migrations e collectstatic
6. ✅ Verifica status dos containers
7. ✅ Executa testes Django: `docker compose exec -T app python manage.py test`
8. ✅ Health check: `docker compose exec -T app python manage.py check`
9. ✅ Teardown: `docker compose down -v`

#### **Job 2: Deploy** (apenas em push para main)

1. ✅ Autenticação no GCP (`google-github-actions/auth@v2`)
2. ✅ Configuração do gcloud CLI (`google-github-actions/setup-gcloud@v2`)
3. ✅ Autenticação Docker com Artifact Registry
4. ✅ Build da imagem com duas tags:
   - `us-docker.pkg.dev/$PROJECT_ID/docker-repo/cars-project:$GITHUB_SHA`
   - `us-docker.pkg.dev/$PROJECT_ID/docker-repo/cars-project:latest`
5. ✅ Push para Artifact Registry
6. ✅ SSH na instância Compute Engine
7. ✅ Correção de estrutura de diretórios (se necessário)
8. ✅ Git pull (ou clone se não existir) em `/opt/cars-project`
9. ✅ Pull da imagem mais recente
10. ✅ Stop dos containers antigos: `docker compose down`
11. ✅ Início dos novos containers: `docker compose up -d`
12. ✅ Aguarda 20s para inicialização
13. ✅ Verifica deployment: `docker compose ps`
14. ✅ Limpeza de imagens antigas (>24h)

---

## Deploy no Google Cloud

### Configuração Inicial do GCP

#### 1. Criar Repositório no Artifact Registry

```bash
export PROJECT_ID=$(gcloud config get-value project)

gcloud artifacts repositories create docker-repo \
  --repository-format=docker \
  --location=us \
  --description="Docker repository for cars-project CI/CD"
```

#### 2. Criar Service Account e Atribuir Permissões

```bash
# Criar service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions CI/CD"

# Artifact Registry Writer (push de imagens)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

# Artifact Registry Reader (pull de imagens)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

# Compute Instance Admin (gerenciar VMs)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/compute.instanceAdmin.v1"

# Service Account User
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Storage Admin (para GCR/GCS)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Compute OS Login (para SSH)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/compute.osLogin"
```

#### 3. Gerar Chave JSON da Service Account

```bash
gcloud iam service-accounts keys create ~/gcp-key.json \
  --iam-account=github-actions@${PROJECT_ID}.iam.gserviceaccount.com

# Exibir conteúdo (você precisará copiar isso para o GitHub)
cat ~/gcp-key.json
```

#### 4. Habilitar APIs Necessárias

```bash
gcloud services enable artifactregistry.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable compute.googleapis.com
```

---

### Configuração da Instância VM

#### 1. SSH na Instância

```bash
gcloud compute ssh SUA_INSTANCIA --zone=SUA_ZONA
```

#### 2. Instalar Docker e Docker Compose v2

```bash
# Atualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
sudo apt-get install -y docker.io docker-compose-plugin git

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Habilitar Docker no boot
sudo systemctl enable docker
sudo systemctl start docker

# Verificar instalação
docker --version
docker compose version
```

#### 3. Preparar Diretório do Projeto

```bash
# Criar diretório
sudo mkdir -p /opt/cars-project
sudo chown -R $USER:$USER /opt/cars-project
cd /opt/cars-project
```

#### 4. Criar Arquivo `.env` de Produção

```bash
nano .env
```

Cole e ajuste:

```bash
DEBUG=False
SECRET_KEY=cole-aqui-uma-chave-secreta-forte-gerada
ALLOWED_HOSTS=seudominio.com,35.123.45.67
POSTGRES_DB=carros
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha-super-segura-aqui
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Salve (`Ctrl+O`, `Enter`, `Ctrl+X`) e ajuste permissões:

```bash
chmod 644 .env
```

#### 5. Configurar Firewall (se necessário)

```bash
# Abrir porta 80 (HTTP)
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow HTTP traffic"

# Abrir porta 443 (HTTPS)
gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow HTTPS traffic"
```

#### 6. Autenticar Docker com Artifact Registry

```bash
gcloud auth configure-docker us-docker.pkg.dev
```

#### 7. Sair da VM

```bash
exit
```

---

### Secrets do GitHub

Configure estes 4 secrets no GitHub:

**Caminho**: `Repositório → Settings → Secrets and variables → Actions → New repository secret`

| Nome                | Valor                            | Como Obter                                             |
| ------------------- | -------------------------------- | ------------------------------------------------------ |
| `GCP_PROJECT_ID`    | ID do seu projeto GCP            | `gcloud config get-value project`                      |
| `GCP_SA_KEY`        | Conteúdo completo do JSON        | `cat ~/gcp-key.json` (cole todo o JSON)                |
| `GCE_INSTANCE_NAME` | Nome da instância Compute Engine | `gcloud compute instances list --format="value(name)"` |
| `GCE_INSTANCE_ZONE` | Zona da instância                | `gcloud compute instances list --format="value(zone)"` |

---

## Operações

### Comandos Docker Compose

```bash
# Iniciar serviços
docker compose up -d

# Iniciar com rebuild
docker compose up -d --build

# Parar serviços
docker compose down

# Parar e remover volumes
docker compose down -v

# Ver logs
docker compose logs -f app
docker compose logs -f nginx
docker compose logs -f db

# Ver status dos containers
docker compose ps
```

### Comandos Django

```bash
# Executar testes
docker compose exec -T app python manage.py test

# Criar superusuário
docker compose exec app python manage.py createsuperuser

# Executar migrações
docker compose exec app python manage.py migrate

# Criar migrações
docker compose exec app python manage.py makemigrations

# Coletar arquivos estáticos
docker compose exec app python manage.py collectstatic --noinput

# Abrir shell do Django
docker compose exec app python manage.py shell

# Abrir shell do banco
docker compose exec db psql -U postgres -d carros

# Health check
docker compose exec app python manage.py check
```

---

## Nginx e Arquivos Estáticos

O **Nginx** atua como:

1. **Proxy reverso**: Encaminha requisições para o Gunicorn (porta 8000)
2. **Servidor de arquivos estáticos**: Serve diretamente `/static` e `/media`

### Fluxo de Arquivos Estáticos

**Desenvolvimento** (`DEBUG=True`):

- Django serve arquivos estáticos automaticamente
- Arquivos fonte em `/app/static`

**Produção** (`DEBUG=False`):

1. `entrypoint.sh` executa `collectstatic` → copia para `/app/staticfiles`
2. Nginx serve de `static_volume` mapeado para `/app/staticfiles`
3. Requisições `/static/*` → Nginx serve diretamente (sem passar pelo Django)

### Configuração de Portas

Por padrão, o Nginx escuta na porta **80** (mapeada no `docker-compose.yml`).

Para alterar:

```yaml
# docker-compose.yml
services:
  nginx:
    ports:
      - '8080:80' # Altera porta externa para 8080
```

### Volumes Importantes

| Volume          | Caminho no Container       | Finalidade                 |
| --------------- | -------------------------- | -------------------------- |
| `static_volume` | `/app/staticfiles`         | CSS, JS, imagens estáticas |
| `media_volume`  | `/app/media`               | Uploads de usuários        |
| `postgres_data` | `/var/lib/postgresql/data` | Dados do banco PostgreSQL  |

## Segurança

### Checklist de Segurança

#### Variáveis de Ambiente

- ✅ **Nunca commite o arquivo `.env`** (incluído no `.gitignore`)
- ✅ `DEBUG=False` em produção
- ✅ `SECRET_KEY` forte e única em produção (min. 50 caracteres aleatórios)
- ✅ `ALLOWED_HOSTS` restrito a domínios/IPs reais
- ✅ Senha forte no `POSTGRES_PASSWORD`

#### Arquivos e Diretórios

- ✅ `.env` com permissões `644` (ou `600` para maior segurança)
- ✅ `/opt/cars-project` com owner correto (`chown -R user:user`)
- ✅ Não expor `.git` publicamente

#### Rede

- ✅ Firewall configurado para permitir apenas portas necessárias (80, 443)
- ✅ HTTPS configurado em produção (certificado SSL/TLS)

---

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## Suporte

Para problemas ou dúvidas, abra uma [issue no GitHub](https://github.com/iuri-medina/cars-project/issues).
