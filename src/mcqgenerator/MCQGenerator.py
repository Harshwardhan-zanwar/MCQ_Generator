import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging

from langchain_google_genai import ChatGoogleGenerativeAI  #type : ignore
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence , RunnableLambda , RunnablePassthrough


load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",   # or "gemini-2.0-pro"
    temperature=0.3,
    api_key=key  
)

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
    )

quiz_chain = RunnableSequence(quiz_generation_prompt | llm)

TEMPLATE="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

review_chain = RunnableSequence(quiz_evaluation_prompt | llm)
# Extract quiz content from AIMessage and combine with original subject
def extract_quiz_and_subject(input_dict):
    """Extract quiz from AIMessage and combine with subject from original input"""
    quiz_output = quiz_chain.invoke(input_dict)
    return {
        "quiz": quiz_output.content if hasattr(quiz_output, 'content') else str(quiz_output),
        "subject": input_dict["subject"]
    }

generate_evaluate_chain = RunnableLambda(extract_quiz_and_subject) | review_chain
#generate_evaluate_chain = RunnableSequence(quiz_chain | review_chain)

