# Finance Bot 🧾🤖

**Finance Bot** is an AI-powered assistant designed to help users **manage and organize their finances** directly from messaging platforms like **WhatsApp** and **Telegram**.

## 🏗️ Architecture

The application follows a clean, modular architecture with a clear separation of concerns:

### Agent System

- **BaseAgent**: Abstract base class providing common functionality for all agents
- **FinanceAgent**: Specialized agent for financial operations
- **AgentFactory**: Factory pattern for creating agent instances
- **ClassLoader**: Secure class loading with validation
- **AgentConfiguration**: Manages agent settings and configurations

### Key Features

- **Modular Design**: Easy to extend with new agent types and tools
- **Secure**: Safe class loading and configuration management
- **Scalable**: Stateless design allows for horizontal scaling
- **Maintainable**: Clean separation of concerns and SOLID principles

With Finance Bot, you can:

- 🗂️ **Manage categories** to track and split different types of expenses
- 💸 **Log and manage transactions** in a structured and intelligent way

---

## 🚀 Features

- Seamless interaction through chat-based commands
- Categorization of expenses
- Easy transaction tracking and management
- AI-powered support using [Langchain](https://www.langchain.com)
- Integration with WhatsApp and Telegram

---

## 📦 Dependencies

- **Python** >= 3.10
- [**uv**](https://github.com/astral-sh/uv) (fast Python package manager)
- [**Docker**](https://www.docker.com/) and [**docker-compose**](https://docs.docker.com/compose/) (optional, for containerized deployment)

### Python Package Dependencies

All Python dependencies are managed in `pyproject.toml` and installed via `uv`. Key dependencies include:

- Django >= 5.1.7
- djangorestframework >= 3.16.0
- drf-spectacular >= 0.28.0
- channels[daphne] >= 4.2.2
- langchain-openai >= 0.2.14
- langgraph >= 0.0.0  # For agent orchestration
- psycopg2-binary >= 2.9.10
- python-dotenv >= 1.0.0
- gunicorn >= 21.2.0
- daphne >= 4.1.0

### Agent System Dependencies

- `langchain-core`: Core components for building agents
- `langchain-openai`: OpenAI integration for language models
- `langgraph`: For building stateful, multi-actor applications
- `pydantic`: For data validation and settings management

---

## 🛠️ Installation

### 1. Clone the repository

```sh
git clone https://github.com/gustavosvalentim/finance-bot
cd finance-bot
```

### 2. Create a virtual environment

```sh
uv venv
```

### 3. Activate the virtual environment

**On Unix/macOS:**

```sh
source .venv/bin/activate
```

**On Windows:**

```sh
.venv/Scripts/activate
```

### 4. Install dependencies

```sh
uv sync
```

### 5. Configure environment variables

Copy the example environment file and edit it:

```sh
cp .env.example .env
```

Edit `.env` and set the required environment variables (see [Environment Variables](#️-environment-variables) below).

### 6. Run database migrations

```sh
python manage.py migrate
```

---

## ▶️ Running the Bot

### Local Interactive Shell (Langchain Agent)

You can interact with the AI agent directly from the command line using the `langchain_chat` management command. This is useful for testing, debugging, or quick interactions without needing a messaging client.

**Basic Usage**

Run the following command to start the interactive shell:

```sh
python manage.py langchain_chat
```

- This will start a local shell where you can interact with the AI agent.
- By default, it uses the `USER_ID` and `USER_NICKNAME` from your `.env` file.

**Advanced Usage with Command-Line Arguments**

You can also specify the user ID and name directly as command-line arguments. This is useful for testing different user contexts without changing your `.env` file.

```sh
python manage.py langchain_chat --user-id="<your_user_id>" --user-name="<your_user_name>"
```

- Replace `<your_user_id>` and `<your_user_name>` with the desired values.
- Type your messages and receive AI-powered responses. Type `bye`, `exit`, or `quit` to exit the shell.

### Telegram Bot

To run the Telegram bot:

```sh
python manage.py telegram_bot
```

- Make sure you have set `TELEGRAM_API_KEY` in your `.env` file (see below).
- The bot will listen for messages and respond using the AI agent.
- **To create your own Telegram bot and get the API key, follow the official guide:** [How to Create a Bot with BotFather](https://core.telegram.org/bots#botfather)

### Django Web Server (with Channels)

To run the Django server (with Channels for WebSockets):

```sh
daphne -b 0.0.0.0 -p 8000 finance_bot.asgi:application
```

Or, for development:

```sh
python manage.py runserver
```

---

## 🐳 Docker & Docker Compose

You can run the entire stack using Docker and docker-compose (recommended for production or quick setup):

### 1. Build and start the services

```sh
docker-compose up --build
```

- This will build the API and start a Postgres database.
- The Django app will run migrations, collect static files, start the Telegram bot, and launch the ASGI server (Daphne) on port 8000.

### 2. Environment Variables

- Docker Compose uses the `.env` file for configuration.
- Make sure to set all required variables before running `docker-compose up`.

---

## ⚙️ Environment Variables

Below are the environment variables available in `.env.example`:

| Variable           | Description |
|--------------------|-------------|
| `USER_ID`          | The default user ID for the `langchain_chat` command if not provided as an argument. Example: `+5511999999999` |
| `USER_NICKNAME`    | The default user name for the `langchain_chat` command if not provided as an argument. Example: `"Mr. Buffet"` |
| `DEBUG`            | Enable debug logs. Set to `True` for verbose logging, `False` for production. |
| `OPENAI_API_KEY`   | Your OpenAI API key for using GPT models. Required for AI features. Get it from [OpenAI](https://platform.openai.com/account/api-keys). |
| `AGENT_USE_MEMORY` | Set to `True` to enable agent memory (helps with long conversations, but may use more tokens). |
| `TELEGRAM_API_KEY` | Your Telegram bot API key. Required to run the Telegram bot. Get it from [BotFather](https://core.telegram.org/bots#botfather). |
| `ALLOWED_HOSTS`    | Comma-separated list of allowed hosts for Django. Required for admin panel and production deployments. |
| `DATABASE_ENGINE`  | (Optional) Set to `postgres` to use PostgreSQL instead of SQLite. |
| `DATABASE_HOST`    | Database host (used if `DATABASE_ENGINE=postgres`). |
| `DATABASE_PORT`    | Database port (used if `DATABASE_ENGINE=postgres`). |
| `DATABASE_NAME`    | Database name (used if `DATABASE_ENGINE=postgres`). |
| `DATABASE_USER`    | Database user (used if `DATABASE_ENGINE=postgres`). |
| `DATABASE_PASSWORD`| Database password (used if `DATABASE_ENGINE=postgres`). |

**Note:**
- If you do not set `DATABASE_ENGINE`, the app will use SQLite by default.
- For production, it is recommended to use PostgreSQL and set all database variables.
- The `.env.example` file contains comments and examples for each variable.

---

## 📱 Messaging Platform Integration

Finance Bot can be integrated with:

- WhatsApp *(integration details coming soon)*
- Telegram *(see above for setup)*

---

## 📝 Additional Notes

- For more advanced configuration, see the `finance_bot/settings.py` file.
- Static files are collected to `/static` when running in Docker.
- The admin panel is available at `/admin` (requires superuser setup).
- **To create a superuser for admin access, run:**

  ```sh
  python manage.py createsuperuser
  ```

  Follow the prompts to set up your admin username, email, and password. For more details, see the [Django createsuperuser documentation](https://docs.djangoproject.com/en/stable/ref/django-admin/#createsuperuser) and the [Django admin site guide](https://docs.djangoproject.com/en/stable/ref/contrib/admin/).

- For API documentation, DRF Spectacular is included (Swagger/OpenAPI support).

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
