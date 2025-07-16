from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
# from langchain.callbacks import get_openai_callback
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2
import streamlit as st

# Load JSON file
with open("C:\\Users\\Z\\Desktop\\End-to-End-Project\\mcqgen-project\\mcq-generater\\experiment\\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

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

# Helper function to parse quiz string (placeholder)
def get_table_data(quiz_str):
    try:
        # Assuming quiz_str is a JSON string of a list of dicts
        return json.loads(quiz_str)
    except Exception:
        return None

st.title("MCQ Generator")

with st.form("user_input"):
    st.write("Upload a PDF or TXT file and generate Multiple Choice Questions (MCQs) from its content.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])

    # Number input for MCQs
    num_questions = st.number_input("Number of MCQs to generate", min_value=3, max_value=50, value=5)

    subject = st.text_input("Subject for the MCQs", value="General Knowledge", max_chars=50)

    tone = st.selectbox("Tone of the MCQs", options=["Easy", "Medium", "Hard", "Very Hard"], index=0)

    # Button to trigger MCQ generation
    button = st.form_submit_button("Generate MCQs")
    if button and uploaded_file is not None and num_questions and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                if not text.strip():
                    st.error("No text found in the uploaded file.")
                else:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": num_questions,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.text(traceback.format_exc())
            else:
                if isinstance(response, dict):
                    quiz_str = response.get('quiz', None)
                    if quiz_str is not None:
                        table_data = get_table_data(quiz_str)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1  # Start index from 1
                            st.table(df)
                            st.text_area(label="Quiz Review", value=response.get('review', ''), height=200)
                        else:
                            st.error("Failed to parse the quiz data.")
                    else:
                        st.write(response)