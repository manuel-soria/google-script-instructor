from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langsmith import Client

from utils import StreamHandler
client = Client()

st.set_page_config(page_title="Apps Script Assistant", page_icon="")
st.title("🥷 Mastering Google Apps Scripts")
button_css =""".stButton>button {
    color: #4F8BF9;
    border-radius: 50%;
    height: 2em;
    width: 2em;
    font-size: 4px;
}"""
st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

