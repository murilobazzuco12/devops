# 📊 FinCalc - Motor Fiscal (Edição DevOps & Infraestrutura)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Multi--Container-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Proxy_Reverso-009639?logo=nginx&logoColor=white)

---

## 📌 Sobre o Projeto

O **FinCalc** é um sistema especializado no processamento e apuração de Imposto de Renda (IR) para investidores da bolsa de valores brasileira (B3). 

Originalmente desenvolvido com foco em regras de negócio complexas e motor fiscal, esta versão do repositório foi adaptada para aplicar rigorosas práticas de **DevOps, Infraestrutura e Cybersegurança**, isolando a aplicação em contêineres e automatizando a integração contínua.

---

## 🏗️ Arquitetura de Infraestrutura (Docker & Redes)

O sistema foi refatorado de uma execução manual para uma arquitetura **Multi-Container Isolada** utilizando Docker Compose.

* **Nginx (Proxy Reverso & Edge Security):** Único ponto de contato com o mundo externo (Portas 80 e 443). Responsável pelo terminação SSL (HTTPS) e cabeçalhos de segurança (CSP, X-Frame-Options).
* **App Backend/Frontend (FastAPI):** Roda em rede interna isolada (`frontend_net` e `backend_net`), processando rotas de API e renderização de views (Jinja2).
* **Banco de Dados (MySQL):** Totalmente inacessível externamente. Comunica-se apenas com a aplicação através da rede `backend_net`. Utiliza volumes Docker para persistência de dados.

---

## 🛡️ Cybersegurança e Boas Práticas

* **HTTPS Local Customizado:** Certificados gerados via `mkcert` operando no domínio local `fincalcDevops.local`.
* **Isolamento de Credenciais:** Senhas de banco e chaves JWT não são versionadas. Injeção dinâmica via arquivos `.env` no Docker.
* **Segurança de Borda:** Redirecionamento forçado de HTTP para HTTPS diretamente no Nginx.

---

## 🛠️ Automação e Qualidade de Código (CI/CD)

O ciclo de vida do desenvolvimento segue o padrão **GitFlow** (branches `main`, `dev` e `feature/*`). A qualidade dos commits é garantida por gatilhos locais:

* **Husky & Commitlint:** Gancho de `pre-commit` implementado para validar mensagens no padrão *Conventional Commits* (ex: `feat:`, `fix:`, `chore:`).
* **Testes End-to-End (E2E):** (Em implementação) Gancho de `pre-push` configurado para bloquear o envio de código que não passe nas validações de interface e fluxos de usuário.

---

## ⚙️ Como Executar o Projeto Localmente

### 📌 Pré-requisitos
* Docker e Docker Compose instalados.
* Ferramenta `mkcert` instalada.

### 🔧 1. Configurar Domínio Local e HTTPS
1. Adicione a seguinte linha ao final do seu arquivo `/etc/hosts` (ou `C:\Windows\System32\drivers\etc\hosts` no Windows):
   `127.0.0.1   fincalcDevops.local`
2. No terminal, navegue até a pasta `nginx/certs` do projeto e gere os certificados locais:``` 
  mkcert -install 
  mkcert fincalcDevops.local```

### 🔐 2. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto (nunca versionado) baseado no .env.example:
MYSQL_ROOT_PASSWORD=sua_senha_root
MYSQL_DATABASE=fincalcDevops
DATABASE_URL=mysql+pymysql://root:sua_senha_root@db:3306/fincalcDevops
CHAVE_SECRETA=sua_chave_jwt_segura

### 🚀 3. Subir a Infraestrutura
Na raiz do projeto, execute:
docker-compose up -d --build
Acesse a aplicação com segurança máxima em: 👉 https://fincalcDevops.local

