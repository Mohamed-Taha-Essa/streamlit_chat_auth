# Streamlit Chat with Authentication & Persistent History

A professional AI-powered chat application built with Streamlit, LangChain, and SQLAlchemy. This project features a secure user authentication system and persistent conversation history stored in a local SQLite database.

## 🚀 Features

- **Secure Authentication**: User registration and login system using Argon2 password hashing.
- **Persistent Chat History**: All conversations and messages are stored in a SQLite database using SQLAlchemy ORM.
- **Multi-Conversation Support**: Users can create multiple chat sessions and switch between them seamlessly via the sidebar.
- **AI Integration**: Powered by LangChain and HuggingFace (using the `EssentialAI/rnj-1-instruct` model).
- **Streaming Responses**: Real-time AI response streaming for a better user experience.
- **Session Management**: Automatic session handling with Streamlit's session state.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Framework**: [LangChain](https://www.langchain.com/)
- **LLM Provider**: [HuggingFace](https://huggingface.co/)
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite)
- **Security**: [Passlib](https://passlib.readthedocs.io/) (Argon2)
- **Environment Management**: `python-dotenv`

## 📂 Project Structure

```text
.
├── app.py              # Main Streamlit application entry point
├── ai.py               # LangChain logic and LLM configuration
├── auth.py             # Authentication logic (hashing, verification)
├── auth_ui.py          # Streamlit UI components for login/register
├── db.py               # Database models and CRUD operations
├── .env                # Environment variables (API keys)
├── .gitignore          # Git ignore file
└── chat_history.db     # SQLite database (generated at runtime)
```

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd streamlit_chat_auth
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install streamlit langchain langchain-huggingface sqlalchemy passlib argon2-cffi python-dotenv
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your HuggingFace API key:
```env
hugging_face_api_key=your_huggingface_api_token_here
```

## 🏃 How to Run

Start the Streamlit application by running:
```bash
streamlit run app.py
```

## 📝 Usage

1. **Register**: Create a new account using the 'Register' tab.
2. **Login**: Sign in with your credentials.
3. **Chat**: Start a new conversation or select an existing one from the sidebar.
4. **Interact**: Type your messages and receive real-time AI responses.

---
*Developed with ❤️ for learning GenAI and Full-Stack development.*
