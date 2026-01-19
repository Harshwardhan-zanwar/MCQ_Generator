#this is a helper file that all the helper functions will be written here

import os
from pypdf import PdfReader 
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

def extract_json_from_text(text):
    """
    Extract JSON from text that may contain markdown code blocks.
    Handles both plain JSON and JSON wrapped in ```json code blocks.
    """
    try:
        # First, try to find JSON in markdown code blocks
        if "```json" in text:
            start = text.find("```json") + 7  # Start after ```json
            end = text.find("```", start)
            if end != -1:
                json_str = text[start:end].strip()
                return json.loads(json_str)
        elif "```" in text:
            # Try generic code blocks
            start = text.find("```") + 3
            end = text.find("```", start)
            if end != -1:
                json_str = text[start:end].strip()
                # Remove "json" if it's the first line
                if json_str.startswith("json"):
                    json_str = json_str[4:].strip()
                return json.loads(json_str)
        
        # Try to find JSON object in the text (between { and })
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = text[start:end+1]
            return json.loads(json_str)
        
        # If all else fails, try parsing the whole text as JSON
        return json.loads(text)
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None