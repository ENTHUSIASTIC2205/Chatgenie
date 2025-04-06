import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import base64
import google.generativeai as gen_ai


load_dotenv()

GOOGLE_API_KEY = os.getenv("AIzaSyD8Umu-6JLeBfoneLgonBWU7RTBGzjKBqA")
gen_ai.configure(api_key="AIzaSyD8Umu-6JLeBfoneLgonBWU7RTBGzjKBqA")

gemini_model = gen_ai.GenerativeModel(model_name='gemini-1.5-flash')

def img_base64(img_path):
    try:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error("⚠️ Image file not found. Check the file path.")
        return None


st.set_page_config(
    page_title="ChatGenie",
    page_icon="🧞‍♂️",
    layout="wide",  
)


with st.sidebar:
    img_path = os.path.join(r"C:\Users\mk\OneDrive\Pictures\Screenshots\Screenshot 2025-04-03 235827.png")
    img_data = img_base64(img_path)
    if img_data:
        st.sidebar.markdown(f'<img src="data:image/png;base64,{img_data}" class="cover-glow">', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("⚙️ Settings")
    model_choice = st.selectbox("Select AI Model", ["gemini-1.5-flash"])
    
    st.markdown("---")
    st.markdown("👨‍💻 Created by Gaurav Rawat")
    
    show_basic_info = st.sidebar.checkbox("About", value=True)
    if show_basic_info:
        st.sidebar.markdown("""
               ChatGenie is an AI-powered chatbot built using Google's Gemini AI to provide intelligent responses to user queries. This chatbot can answer questions, and engage in natural conversations.
        ### ✨ Key Features:
           - AI-Powered Conversations - Uses Google's Gemini AI model for intelligent responses.
           - User-Friendly Interface - Clean, responsive, and interactive chat design.
        """)
    
    st.markdown("---")
    img_path =(r"C:\Users\mk\OneDrive\Pictures\Screenshots\Screenshot 2025-04-04 002222.png")
    img_base64 = img_base64(img_path)
    if img_base64:
        st.sidebar.markdown(f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',unsafe_allow_html=True,)
        


if "chat_session" not in st.session_state:
    st.session_state.chat_session = gemini_model.start_chat(history=[])

if model_choice != 'gemini-1.5-flash':
    gemini_model = gen_ai.GenerativeModel(model_name=model_choice)

st.markdown(
    "<h1 style='text-align: center; color: #ffffff;'>🤖 ChatGenie - AI Assistant</h1>", 
    unsafe_allow_html=True
)

for msg in st.session_state.chat_session.history:
    if msg.parts:
        with st.chat_message("assistant" if msg.role == "model" else msg.role):
            st.markdown(msg.parts[0].text)


user_input = st.chat_input("Ask anything...")
if user_input:
    st.chat_message("user").markdown(f"**You:** {user_input}")

    try:
        ai_response = st.session_state.chat_session.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(f"**ChatGenie:** {ai_response.text}")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")

