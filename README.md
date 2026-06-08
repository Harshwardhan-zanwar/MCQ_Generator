# 🧠 QuizForge AI

> An LLM-powered MCQ generation system that transforms any text or document into structured, interactive multiple-choice quizzes — built with LangChain, Google Gemini, and Streamlit.

---

## 🔍 Overview

QuizForge AI automates the creation of high-quality multiple-choice questions from raw text or uploaded documents. By leveraging large language models through a LangChain pipeline, it generates contextually accurate questions with configurable difficulty, subject tagging, and structured JSON output — all accessible through an interactive Streamlit interface.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Orchestration | LangChain + Google Gemini |
| Frontend / UI | Streamlit |
| File Parsing | PyPDF / text file reader |
| Output Format | JSON / CSV |
| Language | Python 3.10+ |

---

## ✨ Key Features

- **LLM-Powered Generation** — Uses Google Gemini via LangChain chains to produce contextually accurate MCQs from any input text
- **Configurable Parameters** — Control number of questions (3–50), subject domain, and complexity level (Simple / Medium / Hard)
- **File Upload Support** — Accepts PDF and `.txt` files as source documents
- **Structured JSON Output** — All questions generated in a consistent JSON schema with `mcq`, `options`, and `correct` fields
- **Interactive Quiz UI** — Paginated question-by-question interface with answer checking, progress tracking, and navigation
- **Complexity Analysis** — LangChain evaluate chain reviews and analyses generated quiz quality post-generation
- **Session State Management** — Streamlit session state preserves answers and progress across question navigation

---

## 📁 Project Structure

```
QuizForge_AI/
├── StreamlitAPP.py          # Main Streamlit application & UI logic
├── response.json            # MCQ response schema / template
├── requirements.txt         # Dependencies
├── setup.py                 # Package setup
├── test.py                  # Unit tests
├── src/
│   └── mcqgenerator/
│       ├── MCQGenerator.py  # LangChain generate + evaluate chain
│       ├── utils.py         # File reader, table parser, JSON extractor
│       └── logger.py        # Logging configuration
└── experiment/              # Jupyter notebooks for prompt experimentation
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Harshwardhan-zanwar/MCQ_Generator.git
cd MCQ_Generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 4. Run the app
```bash
streamlit run StreamlitAPP.py
```

---

## 🧪 How It Works

1. Upload a **PDF or text file** (or paste raw text)
2. Set the **number of MCQs**, **subject**, and **complexity level**
3. Click **"Create MCQs"** — LangChain invokes the Gemini chain
4. Questions are extracted from the LLM's JSON response and rendered as an interactive paginated quiz
5. Select answers, click **"Check Answer"** for instant feedback
6. Track progress via the bottom progress bar

---

## 🔗 LangChain Pipeline

```
Input Text + Config
       ↓
generate_evaluate_chain (LangChain SequentialChain)
       ↓
[Generation Chain] → Raw MCQ JSON from Gemini
       ↓
[Evaluation Chain] → Complexity Analysis & Review
       ↓
extract_json_from_text() → Parsed Quiz Dict
       ↓
Streamlit Interactive UI
```

---

## 📦 Requirements

```
langchain
langchain-google-genai
streamlit
python-dotenv
pandas
PyPDF2
```
