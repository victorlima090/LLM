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

# region config
API_KEY="AIzaSyBCG93yixkk84XyiOmZUu1-kINLjpwvFl0"

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = "AIzaSyBCG93yixkk84XyiOmZUu1-kINLjpwvFl0"

# endregion

# region create front
st.title("Hello World!")

st.header("This is a header", divider=True)

st.markdown("## This is a markdown header")

x = st.select_slider("Nível de educação",options=["Educado","Neutro","Mal-Educado","MUITO Mal-Educado"],)

st.write(f"Nice level is {x}")

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

#TODO define aqui o nível de educação do modelo
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You talk like a pirate. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

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
#TODO get user input
query= "Ola eu sou o Victor, me de um poema com 1000 caracteres sobre a vide um programador, em portugues"

input_mesages = [HumanMessage(query)]
# output = app.invoke({"messages": input_mesages}, config)

for chunk, metadata in app.stream(
    {"messages": input_mesages},
    config,
    stream_mode="messages",
):
    if isinstance(chunk, AIMessage):  # Filter to just model responses
        print(chunk.content)

