# LangGraph Chatbot with Persistent Memory (SQLite)

This repository implements a conversational AI chatbot using **LangGraph**, **LangChain**, and **Google Generative AI (Gemini)**. The chatbot supports multiple conversation threads with **persistent memory** stored in an SQLite database. A Streamlit-based frontend provides an interactive chat UI with a sidebar for managing and switching between conversations.

---

## 🚀 Features

* **Multi-threaded Conversations**: Each conversation is assigned a unique `thread_id` using UUIDs.
* **Persistent Memory**: Conversations are stored in an SQLite database via `SqliteSaver`, so chats remain available even after restarting.
* **Streamlit Frontend**: Interactive chat interface with:

  * Sidebar to create and switch between threads
  * Chat-style display using `st.chat_message`
  * Realtime AI response streaming
* **Google Generative AI (Gemini)** as the LLM backend
* **LangGraph Integration**: Graph-based conversational state management with checkpointing.

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/langgraph-chatbot.git
cd langgraph-chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Make sure you have a `requirements.txt` file. To generate it from your environment:

```bash
pip freeze > requirements.txt
```

Then install:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## 📂 Project Structure

```
langgraph-chatbot/
│
├── frontend.py          # Streamlit-based UI
├── langgraph_backend.py # LangGraph chatbot backend with SQLite persistence
├── chat_db              # SQLite database file (auto-created)
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

---

## 🖥️ Usage

### Run the chatbot frontend

```bash
streamlit run frontend.py
```

### Frontend UI Walkthrough

* **Sidebar**

  * **New Chat**: Start a new thread (conversation)
  * **Conversations**: List of saved threads. Click to load old chats.
* **Main Chat Window**

  * Displays conversation history
  * Input box (`st.chat_input`) for user queries
  * AI responses streamed in real-time

---

## ⚙️ Backend Logic (`langgraph_backend.py`)

* **LLM**: `ChatGoogleGenerativeAI` (Gemini 1.5 Flash)
* **StateGraph**: Manages conversational state with a single `chat_node`
* **SqliteSaver**: Handles checkpointing and conversation persistence
* **Thread Retrieval**: `retreive_all_threads()` lists all stored conversations from the database

---

## 📜 Example Conversation Flow

1. User starts a new chat → new `thread_id` is generated.
2. Messages are appended to `st.session_state['message_history']`.
3. LangGraph processes the conversation state through `chat_node`.
4. AI responses are streamed back to the UI.
5. Conversation history is checkpointed in SQLite for persistence.

---

## 🛡️ Notes

* Ensure that your **Google API Key** has access to the Gemini model.
* The SQLite database (`chat_db`) is created automatically in the project root.
* If you want to reset memory, delete `chat_db`.

---

## 📌 Future Improvements

* Add user authentication for personalized chat histories.
* Implement message search within past threads.
* Enhance UI with message timestamps.
* Support exporting conversations to `.txt` or `.json`.

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or want to suggest improvements, open an issue first.

---

## 📄 License

This project is licensed under the MIT License.
