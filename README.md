# SkillUp Back-end

## Guia de Configuração e Execução da API com Docker Compose

Este guia mostra como configurar e executar a API com Docker Compose. Siga os passos abaixo para preparar o ambiente, configurar variáveis de ambiente e rodar a aplicação.

---

## Pré-Requisitos

- **Docker e Docker Compose:** Certifique-se de ter as últimas versões instaladas.
- **.env:** Crie e configure o arquivo `.env` na raiz do projeto.
- **Servidor SMTP:** Configure um servidor SMTP (por exemplo, [Mailtrap](https://mailtrap.io)) para envio de e-mails.
- **Chave Secreta:** Gere uma chave secreta única hex de 32 bytes (p.ex.: usando `openssl rand -hex 32`).

---

## Configuração do Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo, substituindo os valores de exemplo pelos seus dados reais:

```dotenv
# Configurações do PostgreSQL
DB_USER=YOUR_POSTGRES_USER
DB_NAME=YOUR_DATABASE_NAME
DB_HOST=YOUR_DATABASE_HOST
DB_PORT=YOUR_DATABASE_PORT
DB_PASSWORD=YOUR_PASSWORD
DB_ECHO=True

# Configurações de E-mail
EMAIL_SENDER=YOUR_EMAIL@example.com
EMAIL_SERVER_HOST=YOUR_SENDER.stmp.io
EMAIL_SERVER_PORT=512
EMAIL_PASSWORD=foo_bar
EMAIL_USERNAME=baz_foo

# Configurações do Back-end
BACKEND_DOMAIN=localhost
SECRET_KEY=type_your_secret_key_here
SECURE_COOKIES=False
```

- **Banco de Dados:** Ajuste as credenciais e os detalhes do PostgreSQL.
- **E-mail:** Configure os dados do seu servidor SMTP (no exemplo, Mailtrap).
- **SECRET_KEY:** Gere uma chave secreta forte para a aplicação.

---

## Estrutura dos Arquivos Docker

### `docker-compose.yaml`

Define os serviços da aplicação:

- **app:** Constrói a imagem com base no `Dockerfile`, mapeia a porta 8000, carrega as variáveis do `.env` e depende do serviço do banco.
- **db:** Utiliza a imagem do Postgres, aplica as variáveis do `.env` e persiste dados no volume `postgres_data`.

### `Dockerfile`

- Baseado em `python:3.13-slim`.
- Instala dependências do sistema e o Poetry.
- Configura o ambiente Python, instala as dependências definidas em `pyproject.toml` e `poetry.lock`.
- Copia o código da aplicação e expõe a porta 8000.
- No CMD, executa as migrações com Alembic e inicia o Uvicorn.

---

## Passos para Executar a Aplicação

1. **Configure o `.env`:**
   Edite o arquivo `.env` com os dados corretos (credenciais, chaves, etc.).

2. **Construa e Inicie os Containers:**
   No diretório raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```
   Isso compila a imagem da aplicação e inicia os containers para a API e o banco de dados.

3. **Acesse a API:**
   Após a inicialização, a API estará disponível em:
   ```
   http://localhost:8000
   ```
