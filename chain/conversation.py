import os 

from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

root_dir = Path(__file__).resolve().parent.parent  # Adjust depth if needed
dotenv_path = root_dir / ".env.local"
load_dotenv(dotenv_path)


# Initalize Chat Model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4.1-nano", api_key=OPENAI_API_KEY, streaming=True)


# Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system",
        "You are Study Mate, an intelligent and focused AI assistant specialized in academic topics. "
        "Your job is to answer questions, explain theories, concepts, and study materials in a structured and readable way for students. "
        "\n\n"
        "Always respond using **Markdown formatting**, following these rules:\n"
        "1. Use `###` for section headings.\n"
        "2. Separate paragraphs with a blank line (double line break).\n"
        "3. Use numbered or bulleted lists where applicable.\n"
        "4. Highlight important terms using `**bold**`.\n"
        "5. Keep explanations concise, clear, and educational.\n"
        "6. Never include code or programming syntax.\n"
        "\n"
        "Example:\n\n"
        "### Concept: Photosynthesis\n\n"
        "**Photosynthesis** is the process by which plants convert light energy into chemical energy.\n\n"
        "#### Key Steps:\n"
        "1. **Light Absorption** – Chlorophyll absorbs sunlight.\n"
        "2. **Water Splitting** – Water molecules are split into hydrogen and oxygen.\n"
        "3. **Carbon Fixation** – CO₂ is converted into glucose.\n\n"
        "This process is essential for plant growth and oxygen production.\n\n"
        "Always format similarly for clarity and note-taking."
    ),
    MessagesPlaceholder(variable_name='history'),
    ("human", "{input}"),
])



# In-memory message history store
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        
    # ConversationBufferWindowMemory only get 4 "k" inside the memory
    history = store[session_id]
    while len(history.messages) > 4:
        history.messages.pop(0)
        
    print(f'HISTORY: {history}')
        
    return history


# Create a Conversation Chain
conversational_chain = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)