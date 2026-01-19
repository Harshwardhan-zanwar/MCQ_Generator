import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data, extract_json_from_text
import streamlit as st
# from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# loading json file
# Fixed: Use raw string (r prefix) or forward slashes for Windows paths
with open(r'C:\GEN AI\MCQ_Generator\response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

# Create a form using st.form - only for input fields
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    # Input Fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    # Add Button
    button = st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                response = generate_evaluate_chain.invoke(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
                
                # Extract content from AIMessage if it's not a dict
                if hasattr(response, 'content'):
                    # It's an AIMessage object
                    response_content = response.content
                    if isinstance(response_content, list) and len(response_content) > 0:
                        # Handle list of content blocks
                        text_parts = []
                        for item in response_content:
                            if isinstance(item, dict):
                                text_parts.append(item.get('text', ''))
                            else:
                                text_parts.append(str(item))
                        response_text = ' '.join(text_parts)
                    elif isinstance(response_content, str):
                        response_text = response_content
                    else:
                        response_text = str(response_content)
                elif isinstance(response, dict):
                    response_text = response.get("quiz", str(response))
                else:
                    response_text = str(response)
                
                # Try to extract JSON quiz data from the response text
                quiz_dict = extract_json_from_text(response_text)
                
                if quiz_dict:
                    # Store quiz data in session state (outside form)
                    st.session_state.quiz_data = quiz_dict
                    st.session_state.current_question = 1
                    st.session_state.user_answers = {}
                    st.session_state.checked_answers = {}
                    st.session_state.response_text = response_text
                    st.session_state.response_object = response
                    st.rerun()  # Rerun to display quiz outside form
                else:
                    st.error("⚠️ Could not extract quiz data in JSON format from the response.")
                    st.write("Response text:", response_text[:500])  # Show first 500 chars
                
            except Exception as e:
                st.error(f"❌ Error occurred: {str(e)}")
                st.error(f"Details: {traceback.format_exc()}")

# Display MCQ Interface OUTSIDE the form (after form ends)
if 'quiz_data' in st.session_state and st.session_state.quiz_data:
    # Get quiz data
    quiz_data = st.session_state.quiz_data
    current_q = st.session_state.current_question
    total_questions = len(quiz_data)
    
    # Display Review if available
    if 'response_text' in st.session_state:
        review_text = ""
        response_obj = st.session_state.get('response_object', None)
        response_text = st.session_state.response_text
        
        if isinstance(response_obj, dict):
            review_text = response_obj.get("review", "")
        elif hasattr(response_obj, 'content'):
            # Try to extract review from response content
            content_str = response_text if isinstance(response_text, str) else str(response_obj)
            # Look for complexity analysis or review section
            if "Complexity Analysis" in content_str:
                review_text = content_str.split("###")[0] if "###" in content_str else content_str[:200]
        
        if review_text:
            with st.expander("📊 Quiz Review & Analysis", expanded=False):
                st.write(review_text)
    
    # Navigation buttons (now outside form, so they work!)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀ Previous", disabled=(current_q <= 1), key="prev_btn"):
            st.session_state.current_question -= 1
            st.rerun()
    with col3:
        if st.button("Next ▶", disabled=(current_q >= total_questions), key="next_btn"):
            st.session_state.current_question += 1
            st.rerun()
    
    # Question counter
    st.markdown(f"### 📝 Question {current_q} of {total_questions}")
    
    # Get current question data
    question_key = str(current_q)
    if question_key not in quiz_data:
        # Try to find the key
        question_keys = sorted(quiz_data.keys(), key=lambda x: int(x) if x.isdigit() else 0)
        question_key = question_keys[current_q - 1] if current_q <= len(question_keys) else question_keys[0]
    
    question_data = quiz_data[question_key]
    
    # Display question
    st.markdown(f"**{question_data['mcq']}**")
    st.markdown("---")
    
    # Display options as radio buttons
    options_list = list(question_data['options'].items())
    
    # Initialize user answer if not present
    answer_key = f"q{current_q}_answer"
    if answer_key not in st.session_state.user_answers:
        st.session_state.user_answers[answer_key] = None
    
    # Get previously selected answer for this question
    prev_answer = st.session_state.user_answers.get(answer_key, None)
    options_only = [opt for opt, _ in options_list]
    
    # Determine index for radio button
    radio_index = None
    if prev_answer and prev_answer in options_only:
        radio_index = options_only.index(prev_answer)
    
    # Radio buttons for options
    selected_option = st.radio(
        "Select your answer:",
        options=options_only,
        format_func=lambda x: question_data['options'][x],
        key=f"radio_{current_q}",
        index=radio_index
    )
    
    # Update user answer
    if selected_option:
        st.session_state.user_answers[answer_key] = selected_option
    
    # Check Answer button (now outside form, so it works!)
    check_col1, check_col2, check_col3 = st.columns([1, 1, 1])
    with check_col2:
        check_button = st.button("✓ Check Answer", key=f"check_{current_q}", use_container_width=True)
    
    # Display result if answer is checked
    if check_button or f"q{current_q}_checked" in st.session_state.checked_answers:
        st.session_state.checked_answers[f"q{current_q}_checked"] = True
        correct_answer = question_data['correct']
        user_answer = st.session_state.user_answers[answer_key]
        
        if user_answer == correct_answer:
            st.success(f"✅ Correct! Well done!")
        else:
            st.error(f"❌ Incorrect. The correct answer is **{correct_answer}: {question_data['options'][correct_answer]}**")
    
    # Progress indicator
    st.markdown("---")
    answered_count = sum(1 for k in st.session_state.user_answers.values() if k is not None)
    st.progress(answered_count / total_questions)
    st.caption(f"Progress: {answered_count}/{total_questions} questions answered")