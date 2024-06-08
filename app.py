import streamlit as st
import requests
import google.generativeai as genai
import time
import json

api_key = "AIzaSyDSdQssjbwc-I-4aHQyi2MS-etlbKD92mY"

# Check if the API key is provided
if api_key == "YOUR_API_KEY_HERE":
    st.error("Please replace 'YOUR_API_KEY_HERE' with your actual API key.")
    st.stop()
else:
    genai.configure(api_key=api_key)

# Function to get response from Gemini Pro Vision API with retry logic
def get_gemini_response(input_text, context, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([context, input_text])
            return response.text.strip()
        except Exception as e:
            if "quota" in str(e).lower() or "500" in str(e):
                st.warning(f"Oops! Slowdown Please. Trying again in {delay} seconds...")
                attempt += 1
                time.sleep(delay)
            else:
                st.error("Something went wrong. Please try again later.")
                return None
    st.error("We're unable to process your request right now. Please try again later or contact support.")
    return None

# Initialize Streamlit app
st.set_page_config(page_title="AI Assistant")
st.header("AI Assistant")

# Fetch JSON data from the file
with open("data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Prepare the base context for the AI
base_context = f"""
Tum Shakoor ho, ek AI bot, jo ek ustaad ke liye har talib ilm ke baray mein tamam maloomat rakhta hai. Neeche di gayi maloomat ke mutabiq sirf roman Urdu mein jawab do.

Yahan maloomat hai jo tum jawab dene ke liye istemal kar sakte ho:
{data}
"""

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Input prompt
input_text = st.text_area("Ask a question:")

submit = st.button("Ask Question")

# If submit button is clicked
if submit:
    if not input_text:
        st.write("Please enter a question.")
    else:
        response = get_gemini_response(input_text, base_context)
        if response:
            # Add the question and response to the conversation history
            st.session_state.conversation.append({"user": input_text, "bot": response})
        else:
            st.error("Failed to get a response from the AI. Please try again.")

# Display the conversation history in reverse order
if st.session_state.conversation:
    conversation_reversed = reversed(st.session_state.conversation)
    for i, chat in enumerate(conversation_reversed):
        if i == 0:
            # Style for the latest response
            user_style = "background-color: #FFF2A6; padding: 8px; border-radius: 10px; color: black; max-width: 80%;"
            bot_style = "background-color: #FFF2A6; padding: 8px; border-radius: 10px; color: black; max-width: 80%;"
        else:
            # Style for other responses
            user_style = "background-color: #CBE7FF; padding: 8px; border-radius: 10px; color: black; max-width: 80%;"
            bot_style = "background-color: #C2E0FF; padding: 8px; border-radius: 10px; color: black; max-width: 80%;"

        st.markdown(f"""
         <div style="display: flex; justify-content: flex-end; align-items: center; margin: 10px 0;">
            <div style="{user_style}">
                <strong></strong> {chat['user']}
          

        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; align-items: center; margin: 10px 0;">
            <div style="margin-right: 10px;">
                <img src="https://img.icons8.com/?size=100&id=L3uh0mNuxBXw&format=png&color=000000" width="50">
            </div>
            <div style="{bot_style}">
                <strong></strong> {chat['bot']}
            </div>
        </div>
        """, unsafe_allow_html=True)