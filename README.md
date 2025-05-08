# Finance Bot 🧾🤖

**Finance Bot** is an AI-powered assistant designed to help users **manage and organize their finances** directly from messaging platforms like **WhatsApp** and **Telegram**.

With Finance Bot, you can:

- 🗂️ **Manage categories** to track and split different types of expenses
- 💸 **Log and manage transactions** in a structured and intelligent way

---

## 🚀 Features

- Seamless interaction through chat-based commands
- Categorization of expenses
- Easy transaction tracking and management
- AI-powered support using [Langchain](https://www.langchain.com)

---

## 🛠️ Setup Instructions

Finance Bot is a Python project that uses [**uv**](https://github.com/astral-sh/uv), a fast Python package manager. Make sure you have Python and `uv` installed before getting started.

### 1. Create a virtual environment

```sh
uv venv
```

### 2. Activate the virtual environment

**On Unix/macOS:**

```sh
source .venv/bin/activate
```

**On Windows:**

```sh
.venv/Scripts/activate
```

### 3. Install dependencies

```sh
uv sync
```

### 4. Configure environment variables

Copy the example environment file and edit it:

```sh
cp .env.example .env
```

Then, open the `.env` file and **set the environment variables**:

- **USER_ID**: A user identification to use the chat, this is the user identification that will be stored in the database. The max limit of characters is 14.
- **OPENAI_API_KEY**: Your OPENAI API key.

### 5. Run database migrations

```sh
python manage.py migrate
```

---

## ▶️ Running the Bot

After completing the setup, you can run Finance Bot in a terminal for testing purposes:

```sh
python manage.py langchain_chat
```

This will start the Langchain-powered interactive shell where you can simulate conversations and test the bot's responses locally before deploying it to a messaging platform like WhatsApp or Telegram.

---

## 📱 Messaging Platform Integration

Finance Bot can be integrated with:

- WhatsApp
- Telegram

> ⚠️ Integration details and webhook setup instructions will be added soon.
