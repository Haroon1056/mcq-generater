import os
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
        # convert the quiz from a str to dict:
        quitz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        #iterate through the quiz dict and extract the data
        for key, value in quitz_dict.items():
            mcq = value['question']
            options = ' | '.join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value['options'].items()
                ]
            )
            correct = value['answer']
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False