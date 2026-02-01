📘 MCQ Generator

An AI-powered Multiple Choice Question (MCQ) Generator
Convert user input into structured multiple-choice questions using NLP and LangChain.

🔍 Project Overview

MCQ Generator is a Python-based tool that automates the creation of multiple-choice questions from text or natural language inputs. Using modern NLP techniques and large language models, the application generates relevant MCQs efficiently and presents them in an interactive UI for users.

🛠️ Tech Stack

Python

LangChain — Natural language processing workflow

Google Gemini (or similar LLM)

Streamlit — Web application for user interface


🚀 Key Features

Generates multiple-choice questions from text input.

Uses LLMs for higher quality question generation.

Includes a streamlit web app for live interaction.

Produces structured output (CSV/JSON) for further use.

📁 Project Structure
MCQ_Generator/

├── README.md

├── requirements.txt

├── StreamlitAPP.py

├── response.json

├── setup.py

├── test.py

└── src/


To start your MCQ Generator app:

streamlit run StreamlitAPP.py


Upload content.

Click “Generate MCQs” and view output in the app.
