import os
import re
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
    elif file.name.endswith('.txt'):
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading text file: {e}")
    else:
        raise Exception("Unsupported file format. Please upload a PDF or TXT file.")

def get_table_data(quiz_str):
    try:
        # Extract the JSON between triple backticks or curly braces
        match = re.search(r"```(.*?)```", quiz_str, re.DOTALL)
        if not match:
            match = re.search(r"({.*})", quiz_str, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in quiz string.")

        json_str = match.group(1).strip()
        quiz_dict = json.loads(json_str)

        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value['question']
            options = ' | '.join(
                [f"{opt}: {ans}" for opt, ans in value['options'].items()]
            )
            correct = value['answer']
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False