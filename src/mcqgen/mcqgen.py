from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq
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

load_dotenv()

key = os.getenv("GROQ_API_TOKEN")
print(key)

with open("C:\\Users\\Z\\Desktop\\End-to-End-Project\\mcqgen-project\\mcq-generater\\Response.json", "r") as file:
    response_json = json.load(file)
# print(response_json)

prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template="""
    Text: {text}
    You are an expert MCQ maker. Given the above text, it is you job to \
    create a quiz of {number} multiple choice questions (MCQs) with answers for {subject} students in {tone} tone.
    Make sure the questions are not repeated. check all the questions to be conforming text as well.
    Make sure to format your response in JSON format with the following structure: ad use it as a guide:
    Ensure to make {number} MCQs
    ### Response json:
    {response_json}
    """
)

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=key,
    temperature=0.7
)

chain = LLMChain(llm=llm, prompt=prompt, output_key='quiz', verbose=True)

template = """
    You are an expert english grammarian and writer. Given a multiple choice quiz for {subject} students, it is your job to \
    You need to evaluate the complexity of the questions and give a complete analysis of the quiz. Only use max 50 words.
    if the quiz is not at per with the cognitive and analytical abilities of the students, \
    update the quiz questions which need to be changed and change the tone such that is perfectly fits the students abilities.
    Quiz_MCQs: {quiz}
    Check from an expert english Writer of the above quiz:
    """
# print(template)
    
prompt2 = PromptTemplate(
    input_variables=["quiz", "subject"],
    template=template
)

review_chain = LLMChain(llm=llm, prompt=prompt2, output_key='review', verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[chain, review_chain],
    input_variables=['text', 'number', 'subject', 'tone', 'response_json'],
    output_variables=['quiz', 'review'],
    verbose=True)


