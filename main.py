import os 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

# Initalize Chat Model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4.1-nano", api_key=OPENAI_API_KEY)

# Define Prompt Template
prompt = ChatPromptTemplate([
    ("system", "You are an helpful study assistant"),
    MessagesPlaceholder(variable_name='history'),
    ("human", "{input}"),
])

# In-memory message history store
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Create a Conversation Chain
conversation_chain = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)

# Start a conversation for a specific session
session_id = "user123"

while True:
    user_input = input("You: ")
