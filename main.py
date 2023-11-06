from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langsmith import Client

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

from utils import StreamHandler
import os

st.set_page_config(page_title="Apps Script Assistant", page_icon="Austral Logo.png")

# Set LangSmith environment variables
try:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
    os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
    os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
except:
    print("Running locally")

client = Client()
# st.title("Mastering Google Apps Scripts")
button_css =""".stButton>button {
    color: #4F8BF9;
    border-radius: 50%;
    height: 2em;
    width: 2em;
    font-size: 4px;
}"""
st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

template = """You are an excellent assistant in helping students learn about Google Apps Script.
You will assist students in any concern. They are begginers.
"""

prompt_template = ChatPromptTemplate(messages = [SystemMessage(content=template), MessagesPlaceholder(variable_name="chat_history"), HumanMessagePromptTemplate.from_template("{input}")])

from langchain.chains import LLMChain

def send_feedback(run_id, score):
    client.create_feedback(run_id, "user_score", score=score)

first_message = """Welcome! I am an AI teaching assistant specialized in Google Apps Script.
I can help you understand the basics, guide you through complex tasks, or assist you in debugging your scripts.
Feel free to ask anything from simple commands, to how to automate tasks in Google Sheets, or even how to interact with other Google Services.
Let's start coding!
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [AIMessage(content=first_message)]

for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user", avatar="ninja.png").write(msg.content)
    else:
        st.chat_message("assistant", avatar="Austral Logo.png").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user", avatar="ninja.png").write(prompt)

    with st.chat_message("assistant", avatar="Austral Logo.png"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-4")
        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain({"input":prompt, "chat_history":st.session_state.messages[-20:]}, include_run_info=True)
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))
        run_id = response["__run"].run_id

        col_blank, col_text, col1, col2 = st.columns([10, 2,1,1])
        with col_text:
            st.text("Feedback:")

        with col1:
            st.button("👍", on_click=send_feedback, args=(run_id, 1))

        with col2:
            st.button("👎", on_click=send_feedback, args=(run_id, 0))
