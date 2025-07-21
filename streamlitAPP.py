from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import os
import re
from src.mcqgen.mcqgen import generate_evaluate_chain

import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2
import streamlit as st

# Load JSON file
with open("Response.json", "r") as file:
    response_json = json.load(file)

# Helper function to read uploaded file
def read_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return ""

def get_table_data(quiz_str):
    try:
        if isinstance(quiz_str, str):
            quiz_str = quiz_str.strip()
            # st.text_area("🔍 Raw Quiz JSON String", quiz_str, height=150)

            # Extract JSON from within code block or brackets
            # First try: between ``` and ```
            match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", quiz_str, re.DOTALL)
            if not match:
                # Fallback: find first [ and last ]
                match = re.search(r"(\[.*\])", quiz_str, re.DOTALL)

            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            else:
                st.error("❌ JSON content not found in quiz string.")
                return None

        elif isinstance(quiz_str, list):
            return quiz_str
        else:
            return None
    except Exception as e:
        st.error(f"JSON Parse Error: {e}")
        return None

st.title("📘 MCQ Generator")

with st.form("user_input"):
    st.write("Upload a PDF or TXT file and generate Multiple Choice Questions (MCQs) from its content.")

    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    num_questions = st.number_input("Number of MCQs to generate", min_value=3, max_value=50, value=5)
    subject = st.text_input("Subject for the MCQs", value="General Knowledge", max_chars=50)
    tone = st.selectbox("Tone of the MCQs", options=["Easy", "Medium", "Hard", "Very Hard"], index=0)

    button = st.form_submit_button("Generate MCQs")
    if button and uploaded_file is not None:
        with st.spinner("🧠 Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                if not text.strip():
                    st.error("❌ No text found in the uploaded file.")
                else:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": num_questions,
                        "subject": subject,
                        "tone": tone,
                        "response_json": response_json
                    })
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
                st.text(traceback.format_exc())
            else:
                if isinstance(response, dict):
                    quiz_str = response.get('quiz', None)
                    if quiz_str is not None:
                        table_data = get_table_data(quiz_str)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index += 1  # Start index from 1
                            st.table(df)
                            st.text_area("📋 Quiz Review", value=response.get('review', ''), height=200)
                        else:
                            st.error("❌ Failed to parse the quiz data.")
                    else:
                        st.write("❓ No 'quiz' field found in the response.")
                else:
                    st.write("⚠️ Unexpected response format.")
