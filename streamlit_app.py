import streamlit as st
import os
import uuid
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import AIMessage
import streamlit as st
from langchain_core.messages import  trim_messages

st.title("Chatbot com LangGraph e Gemini")

x = st.select_slider("Nível de educação",options=["Educado","Neutro","Mal-Educado"],value="Neutro")

st.write(f"Nível de educação:{x}")

st.title("Simple chat")

# Inicializa o estado do chat
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# Botão para mostrar o chat
if st.button("Abrir Chat"):
    st.session_state.show_chat = True

# region config
API_KEY="AIzaSyBCG93yixkk84XyiOmZUu1-kINLjpwvFl0"

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = "AIzaSyBCG93yixkk84XyiOmZUu1-kINLjpwvFl0"

# endregion
uuid_str = str(uuid.uuid4())
model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

prompt_educado = "Você é um atendente muito educado, responda todas as perguntas da melhor forma possível."
prompt_neutro = "Você é um atendente neutro, responda todas as perguntas de forma neutra."
prompt_mal_educado = "Você é um atendente muito mal educado, responda todas as perguntas da pior forma possível."
prompt_educacao = ""
if x == "Educado":
    prompt_educacao = prompt_educado
elif x == "Neutro":
    prompt_educacao = prompt_neutro
elif x == "Mal-Educado":
    prompt_educacao = prompt_mal_educado
#TODO define aqui o nível de educação do modelo
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            prompt_educacao,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def call_model(state: MessagesState):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke({"messages": trimmed_messages})
    response = model.invoke(prompt)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
config = {"configurable": {"thread_id": uuid_str}}



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.show_chat:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Posso ti ajudar em algo?"):    
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        input_mesages = [HumanMessage(prompt)]
        

        def stream_response():
            response = ""

            for chunk, metadata in app.stream(
                {"messages": input_mesages},
                config,
                stream_mode="messages",
            ):
                if isinstance(chunk, AIMessage):
                    response += chunk.content
                    yield chunk.content
            st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.write_stream(stream_response())

